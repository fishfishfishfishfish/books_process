import utils_sql_create_table
import utils_sqlite
import utils_log
import get_querys
import get_meaning
import pandas


class NoteReader:
    def __init__(self, filename, dest_db_name):
        self.filename = filename
        self.dest_db_name = dest_db_name

    def get_hightlight(self):
        utils_sql_create_table.create_table(self.dest_db_name,
                                            utils_sql_create_table.HighLightTable,
                                            "highlight")
        notes = get_querys.from_csv(self.filename, [0, 1])
        for n in notes:
            try:
                print(n)
                with utils_sqlite.sqlite_shell(self.dest_db_name) as cur:
                    cur.execute("INSERT INTO highlight (highlight, note) VALUES (?, ?);", n)
            except:
                pass

    def get_meaning(self):
        utils_sql_create_table.create_table(self.dest_db_name,
                                            utils_sql_create_table.MeaningTable,
                                            "meaning")
        utils_sql_create_table.create_table(self.dest_db_name,
                                            utils_sql_create_table.create_relation_table(
                                                cols_name=["highlight_id", "meaning_id"]),
                                            "highlight_meaning_relation")
        with utils_sqlite.sqlite_shell(self.dest_db_name) as cur:
            cur.execute("SELECT id, highlight from highlight;")
            highlights = cur.fetchall()
        for h in highlights:
            print(h[1])
            try:
                meanings = get_meaning.from_youdao(h[1])
                meanings.extend(get_meaning.from_kingsoft(h[1]))
                for m in meanings:
                    print("\t", m)
                    with utils_sqlite.sqlite_shell(self.dest_db_name) as cur:
                        cur.execute("INSERT INTO meaning (meaning) VALUES (?)", (m,))
                        cur.execute("INSERT INTO highlight_meaning_relation VALUES (?,?)",
                                    (h[0], cur.lastrowid))
            except BaseException as e:
                utils_log.get_logger(__name__).log(utils_log.ERROR,
                                                   f"{h[1]}\n{str(e)}")
