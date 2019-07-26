import pickle
import sqlite3
import utils_log


class sqlite_shell:
    def __init__(self, db_name, function=None, aggregate=None):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        if function is not None:
            self.conn.create_function(function.name, function.num_param, function.run)
        if aggregate is not None:
            self.conn.create_aggregate(aggregate().name, aggregate().num_param, aggregate)

    def __enter__(self):
        return self.cur

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.cur.close()
        if exc_tb is None:
            self.conn.commit()
        else:
            utils_log.get_logger(__name__).log(40, exc_value)


def sqlite_pickle_dump(obj):
    return sqlite3.Binary(pickle.dumps(obj))


def insert_many(db_name, tb_name, tuples: list, col_names=None):
    try:
        tuple_size = len(tuples[0])
        sql = "INSERT INTO %s" % (tb_name, )
        if col_names is not None:
            sql += " (" + col_names[0]
            for cname in col_names[1:]:
                sql += ", " + cname
            sql += ")"
        sql += " VALUES (?"
        for i in range(tuple_size-1):
            sql += ", ?"
        sql += ");"
        with sqlite_shell(db_name) as cur:
            cur.executemany(sql, tuples)
    except BaseException as e:
        raise e

