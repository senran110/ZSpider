import codecs
import io
import json
import random
import re
import time
from pprint import pprint

import requests
from fontTools.ttLib import TTFont
from pymongo import MongoClient
from requests.adapters import HTTPAdapter

from scrapy import Selector
from bs4 import BeautifulSoup as bs, Tag
from fake_useragent import UserAgent
from selenium import webdriver

from constants import *
from decrypt import _decrypt_text_tag, _decrypt_textPath_tag, _decrypt_woff_tag
from fontcache import Cache
from logtofile import init_logger

# 调用UserAgent类生成ua实例

from proxy import proxies
from word import dictionary, woffs

ua = UserAgent(verify_ssl=False)


class DpFont:
    def __init__(self, dp_name):
        self.DpLogger = init_logger(log_name=dp_name)

        # Mongo初始化
        self.client = MongoClient('localhost', 27017)
        self.collection = self.client['dianping']['shop']

        self.session = requests.session()
        self.session.mount('http://', HTTPAdapter(max_retries=3))
        self.session.mount('https://', HTTPAdapter(max_retries=3))
        # 暂存字体对映的字典
        # self.my_font_dict = dict()
        self.font_cache = Cache()
        print("init success")

    def parse_url(self, url, headers=None):
        """
        解析页面
        :param url: 请求链接
        :param headers: 请求头
        :return: response
        """
        if headers:
            headers['User-Agent'] = ua.random
            # todo 将阿布云代理换成自己的才可使用或者设为None表示不用隧道
            proxie = None

            response = self.session.get(url, headers=headers, proxies=proxie, timeout=5)

            if response.history and response.history[0].status_code == 302:
                # 将重定向链接写入日志
                print("redirect verifyCode")
                self.DpLogger.warning("verifyCode：%s", response.url)

                return None

            return response
        else:
            # 请求CSS文件时,不可携带session里的cookie
            css_resp = requests.get(url, headers=CSS_HEADERS)
            return css_resp

    def get_css(self, html):
        """
        提取svg_css链接
        :param html: 列表页html
        :return: CSS文件内容
        """
        # re.M多行模式
        # In [6]: re.findall(r"\w+$",s,re.M)
        # Out[6]: ['boy', 'girl'] 若去掉则只匹配girl
        svg_text_css = re.search(PATTERN_SVG_CSS, html, re.M)

        if not svg_text_css:
            raise Exception("cannot find svg_text_css file")
        else:
            css_url = svg_text_css.group(1)
            content = self.parse_url(CSS_URL_PREFIX + css_url)
            return content

    @staticmethod
    def parse_shop_css(css):
        """
        解析CSS文件
        :param self:
        :param css: CSS文件内容
        :return:(sjipiv,x,y)
        """
        # 偏移量字典存储,svg的url dict储存
        css_px_dict, svg_url_dict = dict(), dict()

        FONT_URLS = re.findall(PATTERN_FONT_NAME, css, re.S)
        font_dict = dict(FONT_URLS)
        # r'.(.*?){background:(.*?)px(.*?)px;}' (sjipiv,x,y)
        css_px = re.findall(PATTERN_BACKGROUND, css)
        # 单个字体的偏移
        if not css_px:
            # raise Exception("not find css px")
            print("not find svg information")
        else:
            for i in css_px:
                css_px_dict[i[0]] = {
                    'x': -int(i[1].strip()),
                    'y': -int(i[-1].strip()),
                }

            # r'\[class\^="(.+?)"\]{width:(.+?)px;.+?url\((.+?)\)' ('dmc','12','xx.svg') 名称 字宽 文件
            svg_urls = re.findall(PATTERN_SPAN_CLASS, css)
            if not svg_urls:
                raise Exception("cannot find svg file")
            else:
                for i in svg_urls:
                    svg_url_dict.update({i[0]: [int(i[1].strip()), PAGE_PREFIX + i[2]]})

        return css_px_dict, svg_url_dict, font_dict

    def decrypt(self, address_tag_soup, svg_url_dict, css_px_dict, font_dict):
        """
        获取标签里包含的子节点，判断子节点是否为纯文本若不是判断应用何种方式，采取相应方式解决
        :param address_tag_soup:
        :param svg_url_dict:
        :param css_px_dict:
        :param font_dict:
        :return:
        """
        # 获取该节点下的所有直接子节点
        contents = address_tag_soup.contents

        text = ""
        while contents:
            methods = 0
            node = contents.pop(0)
            # 判断该标签是否为标签，若为文字则直接追加
            if isinstance(node, Tag):
                # 标签名为列表中的几项视为加密标签，否则直接提取文本
                if node.name in DECRYPT_TAGS and node['class'][0] not in IGNORED_SPAN_CLASS:
                    # 判断标签的类及对应的方式method 1 svg / 0 自定义字体
                    for svg_name in svg_url_dict.keys():
                        if node['class'][0].startswith(svg_name):
                            methods = 1
                            break

                    node_text = self.get_decrypted(node, svg_url_dict, css_px_dict, font_dict, methods)
                    text += node_text
                else:
                    # 标签里面的直接文本或单标签无文本
                    if node.string is None:
                        node.string = ''
                    text += node.string

            elif not isinstance(node, str):
                continue

            else:
                # 无外标签的文字
                text += node

        return text.strip()

    def get_decrypted(self, node, svg_url_dict, css_px_dict, font_dict, methods):
        """
        :param node: 要解析的节点
        :param svg_url_dict: 略
        :param css_px_dict: 略
        :param methods:1 自定义字体/0 svg格式
        :return:
        """
        if not methods:
            new_dict = dict()
            unitext = node.get_text().encode('raw_unicode_escape').replace(b'\u', b'').decode()
            font_class = node.get('class')[0]
            postfix_name, target_font_url = "", ""

            # 以字体名的形式存储/
            for font_family, font_url in font_dict.items():
                if font_class in font_family:
                    # 1、获取链接中文件名
                    postfix_name = font_url[font_url.rfind('/') + 1: -5]
                    target_font_url = font_url
                    break

            if not target_font_url:
                print("没有与之对应的字体文件")
                raise

            if self.font_cache.check_hash(postfix_name):
                new_dict = json.loads(self.font_cache.get_hash(postfix_name))
            else:
                byte_font = requests.get(CSS_URL_PREFIX + target_font_url).content
                # 将二进制文件当做文件操作
                new_font = TTFont(io.BytesIO(byte_font))
                uni_list = new_font['cmap'].tables[0].ttFont.getGlyphOrder()[2:]  # 取出字形保存到uniList中
                new_dict = dict(zip(uni_list, woffs))
                json_data = json.dumps(new_dict, ensure_ascii=False)
                # 存到redis中
                self.font_cache.add_hash(postfix_name, json_data)

            text = _decrypt_woff_tag(unitext, new_dict)
            # print("text:", text)
        else:
            font_size, svg_url = None, None

            # 1、根据CSS的名称获取偏移量
            css_class = node['class'][0]

            x_offset, y_offset = css_px_dict[css_class]['x'], css_px_dict[css_class]['y']

            # 2、获取字宽请求svg链接，判断textPath是否存在确定种类
            for svg_name in svg_url_dict.keys():
                if css_class.startswith(svg_name):
                    font_size = svg_url_dict[svg_name][0]
                    svg_url = svg_url_dict[svg_name][1]
                    break

            svg_content = self.parse_url(svg_url).text
            # 3、解析获取真实的文字
            if "textPath" in svg_content:
                text = _decrypt_textPath_tag(svg_content, font_size, x_offset, y_offset)
            else:
                text = _decrypt_text_tag(svg_content, font_size, x_offset, y_offset)

        return text

    def __call__(self):
        # 先请求首页获取cookie
        self.session.get("http://www.dianping.com/", headers=HEADERS)
        # 1、请求列表页
        content = self.parse_url(START_URL, HEADERS)
        if content is None:
            return None
        else:
            # with codecs.open('txt/shoplist.html', 'w', encoding='utf-8') as f:
            #     f.write(content.text)
            # 2、提取详情页链接并请求
            resp = Selector(content)
            shops = resp.xpath("//div[@id='shop-all-list']/ul//div[@class='tit']/a[1]/@href").extract()
            for shop_url in shops:
                print("start parse shop:", shop_url)
                item = dict()

                shop_content_text = self.parse_url(shop_url, SHOP_HEADERS).text
                content_css = self.get_css(shop_content_text).text

                # 4、获取当前详情页class对应坐标,class对应svg链接
                css_px_dict, svg_url_dict, font_dict = self.parse_shop_css(content_css)

                # 5、获取需要解密的标签 span id addresss
                shop_page_soup = bs(shop_content_text, 'lxml')

                address_tag = shop_page_soup.find(id='address')
                # 6、解密标签返回正确文本
                address = self.decrypt(address_tag, svg_url_dict, css_px_dict, font_dict)

                # print(f'\n>> 解密后内容：\n {address}')
                shop_name = list(shop_page_soup.find(name='h1', class_="shop-name").stripped_strings)[0]
                telephone_tag = shop_page_soup.find(name='p', class_="expand-info tel")
                #
                comment_tag = shop_page_soup.find(name='p', class_="desc J-desc")
                # \xa0 是不间断空白符 &nbsp; \u3000 是全角的空白符
                telephone = self.decrypt(telephone_tag, svg_url_dict, css_px_dict, font_dict).replace("电话：", "") \
                    .replace("\xa0", ",").strip()

                # 暂时只取第一条评论
                comment = self.decrypt(comment_tag, svg_url_dict, css_px_dict, font_dict)

                item['name'] = shop_name
                item['address'] = address
                item['phone'] = telephone
                item['comment'] = comment
                pprint(item)
                # 7、存储到mongodb
                # self.collection.insert_one(item)
                # time.sleep(random.uniform(*COMMENTS_SLEEP))
                # 获取下一页


if __name__ == '__main__':
    name = "dianping"
    dianping = DpFont(name)
    dianping()
