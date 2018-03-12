from bs4 import BeautifulSoup
import re

if __name__ == '__main__':
    file_index = 1
    chapter_index = 1
    chapter_out_file = open("sentences", 'w')
    while file_index <= 6:
        book_f = open(str(file_index)+".html", encoding="UTF-8")
        soup = BeautifulSoup(book_f.read(), "html.parser")
        while chapter_index <= 16:
            chapter_id = chapter_pre+"%02d" % (chapter_index+2)
            # 找出章节位置
            body = soup.body
            chapter = body.find('h2', {'id': chapter_id})
            if chapter is None:
                file_index += 1
                break
            print(chapter.string)
            # 写入文件
            chapter_out_file.write(chapter.string+"\n")
            para = chapter.next_sibling
            while para.next_element.name != "a":
                if para.name is not None:
                    sentences = re.split(r'(?<!Mr|rs)\.|!|\?|“|”', para.string.lower())
                    for sentence in sentences:
                        if sentence != '':
                            chapter_out_file.write(sentence.strip(' ') + "\n")
                para = para.next_sibling
            chapter_out_file.write("<end of chapter>\n\n")
            chapter_index += 1
