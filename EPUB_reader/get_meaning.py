from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
from lxml.html import etree as et

import utils_text_preprocess


def from_youdao(query: str):
    html = urlopen("https://www.youdao.com/w/eng/%s/#keyfrom=dict2.index" % (quote(query), ))
    bs_obj = BeautifulSoup(html, 'html.parser')
    html_str = bs_obj.prettify()
    root = et.fromstring(html_str)
    ns = {"default": root.nsmap[None]}
    xpath = ".//*[contains(@id, 'phrsListTab')]//*[contains(@class, 'container')]//default:li//text()"
    li_text = root.xpath(xpath, namespaces=ns)
    meaning = [utils_text_preprocess.clean_text(li) for li in li_text]
    return meaning

