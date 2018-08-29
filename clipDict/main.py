import get_meaning
import pyperclip
import time
import os

fname = time.strftime("%Y-%m-%d", time.localtime()) + ".log"
f = open(fname, 'a')
last=pyperclip.paste()
while True:
    curr=pyperclip.paste()
    if curr != last:
        good_curr = curr.strip()
        print(good_curr)
        Meaning = get_meaning.get_mean(good_curr)
        print(Meaning)
        f.write(good_curr + "\t" + Meaning + "\t\n")
        last = curr
    time.sleep(1)
