import threading
import pyperclip
import tkinter
from tkinter import ttk

import get_meaning


class TKContext:
    def __init__(self):
        self.colors = ["#E0E3DA", "#FFFFFF"]
        self.window = tkinter.Tk()
        self.last_query = ""
        self.cur_query_str = tkinter.StringVar()
        self.query_label = ttk.Label(self.window, textvariable=self.cur_query_str,
                                     width=50, justify="left",  # 文本对齐方式
                                     background="white",  # 背景颜色
                                     )
        self.confirm_btn = tkinter.Button(self.window, text="start catch", command=self.create_thread)

    def grid_wigets(self):
        self.query_label.grid(row=1, column=1, columnspan=5)
        self.confirm_btn.grid(row=2, column=1)

    def catch_query(self):
        self.confirm_btn["state"] = tkinter.DISABLED
        while True:
            curr = pyperclip.paste()
            if curr != self.last_query:
                self.last_query = curr
                good_curr = curr.strip()
                self.cur_query_str.set(good_curr)
                break
        self.confirm_btn["state"] = tkinter.NORMAL

    # Running methods in Threads
    def create_thread(self):
        run_thread = threading.Thread(target=self.catch_query)
        print(run_thread)
        run_thread.start()


if __name__ == "__main__":
    TKC = TKContext()
    TKC.grid_wigets()
    TKC.window.mainloop()
