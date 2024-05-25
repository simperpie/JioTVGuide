import requests

class NoProxyFound(Exception):
    def _init_(self):
        self.message = "No working proxy found"
        super()._init_(self.message)

def get_working_proxy():
    proxyListUrl = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=IN&ssl=IN&anonymity=IN"
    response = requests.get(proxyListUrl)
    response.raise_for_status()
    proxies = response.text.strip().split("\r\n")
    residential_proxy = "125.99.106.250:3128"
    residential_proxy2 = "125.99.106.250:3128"
    proxies.insert(0, residential_proxy)
    proxies.insert(0, residential_proxy2)
    working_proxy = None
    for prx in proxies:
        tproxies = {
            "http": "http://{prx}".format(prx=prx),
        }
        try:
            test_url = "http://jiotv.data.cdn.jio.com/apis/v3.0/getMobileChannelList/get/?langId=6&os=android&devicetype=phone&usertype=tvYR7NSNn7rymo3F&version=285"
            response = requests.get(test_url, proxies=tproxies, timeout=5)
            if response.status_code == 200:
                working_proxy = prx
                break
        except requests.exceptions.RequestException:
            pass
    if working_proxy:
        print("Got working proxy:", working_proxy)
        return working_proxy
    else:
        print("No working proxy found")
        raise NoProxyFound()

# Example usage:
proxy = get_working_proxy()
print(proxy)
