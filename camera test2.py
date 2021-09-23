
import requests
from requests_toolbelt.utils import dump
command = 'https://google.com'
r = requests.get(command)
print(r.headers)
print(r.content)
