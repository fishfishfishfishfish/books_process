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
        self.cur_highlight = tkinter.StringVar()
        self.cur_highlight_id = 1
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
        self.highlight_label = ttk.Label(self.window, textvariable=self.cur_highlight, justify="left", background="white")
        self.last_highlight_btn = tkinter.Button(self.window, text="last highlight", command=self.last_highlight)
        self.next_highlight_btn = tkinter.Button(self.window, text="next highlight", command=self.next_highlight)

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
        self.highlight_label.grid(row=3, column=9, columnspan=2, pady=10, sticky="w")
        self.last_highlight_btn.grid(row=4, column=9, pady=5, sticky="w")
        self.next_highlight_btn.grid(row=4, column=10, pady=5)

    def get_db_name(self):
        self.db_name.set(filedialog.askopenfilename())
        self.get_book_content()
        self.cur_highlight.set(self.get_cur_highlight()[1])
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

    def get_cur_highlight(self):
        with utils_sqlite.sqlite_shell(self.db_name.get()) as cur:
            cur.execute(f"""
                        SELECT id, highlight FROM highlight where id = {self.cur_highlight_id};
                        """)
            return cur.fetchone()

    def last_highlight(self):
        self.cur_highlight_id = self.cur_highlight_id - 1 if self.cur_highlight_id > 1 else 1
        self.cur_highlight.set(self.get_cur_highlight()[1])
        self.cur_sentence_ids = self.get_cur_related_sentences()
        self.mark_cur_sentence()

    def next_highlight(self):
        self.cur_highlight_id = self.cur_highlight_id + 1
        if self.get_cur_highlight() is None:
            self.cur_highlight_id = self.cur_highlight_id - 1
        self.cur_highlight.set(self.get_cur_highlight()[1])
        self.cur_sentence_ids = self.get_cur_related_sentences()
        self.mark_cur_sentence()

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

    def mark_cur_sentence(self):
        self.content_tree_view.selection_set(self.cur_sentence_ids[self.cur_sentence_id_idx])
        self.content_tree_view.see(self.cur_sentence_ids[self.cur_sentence_id_idx])


if __name__ == "__main__":
    TKC = TKContext()
    TKC.config_wigets()
    TKC.grid_wigets()
    TKC.window.mainloop()
