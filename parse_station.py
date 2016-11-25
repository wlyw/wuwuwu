#coding: utf-8
import re
import requests
import json
from pprint import pprint

url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8979'
response = requests.get(url, verify=False)
stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
#pprint(dict(stations), indent=4)

jsobj = json.dumps(dict(stations))
fileobj = open('stations.json','w')
fileobj.write(jsobj)
fileobj.close()