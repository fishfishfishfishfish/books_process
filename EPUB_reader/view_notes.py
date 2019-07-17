import re
import tkinter
from tkinter import ttk
from tkinter import filedialog

import utils_sqlite
import get_querys


class TKContext:
    def __init__(self):
        self.colors = ["#E0E3DA", "#FFFFFF"]
        self.window = tkinter.Tk()
        self.db_name = tkinter.StringVar()
        # 标记的相关记录数据
        self.highlight_num = 0
        self.cur_highlight_id = 1
        self.cur_highlight = tkinter.StringVar()
        self.cur_highlight_id_str = tkinter.StringVar()
        # 与标记相关句子相关的记录数据
        self.cur_sentence_id_str = tkinter.StringVar()
        self.cur_sentence_ids = []
        self.cur_sentence_id_idx = 0  # 当前句子在cur_sentence_ids中的序号
        # 选取文件路径
        self.db_chose_btn = tkinter.Button(self.window, text="chose db", command=self.get_db_name)
        self.db_name_label = ttk.Label(self.window, textvariable=self.db_name,
                                       justify="left",  # 文本对齐方式
                                       background="white",  # 背景颜色
                                       relief="sunken",  # 边框形式: raised, sunken, flat, groove, ridge
                                       )
        # 图书内容列表
        self.content_tree_view = ttk.Treeview(self.window, columns=["1", "2"], show="headings",
                                              selectmode="browse", height=28)
        self.content_vbar = ttk.Scrollbar(self.window, orient=tkinter.VERTICAL, command=self.content_tree_view.yview)
        # 显示当前标记
        self.highlight_num_label = ttk.Label(self.window, textvariable=self.cur_highlight_id_str,
                                             justify="left", width=10, background="white")
        self.highlight_label = ttk.Label(self.window, textvariable=self.cur_highlight,
                                         justify="left", width=20, background="white")
        self.last_highlight_btn = tkinter.Button(self.window, text="last highlight", command=self.last_highlight)
        self.next_highlight_btn = tkinter.Button(self.window, text="next highlight", command=self.next_highlight)
        # 控制选中的句子
        self.sentence_num_label = ttk.Label(self.window, textvariable=self.cur_sentence_id_str,
                                            justify="left", width=10, background="white")
        self.last_sentence_btn = tkinter.Button(self.window, text="last sentence", command=self.last_sentence)
        self.next_sentence_btn = tkinter.Button(self.window, text="next sentence", command=self.next_sentence)

    def config_wigets(self):
        # 图书内容列表
        self.content_tree_view.column("1", width=500, anchor="w")
        self.content_tree_view.column("2", width=100, anchor="w")
        self.content_tree_view.heading('1', text='sentence')
        self.content_tree_view.heading('2', text='chapter')
        self.content_tree_view.tag_configure("type0", foreground="black", background=self.colors[0])
        self.content_tree_view.tag_configure("type1", foreground="black", background=self.colors[1])
        self.content_tree_view.configure(yscrollcommand=self.content_vbar.set)

    def grid_wigets(self):
        # 选取文件路径
        self.db_chose_btn.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.db_name_label.grid(row=1, column=2, columnspan=10, padx=10, pady=10, sticky="ew")
        # 图书内容列表
        self.content_tree_view.grid(row=3, column=1, columnspan=6, rowspan=50, pady=10, sticky="e")
        self.content_vbar.grid(row=3, column=7, pady=10, rowspan=50, sticky="nsw")
        # 显示当前标记
        self.highlight_num_label.grid(row=3, column=9, pady=10, sticky="w")
        self.highlight_label.grid(row=3, column=10, columnspan=3, pady=10, sticky="w")
        self.last_highlight_btn.grid(row=4, column=9, pady=5, sticky="w")
        self.next_highlight_btn.grid(row=4, column=10, pady=5)
        # 控制当前选中句子
        self.sentence_num_label.grid(row=5, column=11, pady=10, sticky="w")
        self.last_sentence_btn.grid(row=5, column=9, pady=5, sticky="w")
        self.next_sentence_btn.grid(row=5, column=10, pady=5)

    def get_db_name(self):
        self.db_name.set(filedialog.askopenfilename())
        self.get_book_content()
        self.cur_highlight.set(self.get_cur_highlight())
        self.highlight_num = self.get_highlight_num()
        self.cur_highlight_id_str.set(f"{self.cur_highlight_id}/{self.highlight_num}")
        self.cur_sentence_ids = self.get_cur_related_sentences()
        self.mark_cur_sentence()

    def get_book_content(self):
        for item in self.content_tree_view.get_children():
            self.content_tree_view.delete(item)
        with utils_sqlite.sqlite_shell(self.db_name.get()) as cur:
            cur.execute("""
                        SELECT sentence.id, sentence.sentence, contents.content_name FROM
                        (contents INNER JOIN content_sentence_relation ON 
                            content_sentence_relation.content_id=contents.id)
                        INNER JOIN sentence ON sentence.id = content_sentence_relation.sentence_id
                        ORDER BY contents.id, sentence.id;
                        """)
            tag = 0
            for item in cur:
                self.content_tree_view.insert("", "end", values=[item[1], item[2]], iid=item[0], tags=[f"type{tag}"])
                tag = (tag + 1) % 2

    def get_highlight_num(self):
        with utils_sqlite.sqlite_shell(self.db_name.get()) as cur:
            cur.execute(f"""
                        SELECT COUNT(*) FROM highlight;
                        """)
            return cur.fetchone()[0]

    def get_cur_highlight(self):
        with utils_sqlite.sqlite_shell(self.db_name.get()) as cur:
            cur.execute(f"""
                        SELECT highlight FROM highlight where id = {self.cur_highlight_id};
                        """)
            return cur.fetchone()[0]

    def change_highlight(self):
        self.cur_highlight.set(self.get_cur_highlight())
        self.cur_highlight_id_str.set(f"{self.cur_highlight_id}/{self.highlight_num}")
        self.cur_sentence_ids = self.get_cur_related_sentences()
        self.mark_cur_sentence()

    def last_highlight(self):
        self.cur_highlight_id = (self.cur_highlight_id - 1) % self.highlight_num + 1
        print(self.cur_highlight_id)
        self.change_highlight()

    def next_highlight(self):
        self.cur_highlight_id = (self.cur_highlight_id + 1) % self.highlight_num + 1
        print(self.cur_highlight_id)
        self.change_highlight()

    def get_cur_related_sentences(self):
        self.cur_sentence_id_idx = 0
        res = []
        with utils_sqlite.sqlite_shell(self.db_name.get()) as cur:
            cur.execute(f"""
                        select id from sentence where sentence like "% {self.cur_highlight.get()} %" 
                                or sentence like "{self.cur_highlight.get()} %"
                                or sentence like "% {self.cur_highlight.get()}";
                        """)
            res = [s[0] for s in cur]
            if len(res) == 0:
                cur.execute(f"""
                            select id from sentence where sentence like "%{self.cur_highlight.get()}%" ;
                            """)
                res = [s[0] for s in cur]
            return res

    def last_sentence(self):
        self.cur_sentence_id_idx = (self.cur_sentence_id_idx - 1) % len(self.cur_sentence_ids)
        self.cur_sentence_id_str.set(f"{self.cur_sentence_id_idx}/{len(self.cur_sentence_ids)}")
        self.mark_cur_sentence()

    def next_sentence(self):
        self.cur_sentence_id_idx = (self.cur_sentence_id_idx + 1) % len(self.cur_sentence_ids)
        self.cur_sentence_id_str.set(f"{self.cur_sentence_id_idx}/{len(self.cur_sentence_ids)}")
        self.mark_cur_sentence()

    def mark_cur_sentence(self):
        self.content_tree_view.selection_set(self.cur_sentence_ids[self.cur_sentence_id_idx])
        self.content_tree_view.see(self.cur_sentence_ids[self.cur_sentence_id_idx])


if __name__ == "__main__":
    TKC = TKContext()
    TKC.config_wigets()
    TKC.grid_wigets()
    TKC.window.mainloop()
