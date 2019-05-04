import utils_text_preprocess

import pandas


def from_csv(path: str, col_index):
    res = []
    df = pandas.read_csv(path)
    for q in df.iloc[:, col_index]:
        res.append(utils_text_preprocess.strip_non_words(q))
    return res


if __name__ == "__main__":
    Querys = from_csv("datafield/A Clash of Kings_clipplings.csv", 0)
