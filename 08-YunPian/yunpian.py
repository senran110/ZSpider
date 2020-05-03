import json
import os
import random
import time
import math
import cv2
import requests

from CrackCode import _reload_js, _encrypt_data, _get_cb, headers, RandomNum, _generate_trace_js


def pic_download(url, type):
    """
    图片下载
    :param url:
    :param type:
    :return:
    """
    img_path = os.path.abspath('...') + '/image/' + '{}.jpg'.format(type)
    img_data = requests.get(url).content
    with open(img_path, 'wb') as f:
        f.write(img_data)

    return img_path


class YunPian:
    def __init__(self):
        self.verifyUrl = 'https://captcha.yunpian.com/v1/jsonp/captcha/verify'
        self.getUrl = "https://captcha.yunpian.com/v1/jsonp/captcha/get"
        self.verifyUrl = "https://captcha.yunpian.com/v1/jsonp/captcha/verify"

        self.ctx = _reload_js()
        # 浏览器环境等参数, 可固定
        self.data = {
            "browserInfo": [{
                "key": "userAgent",
                "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
            }, {"key": "language", "value": "zh-CN"}, {"key": "hardware_concurrency", "value": 4}, {
                "key": "resolution",
                "value": [1920, 1080]
            }, {"key": "navigator_platform", "value": "Win32"}],
            "mobile": "",
            "nativeInfo": {},
            "options": {"sdk": "https://www.yunpian.com/static/official/js/libs/riddler-sdk-0.2.2.js"},
            "fp": "c723c98d68b3641085c35891e243e063",
            "address": "https://www.yunpian.com",
            "yp_riddler_id": "1ba912a6-0a30-488f-80fb-9a41735a2b41"
        }

    def _init_slider(self):
        encrypt_data = _encrypt_data(self.ctx, self.data)
        params = {
            'cb': _get_cb(self.ctx),
            'i': encrypt_data['i'],
            'k': encrypt_data['k'],
            'captchaId': 'b68fba1577964dc59c10a46c142b12ac'  # 固定值
        }
        resp = requests.get(self.getUrl, params=params, headers=headers)
        print("请求完毕！！！")
        result = json.loads(resp.text.replace('ypjsonp(', '').replace(')', ''))
        if result['msg'] == 'ok':
            bg = result['data']['bg']
            fg = result['data']['front']
            token = result['data']['token']

            return {
                'captcha_url': bg,
                'slider_url': fg,
                'token': token
            }

        return None

    @staticmethod
    def _get_distance(slider_url, captcha_url):
        """
        获取缺口距离
        :param slider_url: 滑块图片 url
        :param captcha_url: 验证码图片 url
        :return:
        """
        # 引用上面的图片下载
        slider_path = pic_download(slider_url, 'slider')
        # 引用上面的图片下载
        captcha_path = pic_download(captcha_url, 'captcha')
        # 计算拼图还原距离
        target_rgb = cv2.imread(captcha_path)

        target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)

        template_rgb = cv2.imread(slider_path, 0)

        res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)
        # 求这个矩阵的最小值，最大值，并得到最大值，最小值的索引
        value = cv2.minMaxLoc(res)
        a, b, c, d = value

        if abs(a) >= abs(b):
            distance = c[0]
        else:
            distance = d[0]

        return distance

    def get_track(self, distance):
        # 生成某个区间的随机数,两位小数
        value = round(random.uniform(0.55, 0.75), 2)  # 分割加减速路径的阀值
        distance += 20  # 划过缺口20px
        v, t, sum = 0, 0.2, 0  # 初始速度，初始计算周期，累积滑动总距的变量
        plus = []  # 用于记录轨迹
        mid = distance * value  # 将滑动距离分段，一段加速度，一段减速度

        while sum < distance:
            if sum < mid:
                a = round(random.uniform(2.5, 3.5), 1)  # 指定范围随机产生一个加速度
            else:
                a = -(round(random.uniform(2.0, 3.0), 1))  # 指定范围随机产生一个减速的加速度
            s = v * t + 0.5 * a * (t ** 2)  # 一个周期需要滑动的距离
            v = v + a * t  # 一个周期结束时的速度
            sum += s
            plus.append(round(s))

        reduce = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]  # 手动制造回滑的轨迹累积20px
        return {'plus': plus, 'reduce': reduce}

    def _generate_trace_py(self, distance):
        baseX = RandomNum(1110, 1130)  #
        baseY = RandomNum(1190, 1220)  #
        sy = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0]
        st = [15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17, 18, 15, 16,
              17, 18, 15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17, 18, 14, 16, 17, 18, 16, 17, 18, 19, 20, 17]

        zt = RandomNum(3, 10)

        value = round(random.uniform(0.55, 0.75), 2)  # 分割加减速路径的阀值
        v, t, sum = 0, 0.2, 0  # 初始速度，初始计算周期，累积滑动总距的变量
        tracks_list = []  # 用于记录轨迹
        mid = distance * value  # 将滑动距离分段，一段加速度，一段减速度
        while sum < distance:
            if sum < mid:
                a = round(random.uniform(2.5, 3.5), 1)  # 指定范围随机产生一个加速度
            else:
                a = -(round(random.uniform(2.0, 3.0), 1))  # 指定范围随机产生一个减速的加速度
            s = v * t + 0.5 * a * (t ** 2)  # 一个周期需要滑动的距离
            v = v + a * t  # 一个周期结束时的速度
            sum += s
            tracks_list.append(round(s))
        # x_offset, y_offset = 0, 0
        timestamp = zt + random.randint(80, 120)
        timestamp_list = [timestamp]
        time.sleep(random.uniform(0.5, 1.5))
        for i in range(1, len(tracks_list)):
            t = random.randint(11, 18)

            timestamp += t

            timestamp_list.append(timestamp)

            i += 1

        y_list = []
        for j in range(len(tracks_list)):
            y = random.choice(sy)
            y_list.append(y)
            j += 1

        trace = [[str(baseX), str(baseY), zt]]
        for index, x in enumerate(tracks_list):
            trace.append([str(baseX + x), str(baseY + y_list[index]), timestamp_list[index]])

        return self.reduce_points(trace)

    def reduce_points(self, points):
        if len(points) <= 50:
            return points

        e = [points[0]]
        n = points[len(points) - 1]
        r = math.floor(len(points) / 50)
        if r < 2:
            return points
        for i in range(1, len(points) - 2, r):
            e.append(points[i])
        e.append(n)
        return e

    def run(self):
        # 获取背景图
        while True:
            init_data = self._init_slider()
            if init_data:
                break
            print("retry...")
            time.sleep(random.random())

        # 图片尺寸比: 浏览器上的验证码图片尺寸为 310 * 155 像素, 而下载下来的图片尺寸为 480 * 240 像素
        distance = self._get_distance(init_data['slider_url'], init_data['captcha_url'])
        distance = int(distance * (310 / 480))
        # 人为轨迹
        trace = _generate_trace_js(self.ctx, distance)
        trace = self.reduce_points(trace)

        data = {
            'points': trace,
            'distanceX': distance / 310,
            'fp': "c723c98d68b3641085c35891e243e063",  # 指纹可固定
            'address': "https://www.yunpian.com",
            'yp_riddler_id': "39448245-cdce-4442-ac02-54e1b476d8a4"  # 这个不知道啥也可以固定
        }
        encrypt_data = _encrypt_data(self.ctx, data)

        params = {
            'cb': self.ctx.call('get_cb'),

            'i': encrypt_data['i'],

            'k': encrypt_data['k'],

            'token': init_data['token'],

            'captchaId': 'b68fba1577964dc59c10a46c142b12ac'
        }

        resp = requests.get(self.verifyUrl, headers=headers, params=params)

        result = json.loads(resp.text.replace('ypjsonp(', '').replace(')', ''))
        if result['msg'] == 'ok':
            return {
                'success': 1,
                'message': '校验成功! ',
                'data': result['data']
            }

        return {
            'success': 0,
            'message': '校验失败! ',
            'data': None
        }


if __name__ == '__main__':
    yp = YunPian()
    yp.run()
