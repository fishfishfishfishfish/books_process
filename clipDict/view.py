import threading
import pyperclip
import tkinter
import tkinter.messagebox
from tkinter import filedialog
from tkinter import ttk

import get_meaning
import utils_sqlite
import utils_sql_create_table


class TKContext:
    def __init__(self):
        self.colors = ["#E0E3DA", "#FFFFFF"]
        self.window = tkinter.Tk()
        # 数据库文件选择
        self.dest_db_name = tkinter.StringVar()
        self.dest_db_chose_btn = tkinter.Button(self.window, text="chose dest db", width=20,
                                                command=self.set_dest_db_name)
        self.dest_db_name_entry = tkinter.Entry(self.window, width=30)
        self.dest_db_confirm_btn = tkinter.Button(self.window, text="ok", width=10,
                                                  command=self.get_dest_db_name)
        # 捕获到的查询的句子
        self.last_query = ""
        self.cur_query_str = tkinter.StringVar()
        self.query_content_disp = tkinter.Text(self.window, height=2)
        # 需要查询的单词
        self.get_word_btn = tkinter.Button(self.window, text="get word", width=10, command=self.get_word)
        self.cur_query_word = tkinter.StringVar()
        self.word_disp = ttk.Label(self.window, textvariable=self.cur_query_word, width=20)
        # 单词的释义
        self.cur_meaning = tkinter.StringVar()
        self.meaning_choosing_label = ttk.Label(self.window, text="meanings: ", justify="left")
        self.meaning_choosing = ttk.Combobox(width=20, height=5, values=[], textvariable=self.cur_meaning)
        # 注释
        self.remark_disp = tkinter.Text(self.window, height=2)
        # 确认按钮
        self.result_num = tkinter.StringVar()
        self.result_num_label = ttk.Label(self.window, textvariable=self.result_num, width=20)
        self.confirm_btn = tkinter.Button(self.window, text="write to db", width=10, command=self.record_to_db)
        self.catch_btn = tkinter.Button(self.window, text="start catch", width=10,
                                        command=lambda: self.create_thread(target=self.catch_query))

    def grid_wigets(self):
        # 数据库文件选择
        self.dest_db_chose_btn.grid(row=1, column=1)
        self.dest_db_name_entry.grid(row=1, column=2, columnspan=3)
        self.dest_db_confirm_btn.grid(row=1, column=5)
        # 捕获到的查询的句子
        self.query_content_disp.grid(row=2, column=1, rowspan=2, columnspan=5)
        # 需要查询的单词
        self.word_disp.grid(row=4, column=1, columnspan=2)
        self.get_word_btn.grid(row=4, column=3)
        # 单词的释义
        self.meaning_choosing.grid(row=4, column=4, columnspan=2)
        # 注释
        self.remark_disp.grid(row=5, column=1, rowspan=2, columnspan=5)
        # 确认按钮
        self.result_num_label.grid(row=7, column=3)
        self.confirm_btn.grid(row=7, column=4)
        self.catch_btn.grid(row=7, column=5)
        self.confirm_btn["state"] = tkinter.DISABLED
        self.catch_btn["state"] = tkinter.DISABLED
        self.get_word_btn["state"] = tkinter.DISABLED

    def set_dest_db_name(self):
        self.dest_db_name_entry.delete(0, tkinter.END)
        self.dest_db_name_entry.insert(0, filedialog.askopenfilename())

    def get_dest_db_name(self):
        self.dest_db_name.set(self.dest_db_name_entry.get())
        utils_sql_create_table.create_table(self.dest_db_name.get(), utils_sql_create_table.ResultTable, "result")
        tkinter.messagebox.showinfo(title="notice", message=f"the dest db is {self.dest_db_name.get()}")
        self.dest_db_chose_btn["state"] = tkinter.DISABLED
        self.dest_db_confirm_btn["state"] = tkinter.DISABLED
        self.create_thread(target=self.catch_query)

    def record_to_db(self):
        with utils_sqlite.sqlite_shell(self.dest_db_name.get()) as cur:
            cur.execute("INSERT INTO result (word, meaning, sentence, remark) VALUES (?, ?, ?, ?);",
                        (self.cur_query_word.get(), self.cur_meaning.get(),
                         self.cur_query_str.get(), self.remark_disp.get("1.0", tkinter.END)))
            cur.execute("SELECT COUNT(*) FROM result;")
            self.result_num.set(f"there are {cur.fetchone()[0]} results")

    def before_catch(self):
        self.query_content_disp.delete("1.0", tkinter.END)
        self.cur_query_word.set("")
        self.cur_meaning.set("")
        self.window.wm_attributes('-topmost', 0)  # 窗口取消置顶
        self.confirm_btn["state"] = tkinter.DISABLED
        self.catch_btn["state"] = tkinter.DISABLED
        self.get_word_btn["state"] = tkinter.DISABLED

    def after_catch(self):
        self.confirm_btn["state"] = tkinter.NORMAL
        self.catch_btn["state"] = tkinter.NORMAL
        self.get_word_btn["state"] = tkinter.NORMAL
        self.query_content_disp.delete("1.0", tkinter.END)
        self.query_content_disp.insert("1.0", self.cur_query_str.get())

    def catch_query(self):
        self.before_catch()
        while True:
            curr = pyperclip.paste()
            if curr != self.last_query:
                self.last_query = curr
                good_curr = curr.strip()
                zh_translation = get_meaning.from_baidu(good_curr)
                self.window.wm_attributes('-topmost', 1)  # 窗口置顶
                if tkinter.messagebox.askyesno(title='catched', message=f'{good_curr}: \n{zh_translation}, \nrecord it?'):
                    self.cur_query_str.set(good_curr)
                    break
                else:
                    self.window.wm_attributes('-topmost', 0)  # 窗口取消置顶
        self.after_catch()

    # Running methods in Threads
    def create_thread(self, **kwargs):
        run_thread = threading.Thread(**kwargs)
        run_thread.setDaemon(True)
        print(run_thread)
        run_thread.start()

    def get_word(self):
        self.cur_query_word.set(self.query_content_disp.selection_get())
        self.create_thread(target=self.get_cur_meanings())
        self.cur_meaning.set("")

    def get_cur_meanings(self):
        meanings = []
        meanings.extend(get_meaning.from_youdao(self.cur_query_word.get()))
        meanings.extend(get_meaning.from_kingsoft(self.cur_query_word.get()))
        self.meaning_choosing.config(values=meanings)


if __name__ == "__main__":
    TKC = TKContext()
    TKC.grid_wigets()
    TKC.window.mainloop()
