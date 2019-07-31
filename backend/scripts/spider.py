# -*- coding: UTF-8 -*-
import os
from lxml import etree
import requests
import json
from bs4 import BeautifulSoup

base_url = "http://m.mafengwo.cn"
image_num = 9
result_dir = "./result"

def spider(key):
    url = "https://www.mafengwo.cn/ajax/ajax_any_index.php"
    querystring = {"sAction":"getSearchCity","sKey":key}
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "www.mafengwo.cn",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive"
    }

    response = requests.get(url, headers=headers, params=querystring)
    response.encoding = "utf-8"
    data = json.loads(response.text)
    id = data["payload"]["data"][0]["id"]
    print ("id: %d" % id)

    url = "https://pagelet.mafengwo.cn/note/pagelet/recommendNoteApi"
    querystring = {"params":"{\"type\":2,\"objid\":%s,\"page\":1,\"ajax\":1,\"retina\":1}" % id}
    headers["Host"] = "pagelet.mafengwo.cn"

    response = requests.request("GET", url, headers=headers, params=querystring)
    response.encoding = "utf-8"
    data = json.loads(response.text)
    html = data["data"]["html"]

    soup = BeautifulSoup(html, features="lxml")
    tn_list = soup.find_all("div", "tn-image")
    for item in tn_list[:3]:
        url = base_url + item.a['href']
        print (url)

        headers["Host"] = "www.mafengwo.cn"
        response = requests.request("GET", url, headers=headers)

        # find img
        soupp = BeautifulSoup(response.text, features="lxml")
        img_url_list = soupp.find_all("img", "_j_lazyload _j_needInitShare")
        for (index, item) in enumerate(img_url_list):
            img_url = item["data-src"]
            print (img_url)
            res = requests.request("GET", img_url)

            if not os.path.exists(result_dir):
                os.path.mkdir(result_dir)

            with open("%s/%s.jpg" % (result_dir, item["data-pid"]), "wb") as f:
                f.write(res.content)
            if index >= image_num:
                break


if __name__ == "__main__":
    spider("迪拜")
