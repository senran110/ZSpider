import json
import re
from copy import deepcopy
import scrapy
from scrapy_redis.spiders import RedisSpider

from zh.items import DangdangItem


class DangDangSpider(RedisSpider):
    name = "DD"
    redis_key = 'DD:start_urls'
    allowed_domains = ["dangdang.com"]

    def __init__(self, *args, **kwargs):
        super(DangDangSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        """
        解析列表页面所有的单独分类，获取其中的小分类
        :param response:
        :return:
        """
        item_list = response.xpath("//div[@class = 'classify_kind']//a/@href").extract()

        for href in item_list:
            yield scrapy.Request(href, callback=self.parse_nxt)

    def parse_nxt(self, response):
        """

        :param response:
        :return:
        """
        li_list = response.xpath("//div[@id = 'search_nature_rg']/ul[1]/li")

        for li in li_list:
            item = DangdangItem()
            item["link"] = li.xpath("./a[1]/@href").extract_first()
            item["title"] = li.xpath("./a[1]/@title").extract_first().strip()
            item["img_link"] = li.xpath("./a[1]/img/@data-original").extract_first()
            if not item["img_link"]:
                item["img_link"] = li.xpath("./a[1]/img/@src").extract_first()

            item['price'] = ''.join(li.xpath("./p[@class = 'price']/span/text()").extract()).replace('¥', '')
            # 商品详情
            item["detail"] = li.xpath("./p[@class = 'detail']//text()").extract_first()
            if not item["detail"]:
                item["detail"] = li.xpath("./p[@class = 'search_hot_word']//text()").extract_first()
            # 评论数
            item["comments_num"] = li.xpath("./p[@class = 'search_star_line']//a/text()").extract_first()
            if not item["comments_num"]:
                item["comments_num"] = li.xpath("./p[@class = 'star']//a/text()").extract_first()
            # 作者
            item["author"] = li.xpath("./p[@class = 'search_book_author']/span[1]/a/text()").extract_first()
            # 出版社
            item["pub"] = li.xpath("./p[@class = 'search_book_author']/span[3]/a/text()").extract_first()

            # 出版时间
            if self.is_legal(item["link"]):
                yield scrapy.Request(item["link"], callback=self.parse_details, meta={"item": item})

        nxt_tmp = response.xpath("//div[@class = 'paging']//li[@class = 'next']/a/@href").extract_first()

        if nxt_tmp is not None:
            yield scrapy.Request(response.urljoin(nxt_tmp), callback=self.parse_nxt)

    def parse_details(self, response):
        """
        解析商品的详情
        :param response:
        :return:
        """
        item = response.meta["item"]
        # 商品所属类别
        # item["category"] = response.xpath('//*[@id="breadcrumb"]/a[1]/b/text()').extract_first() + '>' + response.xpath(
        #     '//*[@id="breadcrumb"]/a[2]/text()').extract_first() + '>' + response.xpath(
        #     '//*[@id="breadcrumb"]/a[3]/text()').extract_first()
        # 商品来源
        try:
            item["source"] = response.xpath("//*[@id='shop-geo-name']/text()").extract()[0].replace('\xa0至', '')
        except IndexError as err:
            item["source"] = '当当自营'

        # 通过正则表达式提取url中的商品id
        try:
            goods_id = re.compile(r'/(\d+).html').findall(response.url)[0]
        except Exception:
            goods_id = re.compile(r'(\d+)').findall(response.url)[0]

        item["goods_id"] = goods_id

        print(item)

    @staticmethod
    def is_legal(url):
        if not url or url == "javascript:void(0);":
            return False
        return True
