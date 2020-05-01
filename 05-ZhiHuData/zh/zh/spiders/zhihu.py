# -*- coding: utf-8 -*-
import json
import re

import scrapy
from scrapy_redis.spiders import RedisSpider

from zh.items import QuestionItem, UserItem


class ZhihuSpider(RedisSpider):
    name = 'zh'
    # allowed_domains = ['zhihu.com']
    # If empty, uses default '<spider>:start_urls'
    redis_key = 'zh:start_urls'
    answer_url = "https://www.zhihu.com/api/v4/questions/{qid}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset={offset}&platform=desktop&sort_by=default"

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        # domain = kwargs.pop('domain', '')
        # self.allowed_domains = filter(None, domain.split(','))
        super(ZhihuSpider, self).__init__(*args, **kwargs)

    # def make_requests_from_url(self, url):
    #     return Request(url, dont_filter=True, cookies=cookies, meta={'cookiejar': 1})

    def parse(self, response):
        # 1、提取详细请求的连接
        detail_url_list = response.xpath("//div[@class='HotList-list']/section[position()>1]/a/@href").extract()
        print("length:", len(detail_url_list))
        # 2、进行每个问答详情请求
        for url in detail_url_list:
            yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        qItem = QuestionItem()
        question_title = response.xpath("//h1[@class='QuestionHeader-title']/text()").extract_first()
        if not question_title:
            question_title = response.xpath("//title/text()").extract_first()

        answer_num = int(response.xpath("//h4[@class='List-headerText']/span/text()").re_first(r"\d+"))
        question_id = re.search(r"\d+", response.url).group()
        qItem['question_title'] = question_title
        qItem['answer_num'] = answer_num
        qItem['question_id'] = question_id

        yield qItem
        # 获取页面显示的用户数据
        UserResponse = response.xpath("//div[@class='List-item']")[0]
        uItem = UserItem()
        username = UserResponse.xpath("//a[@class='UserLink-link']/text()").extract_first()
        userid = UserResponse.xpath("//a[@class='UserLink-link']/@href").extract_first()
        userid = userid[userid.rindex('/') + 1:]

        headline = UserResponse.xpath("//div[@class='ztext AuthorInfo-badgeText']/text()").extract_first("")
        vote_num = UserResponse.xpath("//span[@class='Voters']//text()").re_first(r"\d+,\d+")

        uItem['username'] = username
        uItem['headline'] = headline
        uItem['vote_num'] = vote_num
        uItem['userid'] = userid

        yield uItem

        if answer_num > 5:
            # 获取更多的用户数据
            userAPI = self.answer_url.format(qid=question_id, offset=5)
            yield scrapy.Request(userAPI, callback=self.parse_user)

    def parse_user(self, response):
        userJson = json.loads(response.text)
        uItem = UserItem()
        data_list = userJson.get('data')
        for data in data_list:
            uItem['username'] = data.get('author').get('name')
            uItem['headline'] = data.get('author').get('headline')
            uItem['vote_num'] = data.get('voteup_count')
            uItem['userid'] = data.get('author').get('url_token')

            yield uItem

        is_end = userJson.get('paging').get('is_end')

        if not is_end:
            print("开始请求下一页....")
            next_url = userJson.get('paging').get('next')
            yield scrapy.Request(next_url, callback=self.parse_user)
