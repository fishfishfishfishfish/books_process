from lxml import etree
from construct_dict import insert_a_word


if __name__ == "__main__":
    DictHTML = etree.parse("冰与火之歌中文维基_dict.html", etree.HTMLParser())
    words = DictHTML.xpath("//span/word/text()")
    description_node = DictHTML.xpath("//description")
    description = list()
    for n in description_node:
        description.append(n.xpath("string(.)"))
    for w, d in zip(words, description):
        print(w)
        insert_a_word(w, d)
