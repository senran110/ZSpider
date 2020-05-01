"""
@file:file_helper.py
@time:2020/2/18-21:57
"""
from http import cookiejar

import requests


def get_cookie_from_txt(filename):
    """
    将cookie解析成字典格式
    :param filename:
    :return:
    """
    session = requests.session()
    session.cookies = cookiejar.LWPCookieJar(filename)
    session.cookies.load(ignore_discard=True)
    cookie_dict = requests.utils.dict_from_cookiejar(session.cookies)
    return cookie_dict


if __name__ == '__main__':
    get_cookie_from_txt('../../cookie.txt')
