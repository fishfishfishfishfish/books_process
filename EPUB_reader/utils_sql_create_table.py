import utils_sqlite

MetaTable = "CREATE TABLE %s (" \
            "name TEXT," \
            "value TEXT," \
            "PRIMARY KEY (name, value)" \
            ");"

ContentListTable = "CREATE TABLE %s (" \
                    "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                    "content_name TEXT," \
                    "content_loc TEXT" \
                    ");"

SentenceTable = "CREATE TABLE %s (" \
                "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "sentence TEXT" \
                ");"


def create_table(db_name: str, create_sql: str, table_name=None):
    try:
        with utils_sqlite.sqlite_shell(db_name) as cur:
            if table_name is not None:
                cur.execute(create_sql % (table_name, ))
            else:
                cur.execute(create_sql)
    except BaseException as e:
        if table_name is not None:
            print("error %s at %s" % (str(e), table_name))
        else:
            print("error %s at %s" % (str(e), create_sql))


def create_relation_table(num_relation=2, cols_name=None):
    if cols_name is None:
        cols_name = ["entity" + str(i) for i in range(num_relation)]
    sql = "CREATE TABLE %s ("
    sql += cols_name[0] + " INTEGER"
    for cname in cols_name[1:]:
        sql += ", " + cname + " INTEGER"
    sql += ");"
    return sql
