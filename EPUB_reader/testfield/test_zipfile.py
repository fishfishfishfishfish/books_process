import zipfile

import utils_xml


if __name__ == "__main__":
    with zipfile.ZipFile("../datafield/A Clash of Kings - George R.R. Martin.epub") as myzip:
        with myzip.open("content/George R.R. Martin - Fire and Ice 02 - A Clash of Kings v4.0 (BD)_split_5.html") as myfile:
            print(myfile.readline())
