import utils_text_preprocess

import pandas


def from_csv(path: str, col_index, sort_key_col=None, index=False):
    res = []
    df = pandas.read_csv(path)
    if sort_key_col is not None:
        # 对查询先进行排序
        # 若使用列的编号来指定排序的列
        if type(sort_key_col) == list and type(sort_key_col[0]) == int:
            sort_key_col = [df.columns[k] for k in sort_key_col]
        elif type(sort_key_col) == int:
            sort_key_col = df.columns[sort_key_col]
        df.sort_values(by=sort_key_col)

    if type(col_index) == list:
        # 选取多个列的内容
        if type(col_index[0]) == int:  # 按序号选取
            for q in df.iloc[:, col_index].itertuples(index=index):
                res.append(tuple(utils_text_preprocess.strip_non_words(i) for i in q))
        elif type(col_index[0]) == str:  # 按列名选取
            for q in df[col_index].itertuples(index=index):
                res.append(tuple(utils_text_preprocess.strip_non_words(i) for i in q))
    else:
        if type(col_index) == int:  # 按序号选取
            for q in df.iloc[:, col_index]:
                res.append(utils_text_preprocess.strip_non_words(q))
        elif type(col_index) == str:  # 按列名选取
            for q in df[col_index]:
                res.append(utils_text_preprocess.strip_non_words(q))
    return res


def dangdang_to_csv(dangdang_path: str, csv_path: str):
    res_dict = {"highlight": [], "note": []}
    with open(dangdang_path, encoding="UTF-8") as f:
        line = f.readline()
        while line:
            res_dict["highlight"].append(line.strip())
            line = f.readline()
            res_dict["note"].append(line[6:].strip())
            line = f.readline()
    res = pandas.DataFrame(res_dict)
    res.to_csv(csv_path, index=False)


if __name__ == "__main__":
    # Queries1 = from_csv("datafield/A Clash of Kings_clipplings.csv", [0, 3], sort_key_col=3)
    # Queries2 = from_csv("datafield/A Clash of Kings_clipplings.csv", ["内容▲", "位置", "日期"], sort_key_col=["位置", "日期"])
    DangPath = "datafield/dangdang_user_Download_A Storm of Swords - George R_ R_ Martin_mobi_.txt"
    CsvPath = "datafield/A Storm of Swords - George R_ R_ Martin_mobi_clip.csv"
    dangdang_to_csv(DangPath, CsvPath)
