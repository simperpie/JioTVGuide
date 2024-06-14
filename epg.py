import requests
from requests.exceptions import HTTPError, RequestException
from datetime import datetime
import xmltodict
import time
import sys
import gzip
from concurrent.futures import ThreadPoolExecutor
import os
import shutil
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API = "http://jiotv.data.cdn.jio.com/apis"
IMG = "http://jiotv.catchup.cdn.jio.com/dare_images"
channel = []
programme = []
error = []
result = []
done = 0

# Proxy configuration
proxies = {
    "http": "http://27.107.27.13:80",
    "https": "http://20.219.180.149:3129",
}
fallback_proxy = "124.123.108.15:80"
residential_proxy = os.getenv("RES_PXY", "125.99.106.250:3128")
residential_proxy2 = os.getenv("RES_PXY2", "125.99.106.250:3128")
proxyTimeOut = 10000
proxyListUrl = f"https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout={proxyTimeOut}&country=IN&ssl=IN&anonymity=IN"
useFallback = False

class NoProxyFound(Exception):
    def __init__(self):
        self.message = "No working proxy found"
        super().__init__(self.message)

def retry_on_exception(max_retries, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Retry {retries + 1}/{max_retries} - Exception: {e}")
                    retries += 1
                    time.sleep(delay)
            raise Exception(f"Function '{func.__name__}' failed after {max_retries} retries.")
        return wrapper
    return decorator

@retry_on_exception(max_retries=10, delay=5)
def get_working_proxy():
    response = requests.get(proxyListUrl)
    response.raise_for_status()
    proxies = response.text.strip().split("\r\n")
    proxies.insert(0, residential_proxy)
    proxies.insert(0, residential_proxy2)
    working_proxy = None

    for prx in proxies:
        tproxies = {"http": f"http://{prx}"}
        try:
            test_url = f"{API}/v3.0/getMobileChannelList/get/?langId=6&os=android&devicetype=phone&usertype=tvYR7NSNn7rymo3F&version=285"
            response = requests.get(test_url, proxies=tproxies, timeout=5)
            if response.status_code == 200:
                working_proxy = prx
                break
        except RequestException:
            continue

    if working_proxy:
        logger.info("Found working proxy")
        return working_proxy
    else:
        logger.error("No working proxy found")
        raise NoProxyFound()

MAX_RETRY = 10

def genEPG(i, c):
    global channel, programme, error, result, API, IMG, done
    for day in range(-1, 7):
        retry_count = 0
        while retry_count < MAX_RETRY:
            try:
                resp = requests.get(f"{API}/v1.3/getepg/get", params={"offset": day, "channel_id": c['channel_id'], "langId": "6"}, proxies=proxies).json()
                if day == 0:
                    channel.append({
                        "@id": c['channel_id'],
                        "display-name": c['channel_name'],
                        "icon": {"@src": f"{IMG}/images/{c['logoUrl']}"}
                    })
                for eachEGP in resp.get("epg"):
                    pdict = {
                        "@start": datetime.utcfromtimestamp(int(eachEGP['startEpoch'] * .001)).strftime('%Y%m%d%H%M%S'),
                        "@stop": datetime.utcfromtimestamp(int(eachEGP['endEpoch'] * .001)).strftime('%Y%m%d%H%M%S'),
                        "@channel": eachEGP['channel_id'],
                        "@catchup-id": eachEGP['srno'],
                        "title": eachEGP['showname'],
                        "desc": eachEGP['description'],
                        "category": eachEGP['showCategory'],
                        "icon": {"@src": f"{IMG}/shows/{eachEGP['episodePoster']}"}
                    }
                    if eachEGP['episode_num'] > -1:
                        pdict["episode-num"] = {"@system": "xmltv_ns", "#text": f"0.{eachEGP['episode_num']}"}
                    if eachEGP.get("director") or eachEGP.get("starCast"):
                        pdict["credits"] = {
                            "director": eachEGP.get("director"),
                            "actor": eachEGP.get("starCast") and eachEGP.get("starCast").split(', ')
                        }
                    if eachEGP.get("episode_desc"):
                        pdict["sub-title"] = eachEGP.get("episode_desc")
                    programme.append(pdict)
                break  # Break out of the retry loop if successful
            except Exception as e:
                logger.error(f"Retry failed (Retry Count: {retry_count + 1}): {e}")
                retry_count += 1
                if retry_count == MAX_RETRY:
                    error.append(c['channel_id'])
                else:
                    time.sleep(2)  # Retry after sleeping for 2 seconds
    done += 1

if __name__ == "__main__":
    stime = time.time()
    if useFallback:
        httpProxy = fallback_proxy
    else:
        httpProxy = get_working_proxy()
    proxies = {
        "http": f"http://{httpProxy}",
        "https": f"http://{httpProxy}",
    }
    try:
        resp = requests.get(f"{API}/v3.0/getMobileChannelList/get/?langId=6&os=android&devicetype=phone&usertype=tvYR7NSNn7rymo3F&version=285", proxies=proxies)
        resp.raise_for_status()
        raw = resp.json()
    except HTTPError as exc:
        code = exc.response.status_code
        logger.error(f'Error calling getMobileChannelList: {code}')
    except Exception as e:
        logger.error(f'Error: {e}')
    else:
        result = raw.get("result")
        with ThreadPoolExecutor() as executor:
            executor.map(genEPG, range(len(result)), result)
        epgdict = {"tv": {"channel": channel, "programme": programme}}
        epgxml = xmltodict.unparse(epgdict, pretty=True)
        output_file = 'epg.xml.gz'
        target_folder = 'path_to_target_folder'  # Change this to your target folder
        target_file = os.path.join(target_folder, output_file)

        # Write and compress the EPG XML
        with open(output_file, 'wb+') as f:
            f.write(gzip.compress(epgxml.encode('utf-8')))
        
        # Move the file to the target directory
        shutil.move(output_file, tempest_config/epg)
        logger.info("EPG updated at %s", datetime.now())
        
        if error:
            logger.error(f'Error in channels: {error}')

        logger.info(f"Took {time.time() - stime:.2f} seconds")
