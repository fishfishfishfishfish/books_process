from bs4 import BeautifulSoup
import re
import sqlite3

if __name__ == '__main__':
    file_path = "peterPan/"
    file_index = 1
    raw_file = open(file_path + str(file_index) + ".html", encoding="UTF-8")
    soup = BeautifulSoup(raw_file.read(), "html.parser")
    body = soup.body
    p = [text for text in body.stripped_strings]
    # print(p)
    # counter = 0
    # for i in p:
    #     if i == 'Chapter 17 WHEN WENDY GREW UP':
    #         print(counter)
    #         break
    #     counter += 1
    p = p[38:]

    # 建立数据库
    conn = sqlite3.connect('PeterPan.db')
    cursor = conn.cursor()
    cursor.execute('''create table Sentence (
                        id integer primary key autoincrement,
                        sentence varchar(500) not null,
                        chapter integer not null)''')
    chapter = ""
    for sentences in p:
        if re.match(r'^Chapter\s\d', sentences):
            chapter = sentences.split(' ')[1]
        else:
            sentence_list = re.split(r'(?<!Mr|rs)\.|!|\?|“|”', sentences)
            for sentence in sentence_list:
                if sentence != '':
                    # print(sentence)
                    cursor.execute('insert into Sentence (id, sentence, chapter) values(null, ?, ?)',
                                   (sentence.strip().lower(), chapter))
    res = cursor.execute("select * from Sentence where id < 30").fetchall()
    raw_file.close()
    cursor.close()
    conn.commit()

    file_index = 2
    while file_index <= 6:
        raw_file = open(file_path + str(file_index) + ".html", encoding="UTF-8")
        soup = BeautifulSoup(raw_file.read(), "html.parser")
        body = soup.body
        p = [text for text in body.stripped_strings]
        cursor = conn.cursor()
        for sentences in p:
            if re.match(r'^Chapter\s\d', sentences):
                chapter = sentences.split(' ')[1]
            elif sentence == '*** END OF THIS PROJECT GUTENBERG EBOOK PETER PAN ***':
                break
            else:
                sentence_list = re.split(r'(?<!Mr|rs)\.|!|\?|“|”', sentences)
                for sentence in sentence_list:
                    if sentence != '':
                        cursor.execute('insert into Sentence (id, sentence, chapter) values(null, ?, ?)',
                                       (sentence.strip().lower(), chapter))

        raw_file.close()
        cursor.close()
        conn.commit()
        file_index += 1

    conn.close()
