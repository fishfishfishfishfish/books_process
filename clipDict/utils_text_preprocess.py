import jieba
import re


def cut_sentence(text: str):
    sentence_list = re.split(r'(?<!Mr|rs)\.|!|\?|"|。|？|！|“|”', text)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    res = []
    for s in sentence_list:
        s = clean_space(s)
        if s != "" or re.fullmatch(r"[\s]+", s) is None:
            res.append(s)
    return res


def clean_space(text: str):
    """
    清理文本，去除多余的空格
    :param text: 需要清理的文本
    :return: 清理后的文本
    """
    text = re.sub(r"[\s]+", " ", text.strip())
    return text


def clean_text(text: str):
    """
    清理文本，去除无用的符号, 空格
    :param text: 需要清理的文本
    :return: 清理后的文本
    """
    text = re.sub(r"[\W]", " ", text.strip())
    text = re.sub(r"[\s]+", " ", text.strip())
    return text


def cut_words(text: str):
    """
    对文本进行分词
    :param text: 需要分词的文本
    :return: 分词后的词语列表
    """
    seg_list = jieba.cut(text)
    return " ".join(seg_list)


def lower_case(text: str):
    """
    将文本全部处理为小写
    :param text: 需要分词的文本
    :return: 小写化后的文本
    """
    return text.lower()


def strip_non_words(text: str):
    """
    将文本开头/结尾的非文字符号去掉
    :param text:
    :return:
    """
    if type(text) != str:
        return text
    text = re.sub(r"\W+$", "", text)
    text = re.sub(r"^\W+", "", text)
    return text

def combine_processor(processors: list):
    def processor(text: str):
        for tp in processors:
            text = tp(text)
        return text
    return processor


class TextProcessor:
    def __init__(self, processors: list):
        self.process = combine_processor(processors)
        self.descri_str = str(processors)


GlobalProcessor = TextProcessor([cut_words, clean_text])
