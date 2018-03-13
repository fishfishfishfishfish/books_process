from bs4 import BeautifulSoup
import os
import sqlite3
import re

if __name__ == '__main__':
    # 建立数据库
    conn = sqlite3.connect('AmericanGods.db')
    cursor = conn.cursor()
    cursor.execute('''create table Sentence (
                        id integer primary key autoincrement,
                        sentence text not null,
                        chapter text not null)''')
    cursor.close()
    conn.commit()

    path = "books"
    files = os.listdir(path)
    print(files)
    # file = files[0]
    for file in files:
        chapter = file.split('.')[0]
        raw_file = open(path + '/' + file, encoding="UTF-8")
        soup = BeautifulSoup(raw_file.read(), 'html.parser')
        body = soup.body
        p = [text for text in body.stripped_strings]
        for sentences in p:
            sentence_list = re.split(r'(?<!Mr|rs)\.|!|\?|“|”', sentences)
            for sentence in sentence_list:
                if sentence != '':
                    cursor = conn.cursor()
                    cursor.execute('insert into Sentence (id, sentence, chapter) values(null, ?, ?)',
                                   (sentence.strip().lower(), chapter))
                    cursor.close()
                    conn.commit()
        print(file)
    conn.close()
