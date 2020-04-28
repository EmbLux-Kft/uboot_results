# pip3 install requests --user

import requests
import os
from datetime import datetime

today = datetime.now()
build_date = today.strftime("%Y-%m-%d %H:%M:%S")

newresult = {
    'title':'tbot triggerd test',
    'build_date':build_date,
    'arch':'arm',
    'cpu' :'armv7'
    'soc':'imx6',
    'toolchain':'bootlin',
    'boardname':"wandboard DL",
    'basecommit':'2345252ef',
    'defconfig':'wandboard_defconfig',
    'splsize':12345,
    'ubsize':765463,
    'success':"True",
    'content':"from client.py",
}

from requests.auth import HTTPBasicAuth

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

# get stuff from Environment
try:
    URL = os.environ['SERVER_URL']
except KeyError:
    raise RuntimeError("set environment variable SERVER_URL")

try:
    PORT = os.environ['SERVER_PORT']
except KeyError:
    raise RuntimeError("set environment variable SERVER_PORT")

try:
    user = os.environ['SERVER_USER']
except KeyError:
    raise RuntimeError("set environment variable SERVER_USER")

try:
    password = os.environ['SERVER_PASSWORD']
except KeyError:
    raise RuntimeError("set environment variable SERVER_PASSWORD")

# setup variables
location = f"{PORT}/api"
loc = f"{location}/tokens"

print ("GET token ------------------- ")
s = requests.Session()
s.auth =(user, password)
r = s.post(url = f"{URL}:{loc}")

if r.status_code != 200:
    raise RuntimeError(f"got status code {r.status_code}")

print("R ", r)
print("R status code ", r.status_code)
data = r.json()
print("DATA ", data)

tok = data["token"]
print ("GET result ------------------- ")
loc = f"{location}/result/1"
r = s.get(url = f"{URL}:{loc}", auth=BearerAuth(tok))

print("R ", r)
print("R status code ", r.status_code)
if r.status_code != 200:
    raise RuntimeError(f"got status code {r.status_code}")

data = r.json()
print("DATA ", data)

print ("POST result ------------------- ")
loc = f"{location}/newresult"
print("DATA ", newresult)
headers = {}
r = s.post(url = f"{URL}:{loc}", auth=BearerAuth(tok), json=newresult, headers=headers)

print("R ", r)
print("R status code ", r.status_code)
if r.status_code != 201:
    raise RuntimeError(f"got status code {r.status_code}")

data = r.json()
print("DATA ", data)

