#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import collections
import re
import sqlite3

if __name__ == '__main__':
    punk = r'[\s\d!！?？.,"“”‘’：:;；\[\]()—\^*…]'  # 标点符号
    # 连接数据库
    conn = sqlite3.connect('AmericanGods.db')
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

    chapters = ['1-SOMEWHERE IN AMERICA', '1', '10', '11-Coming to America', '11', '12-INTERLUDE 2', '12-INTERLUDE 3', '12-INTERLUDE', '12', '13-COMING TO AMERICA', '13', '14', '15', '16', '17', '18', '19', '2', '20-POSTSCRIPT', '20', '3-Coming To America', '3', '4-Coming To America', '4', '5', '6', '7-SOMEWHERE IN AMERICA', '7', '8', '9-MEANWHILE. A CONVERSATION', '9']
    for chapter in chapters:
        cursor_s = conn.cursor()
        sentences = cursor_s.execute('select * from Sentence where chapter = ?', (chapter,))
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
        print(chapter)

    conn.close()
