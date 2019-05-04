# import xml.etree.ElementTree as ET
from lxml.html import etree as ET
import re


def strip_namespace(xml_tag: str):
    if "}" in xml_tag:
        return xml_tag.split("}")[-1]
    return xml_tag


if __name__ == "__main__":
    tree = ET.parse('../datafield/A Clash of Kings - George R.R. Martin/metadata.opf')
    NS = {"dc": "http://purl.org/dc/elements/1.1/",
          "opf": "http://www.idpf.org/2007/opf",
          "calibre": "http://calibre.kovidgoyal.net/2009/metadata"}

    NamespaceDC = tree.xpath(".//opf:metadata/*[namespace-uri()='%s']" % (NS["dc"], ), namespaces=NS)
    DCTuples = []
    for node in NamespaceDC:
        DCTuples.append((strip_namespace(node.tag), node.text))

