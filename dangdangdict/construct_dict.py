import sqlite3


def insert_a_word(word, description):
    conn = sqlite3.connect("asoiaf.dict")
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO dictword (word, mainword, id) VALUES"
                    "(?, ?, 0);", (word, word))
    except BaseException as e:
        print(e)

    try:
        cur.execute("SELECT last_insert_rowid()")
    except BaseException as e:
        print(e)
    word_id = cur.fetchone()[0]

    try:
        cur.execute("UPDATE dictword SET id=? WHERE word=?;", (word_id, word))
        cur.execute("INSERT INTO translation (id, content) VALUES"
                    "(?, ?);", (word_id, description))
    except BaseException as e:
        print(e)
    conn.commit()


if __name__ == "__main__":
    Conn = sqlite3.connect("asoiaf.dict")
    Cur = Conn.cursor()
    try:
        Cur.execute("CREATE TABLE dictword ("
                    "key INTEGER primary "
                    "key AUTOINCREMENT, "
                    "word varchar (128), "
                    "mainword varchar(128), "
                    "id INTEGER);")
        Cur.execute("CREATE TABLE information ("
                    "name varchar (128) primary key, "
                    "value varchar(255));")
        Cur.execute("CREATE TABLE translation ("
                    "id INTEGER primary key, "
                    "content varchar(255));")
        # Cur.execute("CREATE TABLE sqlite_sequence(name,seq);")
        Cur.execute("CREATE INDEX word_idx on dictword(word);")
    except BaseException as e:
        print(e)
    finally:
        Cur.close()
    Conn.commit()

    Cur = Conn.cursor()
    try:
        Cur.execute("INSERT INTO information (name, value) VALUES"
                    "('version', 2),"
                    "('name', 'A song of ice and fire wiki'),"
                    "('inputmethod', '中文'),"
                    "('tts', 0),"
                    "('detail', 0),"
                    "('failed', 0),"
                    "('phonitic', 0),"
                    "('pinyin', 0),"
                    "('pronounce', 1),"
                    "('picture', 0),"
                    "('example', 0),"
                    "('synonyms', 0),"
                    "('antonyms', 0);")
    except BaseException as e:
        print(e)
    finally:
        Cur.close()
    Conn.commit()

