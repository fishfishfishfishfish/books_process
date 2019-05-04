from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup

import utils_text_preprocess


def from_youdao(query: str):
    html = urlopen("https://www.youdao.com/w/eng/%s/#keyfrom=dict2.index" % (quote(query), ))
    bs_obj = BeautifulSoup(html, 'html.parser')
    tab = bs_obj.find_all(id="phrsListTab")
    trans = []
    for t in tab:
        trans.extend(t.find_all(class_="trans-container"))
    meaning = []
    for t in trans:
        i_nodes = t.find_all("li")
        for i in i_nodes:
            meaning.append(utils_text_preprocess.clean_text(i.get_text()))
    return meaning


if __name__ == "__main__":
    pass
