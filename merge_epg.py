import requests
import gzip
import shutil
import xml.etree.ElementTree as ET
import os

def download_file(url, file_name):
    response = requests.get(url, stream=True)
    with open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

def decompress_file(file_name):
    with gzip.open(file_name, 'rb') as f_in:
        with open(file_name[:-3], 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def merge_xml_files(files, selected_channels):
    master_tree = ET.parse(files[0])
    master_root = master_tree.getroot()

    second_tree = ET.parse(files[1])
    second_root = second_tree.getroot()

    # Include only selected channels from the second file
    for elem in second_root.findall('channel'):
        if elem.attrib['id'] in selected_channels:
            master_root.append(elem)
    
    for elem in second_root.findall('programme'):
        if elem.attrib['channel'] in selected_channels:
            master_root.append(elem)

    master_tree.write('merged_epg.xml')

def compress_file(file_name):
    with open(file_name, 'rb') as f_in:
        with gzip.open(file_name + '.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

# URLs of the EPG files
urls = [
    'https://github.com/simperpie/epg-grabber/raw/main/tempest_config/epg/tempest.xml.gz',
    'https://github.com/matthuisman/i.mjh.nz/raw/master/SamsungTVPlus/in.xml.gz'
]

# Selected channels from the second EPG
selected_channels = ['INBD21000016Y', 'INBC43000071R', 'INBD4700006JD', 'INBD4800001IR', 'INBC4300009W5', 'IN1300001NN']

# Download the files
for i, url in enumerate(urls):
    download_file(url, f'epg{i+1}.xml.gz')

# Decompress the files
for i in range(len(urls)):
    decompress_file(f'epg{i+1}.xml.gz')

# Merge the XML files with filtering
merge_xml_files(['epg1.xml', 'epg2.xml'], selected_channels)

# Compress the merged file
compress_file('merged_epg.xml')

# Rename the merged file
renamed_file = 'epg.xml.gz'
os.rename('merged_epg.xml.gz', renamed_file)