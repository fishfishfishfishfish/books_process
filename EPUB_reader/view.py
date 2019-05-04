from lxml.html import etree as et
import epub_reader

import utils_log


def diy_parse_content_list(content_list_file):
    if isinstance(content_list_file, str):
        content_list_file = open(content_list_file)
    tree = et.parse(content_list_file)
    root = tree.getroot()
    ns = {"default": root.nsmap[None]}
    nav_points = root.xpath(".//*[contains(@class, 'MsoHyperlink')]/default:a", namespaces=ns)
    nav_points_tuples = []
    for node in nav_points:
        chapter_name = node.text
        chapter_loc = "content/" + node.attrib["href"]
        nav_points_tuples.append((chapter_name, chapter_loc))
    return nav_points_tuples


if __name__ == "__main__":
    utils_log.initial_logger("utils_sqlite")
    BookName = "datafield/A Clash of Kings - George R.R. Martin.epub"
    DBName = "datafield/A Clash of Kings - George R.R. Martin-3.db"
    ER = epub_reader.EPUBReader(BookName, DBName)
    ER.get_metadata()
    ContentListLoc = "content/George R.R. Martin - Fire and Ice 02 - A Clash of Kings v4.0 (BD)_split_1.html"
    ER.get_content_list(ContentListLoc, diy_parse_content_list)
    ER.get_sentences()
