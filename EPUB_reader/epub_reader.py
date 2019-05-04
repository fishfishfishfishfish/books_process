import multiprocessing
import os
import re

import utils_text_preprocess
import utils_sql_create_table
import utils_sqlite
import utils_xml
import utils_zipfile


class EPUBReader:
    def __init__(self, filename, dest_db_name):
        self.filename = filename
        self.dest_db_name = dest_db_name

    def get_metadata(self):
        utils_sql_create_table.create_table(self.dest_db_name,
                                            utils_sql_create_table.MetaTable,
                                            "metadata")
        with utils_zipfile.zipfile_shell(self.filename, "metadata.opf") as meta_data_file:
            meta_data = utils_xml.get_metadata(meta_data_file)
        utils_sqlite.insert_many(self.dest_db_name, "metadata", meta_data)

    def get_content_list(self, content_list_loc=None, content_list_parser=None):
        """
        获取各章节名称及位置
        :param content_list_loc: 目录文件的位置
        :param content_list_parser: 用于解析保存目录的xml文件的函数, 返回list<tuple<str,str>>记录章节名以及对应位置
        :return:
        """
        utils_sql_create_table.create_table(self.dest_db_name,
                                            utils_sql_create_table.ContentListTable,
                                            "contents")
        if content_list_loc is None:
            with utils_zipfile.zipfile_shell(self.filename, "toc.ncx") as toc_file:
                content_data = utils_xml.parse_toc(toc_file)
            utils_sqlite.insert_many(self.dest_db_name, "contents", content_data,
                                     col_names=["content_name", "content_loc"])
        else:
            with utils_zipfile.zipfile_shell(self.filename, content_list_loc) as toc_file:
                content_data = content_list_parser(toc_file)
            utils_sqlite.insert_many(self.dest_db_name, "contents", content_data,
                                     col_names=["content_name", "content_loc"])

    def get_chapter_sentences(self, chapter_id, chapter_loc: str):
        chapter_filename = chapter_loc.split("#")[0]
        chapter_node_id = chapter_loc.split("#")[1]

        with utils_zipfile.zipfile_shell(self.filename, chapter_filename) as chapter_file:
            content_data = utils_xml.find_text_by_id(chapter_file, chapter_node_id)
        sentences_list = [s for s in utils_text_preprocess.cut_sentence(content_data)]
        # 分隔符加入前面的句子
        if len(sentences_list) % 2:
            sentences_list.append("")
        sentences_list = [("".join(s), ) for s in zip(sentences_list[0::2], sentences_list[1::2])]
        for sentence in sentences_list:
            if sentence[0] != "":
                while True:
                    try:
                        with utils_sqlite.sqlite_shell(self.dest_db_name) as cur:
                            cur.execute("INSERT INTO sentence (sentence) VALUES (?)", sentence)
                            cur.execute("INSERT INTO content_sentence_relation VALUES (?,?)",
                                        (chapter_id, cur.lastrowid))
                            break
                    except:
                        pass
        print("got chapter %s" % str(chapter_id))

    def get_sentences(self, workers=2):
        utils_sql_create_table.create_table(self.dest_db_name, utils_sql_create_table.SentenceTable, "sentence")
        utils_sql_create_table.create_table(self.dest_db_name, utils_sql_create_table.create_relation_table(
            cols_name=["content_id", "sentence_id"]), "content_sentence_relation")
        with utils_sqlite.sqlite_shell(self.dest_db_name) as cur:
            cur.execute("SELECT id, content_loc FROM contents;")
            content_list = cur.fetchall()
        with multiprocessing.Pool(workers) as Pool:
            for c_id, c_loc in content_list:
                Pool.apply_async(self.get_chapter_sentences, args=(c_id, c_loc))
            Pool.close()
            Pool.join()
