import json

import requests
from modules.destiny2util.update import *


BASE = "https://www.bungie.net"

PATHS = {
    "manifest": "/Platform/Destiny2/Manifest/",
    "content": {}
}

data = "./data/destiny2util/"

langs = ('en', 'zh-chs', 'zh-cht')


def update_manifest():
    print("Fetching manifest")
    res = requests.request("GET", BASE + PATHS["manifest"])
    with open(data + 'manifest.json', 'w') as f:
        t = res.content.decode('utf-8')
        t = json.loads(t)
        json.dump(t, f)

    return t


def update_paths():
    with open(data + 'manifest.json', 'r') as f:
        res = json.load(f)
    for i in langs:
        print(f"Updating {i} path")
        if i not in res["Response"]['jsonWorldContentPaths']:
            raise Exception(f"Incorrect language code {i}")
        PATHS['content'][i] = res["Response"]['jsonWorldContentPaths'][i]


def fetch_data():
    update_paths()
    for i in langs:
        print(f"Fetching {i} data")
        with open(data + i + ".json", 'w') as f:
            url = BASE + PATHS['content'][i]
            res = requests.request("GET", url)
            t = res.content.decode('utf-8')
            t = json.loads(t)
            json.dump(t, f)
