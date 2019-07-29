import hashlib
import json
import random
import re
import urllib
from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
from lxml.html import etree as et

import utils_text_preprocess


def from_youdao(query: str):
    try:
        html = urlopen("https://www.youdao.com/w/eng/%s/#keyfrom=dict2.index" % (quote(query), ))
        bs_obj = BeautifulSoup(html, 'html.parser')
        html_str = bs_obj.prettify()
        html_str = re.split("(</html>)", html_str)
        html_str = html_str[0] + html_str[1]
        root = et.fromstring(html_str)
        ns = {"default": root.nsmap[None]}
        xpath = ".//*[contains(@id, 'phrsListTab')]//*[contains(@class, 'container')]//default:li//text()"
        li_text = root.xpath(xpath, namespaces=ns)
        meaning = [utils_text_preprocess.clean_text(li) for li in li_text]
    except BaseException as e:
        meaning = str(e)
    return meaning


def from_kingsoft(query: str):
    try:
        xml = urlopen(f"http://dict-co.iciba.com/api/dictionary.php?w={query}&key=1F287830F78CD6CFEB5E4279236CBEBB")
        root = et.parse(xml)
        xpath_pos = ".//pos//text()"
        xpath_acc = ".//acceptation//text()"
        acceptations = root.xpath(xpath_acc)
        pos = root.xpath(xpath_pos)
        meaning = [p + utils_text_preprocess.clean_text(a) for p, a in zip(pos, acceptations)]
    except BaseException as e:
        meaning = str(e)
    return meaning


def from_baidu(query: str):
    try:
        appid = "20190729000322103"
        secret_key = "f7VF7IUDgc8ERoBHrMwZ"
        salt = random.randint(32768, 65536)
        sign = appid + query + str(salt) + secret_key
        sign = hashlib.md5(sign.encode()).hexdigest()
        params = {"q": query, "from": "auto", "to": "zh", "appid": "20190729000322103", "salt": str(salt), "sign": sign}
        params = urllib.parse.urlencode(params).encode("UTF-8")
        # 获得返回的结果，结果为json格式
        response = urlopen("http://api.fanyi.baidu.com/api/trans/vip/translate", params).read().decode("utf-8")
        js = json.loads(response)  # 将json格式的结果转换字典结构
        meaning = str(js["trans_result"][0]["dst"])  # 取得翻译后的文本结果
    except BaseException as e:
        meaning = str(e)
    return meaning
