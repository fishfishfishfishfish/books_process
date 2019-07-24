# !/usr/bin/env Python3

import tkinter as tk
from threading import Thread
from time import sleep
from tkinter import ttk


class App:
    def __init__(self):
        # Create instance
        self.win = tk.Tk()
        # Add title
        self.win.title("Python GUI")
        # Adding a Button
        self.action = ttk.Button(self.win, text='Click Me!', command=self.click_me)
        # Adding a Label
        self.label_str = tk.StringVar()
        self.label = ttk.Label(self.win, textvariable=self.label_str)

    def method_in_a_thread(self, num_of_loops=10):
        while True:
            curr = pyperclip.paste()
            if curr != last_query:
                good_curr = curr.strip()
                q.put(good_curr)
                break

    def click_me(self):
        self.action.configure(text='Hello')
        self.create_thread()

    def grid_widgets(self):
        self.action.grid(column=1, row=1)
        self.label.grid(column=1, row=2)

    # Running methods in Threads
    def create_thread(self):
        run_thread = Thread(target=self.method_in_a_thread, args=[2])
        print(run_thread)
        run_thread.start()


app = App()
app.grid_widgets()
app.win.mainloop()
