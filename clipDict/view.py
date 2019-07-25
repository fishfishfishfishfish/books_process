import threading
import pyperclip
import tkinter
import tkinter.messagebox
from tkinter import ttk

import get_meaning


class TKContext:
    def __init__(self):
        self.colors = ["#E0E3DA", "#FFFFFF"]
        self.window = tkinter.Tk()
        self.last_query = ""
        self.cur_query_str = tkinter.StringVar()
        self.query_content_disp = tkinter.Text(self.window, height=5)
        self.cur_query_word = tkinter.StringVar()
        self.word_disp = ttk.Label(self.window, textvariable=self.cur_query_word, width=30)
        self.cur_meaning = tkinter.StringVar()
        self.meaning_choosing_label = ttk.Label(self.window, text="meanings: ", justify="left")
        self.meaning_choosing = ttk.Combobox(width=30, height=5, values=[], textvariable=self.cur_meaning)
        self.confirm_btn = tkinter.Button(self.window, text="start catch", command=self.create_thread)
        self.get_word_btn = tkinter.Button(self.window, text="get word", command=self.get_word)

    def grid_wigets(self):
        self.query_content_disp.grid(row=1, column=1, columnspan=3)
        self.get_word_btn.grid(row=2, column=2)
        self.word_disp.grid(row=3, column=1)
        self.meaning_choosing.grid(row=3, column=2)
        self.confirm_btn.grid(row=4, column=2)
        self.create_thread()

    def before_catch(self):
        self.confirm_btn["state"] = tkinter.DISABLED
        self.get_word_btn["state"] = tkinter.DISABLED

    def after_catch(self):
        self.confirm_btn["state"] = tkinter.NORMAL
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
                if tkinter.messagebox.askyesno(title='catched', message=f'{good_curr}, record it?'):
                    self.cur_query_str.set(good_curr)
                    break
        self.after_catch()

    # Running methods in Threads
    def create_thread(self):
        run_thread = threading.Thread(target=self.catch_query)
        print(run_thread)
        run_thread.start()

    def get_word(self):
        self.cur_query_word.set(self.query_content_disp.selection_get())
        self.meaning_choosing.config(values=self.get_cur_meanings())

    def get_cur_meanings(self):
        return get_meaning.from_youdao(self.cur_query_word.get())


if __name__ == "__main__":
    TKC = TKContext()
    TKC.grid_wigets()
    TKC.window.mainloop()
