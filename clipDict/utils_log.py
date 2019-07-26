import logging
import os

LOGNAME = "my_log"
INFO = logging.INFO
ERROR = logging.ERROR
DEBUG = logging.DEBUG


# 配置日志输出，方便debug
def initial_logger(log_name=LOGNAME):
    if not os.path.exists("./log/"):
        os.mkdir("./log/")
    log_file = "./log/{}.log".format(log_name)
    log_level = logging.DEBUG
    # 创建日志
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)
    # 日志格式的设置
    formatter = logging.Formatter("[%(levelname)s][%(funcName)s][%(asctime)s]%(message)s")
    # 输出到文件的日志
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    # 输出到控制台的日志
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    # 添加输出到文件和控制台的日志处理器
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


def get_logger(log_name=LOGNAME):
    return logging.getLogger(log_name)
