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
        self.note_file_name = tkinter.StringVar()
        # 选取文件路径
        self.db_chose_btn = tkinter.Button(self.window, text="chose book info db", command=self.get_db_name)
        self.note_chose_btn = tkinter.Button(self.window, text="chose note file", command=self.get_note_file_name)
        self.db_name_label = ttk.Label(self.window, textvariable=self.db_name,
                                       justify="left",  # 文本对齐方式
                                       background="white",  # 背景颜色
                                       relief="sunken",  # 边框形式: raised, sunken, flat, groove, ridge
                                       )
        self.note_file_label = ttk.Label(self.window, textvariable=self.note_file_name,
                                         justify="left", background="white", relief="sunken")
        # 图书内容列表
        self.content_tree_view = ttk.Treeview(self.window, columns=["1", "2"], show="headings",
                                              selectmode="browse", height=28)
        self.content_vbar = ttk.Scrollbar(self.window, orient=tkinter.VERTICAL, command=self.content_tree_view.yview)
        # 笔记列表
        self.note_tree_view = ttk.Treeview(self.window, columns=["1", "2", "3", "4"], show="headings",
                                           selectmode="browse", height=28)
        self.note_vbar = ttk.Scrollbar(self.window, orient=tkinter.VERTICAL, command=self.note_tree_view.yview)

    def config_wigets(self):
        # 图书内容列表
        self.content_tree_view.column("1", width=500, anchor="w")
        self.content_tree_view.column("2", width=100, anchor="w")
        self.content_tree_view.heading('1', text='sentence')
        self.content_tree_view.heading('2', text='chapter')
        self.content_tree_view.tag_configure("type0", foreground="black", background=self.colors[0])
        self.content_tree_view.tag_configure("type1", foreground="black", background=self.colors[1])
        self.content_tree_view.configure(yscrollcommand=self.content_vbar.set)
        # 笔记列表
        self.note_tree_view.column("1", width=100, anchor="w")
        self.note_tree_view.column("2", width=100, anchor="w")
        self.note_tree_view.column("3", width=100, anchor="w")
        self.note_tree_view.column("4", width=100, anchor="w")
        self.note_tree_view.heading('1', text='highlighted')
        self.note_tree_view.heading('2', text='note')
        self.note_tree_view.heading('3', text='meanings')
        self.note_tree_view.heading('4', text='examples')
        self.note_tree_view.tag_configure("type0", foreground="black", background=self.colors[0])
        self.note_tree_view.tag_configure("type1", foreground="black", background=self.colors[1])
        self.note_tree_view.configure(yscrollcommand=self.note_vbar.set)

    def grid_wigets(self):
        # 选取文件路径
        self.db_chose_btn.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.db_name_label.grid(row=1, column=2, columnspan=10, padx=10, pady=10, sticky="ew")
        self.note_chose_btn.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.note_file_label.grid(row=2, column=2, columnspan=10, padx=10, pady=10, sticky="ew")
        # 图书内容列表
        self.content_tree_view.grid(row=3, column=1, columnspan=6, pady=10, sticky="e")
        self.content_vbar.grid(row=3, column=7, pady=10, sticky="nsw")
        # 笔记列表
        self.note_tree_view.grid(row=3, column=8, columnspan=4, pady=10, sticky="e")
        self.note_vbar.grid(row=3, column=12, pady=10, sticky="nsw")

    def get_db_name(self):
        self.db_name.set(filedialog.askopenfilename())
        self.get_book_content()

    def get_note_file_name(self):
        self.note_file_name.set(filedialog.askopenfilename())
        self.get_note_list()

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

    def get_note_list(self):
        for item in self.note_tree_view.get_children():
            self.note_tree_view.delete(item)
        queries = get_querys.from_csv(self.note_file_name.get(), ["内容▲", "位置"], index=True)
        for item in queries:
            self.note_tree_view.insert("", "end", values=[item[1], item[2], "", ""],
                                       iid=item[0], tags=[f"type{item[0]%2}"])


if __name__ == "__main__":
    TKC = TKContext()
    TKC.config_wigets()
    TKC.grid_wigets()
    TKC.window.mainloop()
