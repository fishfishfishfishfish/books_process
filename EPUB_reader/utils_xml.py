import os
from lxml.html import etree as et


def strip_namespace(xml_tag: str):
    if "}" in xml_tag:
        return xml_tag.split("}")[-1]
    return xml_tag


def get_metadata(opf_file):
    if isinstance(opf_file, str):
        opf_file = open(opf_file)
    tree = et.parse(opf_file)
    ns = {"dc": "http://purl.org/dc/elements/1.1/",
          "opf": "http://www.idpf.org/2007/opf",
          "calibre": "http://calibre.kovidgoyal.net/2009/metadata"}
    namespace_dc = tree.xpath(".//opf:metadata/*[namespace-uri()='%s']" % (ns["dc"],), namespaces=ns)
    dc_tuples = []
    for node in namespace_dc:
        dc_tuples.append((strip_namespace(node.tag), node.text))
    return dc_tuples


def parse_toc(toc_file):
    if isinstance(toc_file, str):
        toc_file = open(toc_file)
    tree = et.parse(toc_file)
    root = tree.getroot()
    ns = {"default": root.nsmap[None]}
    nav_points = root.xpath(".//default:navPoint", namespaces=ns)
    nav_points_tuples = []
    for node in nav_points:
        chapter_name = node.find("./default:navLabel/default:text", namespaces=ns).text
        chapter_loc = node.find("./default:content", namespaces=ns).attrib["src"]
        nav_points_tuples.append((chapter_name, chapter_loc))
    return nav_points_tuples


def find_text_by_id(xml_file, node_id: str):
    if isinstance(xml_file, str):
        xml_file = open(xml_file)
    tree = et.parse(xml_file)
    root = tree.getroot()
    ns = {"default": root.nsmap[None]}
    dest_elements = root.xpath(".//*[contains(@id, '%s')]//parent::*"
                               "//parent::*//following-sibling::*//text()" % (node_id, ), namespaces=ns)
    res = ""
    for t in dest_elements:
        res += t if t is not None else ""
    return res
