from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
from lxml.html import etree as et


if __name__ == "__main__":
    html = urlopen("https://www.youdao.com/w/eng/saw/#keyfrom=dict2.index")
    bs_obj = BeautifulSoup(html, 'html.parser')
    html_str = bs_obj.prettify()
    root = et.fromstring(html_str)