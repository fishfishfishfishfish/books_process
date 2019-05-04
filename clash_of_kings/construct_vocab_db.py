import sqlite3

if __name__ == "__main__":
    Conn = sqlite3.connect("vocab_clash_of_kings.db")
    Cur = Conn.cursor()
    try:
        Cur.execute("CREATE TABLE BOOK_INFO ("
                    "id TEXT PRIMARY KEY NOT NULL, "
                    "asin TEXT, guid TEXT, "
                    "lang TEXT, "
                    "title TEXT, "
                    "authors TEXT);")
        Cur.execute("CREATE TABLE DICT_INFO ("
                    "id TEXT PRIMARY KEY NOT NULL, "
                    "asin TEXT, "
                    "langin TEXT, "
                    "langout TEXT);")
        Cur.execute("CREATE TABLE LOOKUPS ("
                    "id TEXT PRIMARY KEY NOT NULL, "
                    "word_key TEXT, book_key TEXT, "
                    "dict_key TEXT, "
                    "pos TEXT, "
                    "usage TEXT, "
                    "timestamp INTEGER DEFAULT 0);")
        Cur.execute("CREATE TABLE METADATA ("
                    "id TEXT PRIMARY KEY NOT NULL, "
                    "dsname TEXT, "
                    "sscnt INTEGER, "
                    "profileid TEXT);")
        Cur.execute("CREATE TABLE VERSION ("
                    "id TEXT PRIMARY KEY NOT NULL, "
                    "dsname TEXT, "
                    "value INTEGER);")
        Cur.execute("CREATE TABLE WORDS ("
                    "id TEXT PRIMARY KEY NOT NULL, "
                    "word TEXT, "
                    "stem TEXT, "
                    "lang TEXT, "
                    "category INTEGER DEFAULT 0, "
                    "timestamp INTEGER DEFAULT 0, "
                    "profileid TEXT);")
        Cur.execute("CREATE INDEX lookupbookkey ON LOOKUPS (book_key);")
        Cur.execute("CREATE INDEX lookupwordkey ON LOOKUPS (word_key);")
        Cur.execute("CREATE INDEX wordprofileid ON WORDS (profileid);")
    except BaseException as e:
        print(e)
    finally:
        Cur.close()
    Conn.commit()
