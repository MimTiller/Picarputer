
import requests
from requests_toolbelt.utils import dump
import json
import time
PARAMS = {'User-Agent':'HiCamera','Connection':'Keep-Alive'}

command = 'http://192.168.0.1/cgi-bin/hi3510/getfilecount.cgi HTTP/1.1'
r = requests.get(command,params=PARAMS)
print (r.headers)
print(r.content)

command = 'http://192.168.0.1/cgi-bin/hi3510/getfilecount.cgi HTTP/1.1'
r = requests.get(command,params=PARAMS)
print (r.headers)
print(r.content)


with requests.Session() as r:
	command = 'http://192.168.0.1/cgi-bin/hi3510/getfilelistinfoios.cgi HTTP/1.1'
	r = requests.get(command,params=PARAMS)
	time.sleep(5)
	print(r.headers)
	print(r.content)
