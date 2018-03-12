#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import collections
import re
import sqlite3

if __name__ == '__main__':
    punk = r'[\s\d!！?？.,"“”‘’：:;；\[\]()—]'  # 标点符号
    # 连接数据库
    conn = sqlite3.connect('PeterPan.db')
    #  单词表
    cursor = conn.cursor()
    cursor.execute('''create table Word (
                            word text primary key not null unique,
                            meaning text,
                            count integer not null)''')
    #  单词句子联系表
    cursor.execute('''create table WSLink (
                                word text not null,
                                sentenceId integer,
                                foreign key (word) references Word(word),
                                foreign key (sentenceId) references Sentence(id),
                                primary key (word, sentenceId))''')
    cursor.close()
    conn.commit()

    chapter = 1
    while chapter <= 17:
        cursor_s = conn.cursor()
        sentences = cursor_s.execute('select * from Sentence where chapter = ' + str(chapter))
        sentence = sentences.fetchone()
        while sentence is not None:
            words = re.split(punk, sentence[1].strip("\n"))
            for w in words:
                if w == '':
                    continue
                cursor = conn.cursor()
                # w = '\'' + w + '\''
                if cursor.execute('''select * from Word where word = ?''', (w,)).fetchone() is None:
                    cursor.execute('''insert into Word(word, meaning, count)
                                        values (?, null, ?)''', (w, '1'))
                    cursor.execute('''insert into WSLink(word, sentenceId)
                                        values(?,?)''', (w, str(sentence[0])))
                    # print(w)
                else:
                    new_count = int(cursor.execute('''select count from Word where word = ?''', (w,)).fetchone()[0]) + 1
                    cursor.execute('''update Word set count = ? where word = ?''',
                                   (str(new_count), w))
                    if cursor.execute('''select * from WSLink where word = ? and sentenceId = ?''',
                                      (w, str(sentence[0]))).fetchone() is None:
                        cursor.execute('''insert into WSLink(word, sentenceId)
                                        values(?,?)''', (w, str(sentence[0])))
                cursor.close()
                conn.commit()
            sentence = sentences.fetchone()
        cursor_s.close()
        sentences.close()
        conn.commit()
        chapter += 1
        print(chapter)

    conn.close()
