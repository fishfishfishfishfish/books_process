import sqlite3
import lxml

if __name__ == "__main__":
    Conn = sqlite3.connect("book_clash_of_kings.db")
    Cur = Conn.cursor()
    try:
        Cur.execute("CREATE TABLE CHAPTER ("
                    "id INTEGER PRIMARY KEY NOT NULL, "
                    "name TEXT NOT NULL);")
        Cur.execute("CREATE TABLE SENTENCE ("
                    "id TEXT PRIMARY KEY NOT NULL, "
                    "content TEXT, "
                    "chapter_id INTEGER);")
    except BaseException as e:
        print(e)
    finally:
        Cur.close()
    Conn.commit()
