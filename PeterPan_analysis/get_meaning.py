import requests
import sqlite3
import random
import time
import socket
import http.client
from bs4 import BeautifulSoup


def get_content(url):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache - Control': 'max - age = 0',
        'Connection': 'keep-alive',
        'Host': 'www.iciba.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url, headers=header, timeout=timeout)
            rep.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print('3:', e)
            time.sleep(random.choice(range(8, 15)))

        except socket.error as e:
            print('4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print('6:', e)
            time.sleep(random.choice(range(5, 15)))

    return rep.text  # return html_text


def get_mean(word):
    soup = BeautifulSoup(get_content('http://www.iciba.com/' + word), "html.parser")
    body = soup.body
    try:
        contents = body.find('div', class_="screen")
        contents = contents.find('div', class_="container")
        contents = contents.find('div', class_="container-left")
        contents = contents.find('div', class_="js-base-info")
        contents = contents.find('div', class_='info-article info-base')
        contents = contents.find('div', class_='in-base')
        if contents.find('ul', class_='') is None:
            contents = contents.div.div
        else:
            contents = contents.find('ul')
    except BaseException as e:
        # print(e)
        # return 'no meaning'
        return ''
    return contents.get_text(strip=True)


if __name__ == '__main__':
    conn = sqlite3.connect('PeterPan.db')
    cursor_w = conn.cursor()
    Words = cursor_w.execute('select * from Word')
    Word = Words.fetchone()
    while Word is not None:
        print(Word[0])
        Meaning = get_mean(Word[0])
        cursor_m = conn.cursor()
        cursor_m.execute('''update Word set meaning = ? where word = ?''', (Meaning, Word[0]))
        cursor_m.close()
        conn.commit()
        Word = Words.fetchone()
    cursor_w.close()
    conn.commit()
    conn.close()
