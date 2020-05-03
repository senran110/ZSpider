import random

import execjs
import math

headers = {
    'Referer': 'https://www.yunpian.com/product-captcha.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
}


def _reload_js():
    """
    加载 js
    :return:
    """
    with open('yp_slider.js', 'rb') as f:
        js = f.read().decode()
    ctx = execjs.compile(js)
    return ctx


def _get_cb(ctx):
    """
    生成 cb 参数
    :param ctx:
    :return:
    """
    return ctx.call('get_cb')


def _encrypt_data(ctx, data):
    """
    js 加密, 生成 i, k 参数, 其中 i 参数为 AES 加密, k 参数为 RSA 加密
    :param ctx:
    :param data:
    :return:
    """
    return ctx.call('data_encrypt', data)


def _generate_trace_js(ctx, distance):
    """
    生成轨迹
    :param ctx:
    :param distance:
    :return:
    """
    return ctx.call('get_trace', distance)


def RandomNum(min_value, max_value):
    return math.floor(random.random() * (max_value - min_value)) + min_value + 1
