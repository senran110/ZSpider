"""
@file:logtofile.py
@time:2019/6/12-14:54
"""
import logging
import random

from constants import LOG_FILE_SAVE_PATH, LOG_DATE_FORMAT


def init_logger(verbose=1, log_name=None):
    # 1.获取日志器 暴露了应用程序代码能直接使用的接口。
    # 如果没有显式的进行创建，则默认创建一个root logger，并应用默认的日志级别(WARN)，
    logger = logging.getLogger(log_name)
    # 设置日志级别
    logger.setLevel(logging.DEBUG if verbose > 1 else logging.INFO)

    # 2.获取处理器 创建一个handler,用于写入日志文件 Formatter默认为%Y-%m-%d %H:%M:%S。
    f_handler = logging.FileHandler(LOG_FILE_SAVE_PATH, encoding='utf-8')
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # formatter = logging.Formatter(LOG_DATE_FORMAT)
    f_handler.setFormatter(formatter)  # 设置格式化器
    f_handler.setLevel(logging.DEBUG)  # 指定日志级别，低于被忽略

    # 3.将处理器添加到日志器中 为Logger实例增加一个处理器,可添加多个handler
    logger.addHandler(f_handler)

    return logger
