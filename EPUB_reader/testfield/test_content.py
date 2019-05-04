from lxml.html import etree as ET

if __name__ == "__main__":
    tree = ET.parse('../datafield/A Clash of Kings - George R.R. Martin/content/'
                    'George R.R. Martin - Fire and Ice 02 - A Clash of Kings v4.0 (BD)_split_6.html')
    root = tree.getroot()
    ns = {"default": root.nsmap[None]}
    # NavPoints = root.xpath(".//*[contains(@class, 'MsoHyperlink')]/default:a", namespaces=ns)
    # tmpNode = NavPoints[0]
    # NavPointsTuples = []
    # for node in NavPoints:
    #     chapter_name = node.xpath("./default:navLabel/default:text/text()", namespaces=ns)
    #     chapter_loc = node.xpath("./default:content/@src", namespaces=ns)
    #     NavPointsTuples.append((chapter_name, chapter_loc))
