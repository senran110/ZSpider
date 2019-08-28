"""
@file:bilibili_Geetst.py
@time:2019/8/27-10:45
"""
import base64
import time
import numpy as np
import cv2
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

USER = 'test'
PWD = 'test'
# 滑块离左边界的距离，可根据验证效果自行调整
BORDER = 6


class Crack:
    def __init__(self):
        self.url = 'https://passport.bilibili.com/login'
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.browser = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.browser, 10)
        self.bgap = "bgap.png"  # 缺口图
        self.bfull = "bfull.png"  # 原图
        self.bslide = "bslide.png"  # 滑块图

    def __del__(self):
        self.browser.close()

    def input_account_pwd(self):
        self.browser.get(self.url)
        input_user = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#login-username')))
        input_user.clear()
        input_user.send_keys(USER)
        time.sleep(1)
        input_password = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#login-passwd')))
        input_password.clear()
        input_password.send_keys(PWD)
        time.sleep(1)
        button_login = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#geetest-wrap > ul > li.btn-box > a.btn.btn-login')))
        button_login.click()
        # 等待验证码图片完全加载
        # time.sleep(5)
        # self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_slicebg geetest_absolute')))

    def get_verity_png(self):
        """获取原图及缺口图"""
        # 通过 toDataURL() 方法获取图片 base64 数据
        getImgJS1 = 'return document.getElementsByClassName("geetest_canvas_bg geetest_absolute")[0].toDataURL("image/png");'
        self.data_to_png(getImgJS1, self.bgap)
        getImgJS2 = 'return document.getElementsByClassName("geetest_canvas_slice geetest_absolute")[0].toDataURL("image/png");'
        self.data_to_png(getImgJS2, self.bslide)
        getImgJS3 = 'return document.getElementsByClassName("geetest_canvas_fullbg geetest_fade geetest_absolute")[0].toDataURL("image/png");'
        self.data_to_png(getImgJS3, self.bfull)

    def data_to_png(self, js, name):
        bg_img = ""
        while len(bg_img) < 5000:
            try:
                bg_img = self.browser.execute_script(js)
            except:
                time.sleep(0.5)
        # 去除类型，只要数据部分
        bg_img_source = bg_img[bg_img.find(',') + 1:]
        bg_source_data = base64.b64decode(bg_img_source)
        file = open(name, 'wb')
        file.write(bg_source_data)
        file.close()

    # def crop_png(self):
    #     image = cv2.imread('bslide.png')
    #     blurred = cv2.GaussianBlur(image, (5, 5), 0)
    #     canny = cv2.Canny(blurred, 380, 400)
    #     cv2.imshow("image", canny)
    #     cv2.waitKey(0)
    #     # imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #     # cv2.imshow("aaa", imgray)
    #     # cv2.waitKey()
    #     # ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    #     contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #
    #     for i, contour in enumerate(contours):
    #         M = cv2.moments(contour)
    #         print(i, cv2.contourArea(contour), cv2.arcLength(contour, True))
    #         if cv2.contourArea(contour) > 1700:
    #             x, y, w, h = cv2.boundingRect(contour)  # 外接矩形
    #             cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    #             cv2.imshow('image', image)
    #             cv2.waitKey()
    #             break
    #
    #     print(x, y, w, h)
    #     newimage = image[y + 2:y + h - 2, x + 2:x + w - 2]  # 先用y确定高，再用x确定宽
    #     cv2.imwrite("dd.png", newimage)
    #
    # def no_get_distance(self):
    #     """
    #     获取滑动距离 方案一: 因滑块图与验证图大小一样,图像切割后在模式匹配,误差大未解决
    #     :return:
    #     """
    #     self.crop_png()
    #     target = cv2.imread(self.bgap, 0)
    #     template = cv2.imread("dd.png", 0)
    #     # w, h = target.shape[::-1]
    #     targ = 'targ.jpg'
    #     temp = 'temp.jpg'
    #
    #     cv2.imwrite(temp, template)
    #     cv2.imwrite(targ, target)
    #
    #     target = cv2.imread(targ)
    #     target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    #     target = abs(255 - target)
    #
    #     cv2.imwrite(targ, target)
    #     target = cv2.imread(targ)
    #
    #     template = cv2.imread(temp)
    #     # 加载原始图像和要搜索的图像模板
    #     result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    #
    #     x, y = np.unravel_index(result.argmax(), result.shape)
    #
    #     print(x, y)
    #
    #     return x, y

    def get_distance(self):
        """
        缺口图和原图像素比对 方案二:可行
        :return:
        """
        gap = cv2.imread(self.bgap)
        full = cv2.imread(self.bfull)
        height = full.shape[0]
        width = full.shape[1]
        # 先确定宽度，再遍历高度
        for j in range(width):
            for i in range(height):
                if not self.is_pixel_equal(gap, full, i, j):
                    distance = j
                    # print("distance:", distance)

                    return distance

        print("Not Found Gap")
        return None

    def is_pixel_equal(self, gap, full, x, y):
        gap_bgr = gap[x, y]
        full_bgr = full[x, y]
        # print(x, y, ':', gap_bgr, full_bgr)

        threshold = 60  # 阈值若超出则可能是缺口边界
        # （注意 imread 函数读到的像素值是 uint8 类型，相减之后可能溢出，所以要转为 int）
        if abs(int(full_bgr[0]) - int(gap_bgr[0])) < threshold and abs(int(full_bgr[1]) - int(gap_bgr[1])) < threshold \
                and abs(int(full_bgr[2]) - int(gap_bgr[2])) < threshold:

            return True
        else:
            return False

    def ease_out_quad(self, x):
        return 1 - (1 - x) * (1 - x)

    def ease_out_quart(self, x):
        return 1 - pow(1 - x, 4)

    def ease_out_expo(self, x):
        if x == 1:
            return 1
        else:
            return 1 - pow(2, -10 * x)

    # 轨迹算法抄自网上
    def get_tracks_2(self, distance, seconds, ease_func):
        """
        根据轨迹离散分布生成的数学 生成  # 参考文档  https://www.jianshu.com/p/3f968958af5a
        成功率很高 90% 往上
        :param distance: 缺口位置
        :param seconds:  时间
        :param ease_func: 生成函数
        :return: 轨迹数组
        """
        distance += 20

        tracks = [0]
        offsets = [0]
        for t in np.arange(0.0, seconds, 0.1):
            ease = ease_func
            offset = round(ease(t / seconds) * distance)

            tracks.append(offset - offsets[-1])

            offsets.append(offset)

        # 为了去除增加的20
        tracks.extend([-3, -2, -3, -2, -2, -2, -2, -1, -0, -1, -1, -1])
        return tracks

    def shake_mouse(self):
        """
        模拟人手释放鼠标抖动
        :return: None
        """
        ActionChains(self.browser).move_by_offset(xoffset=-2, yoffset=0).perform()
        ActionChains(self.browser).move_by_offset(xoffset=3, yoffset=0).perform()

    def move_to_gap(self, tracks):
        """
        捕捉滑块并按轨迹
        :param slider:
        :param tracks:
        :return:
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        ActionChains(self.browser).click_and_hold(slider).perform()
        while tracks:
            x = tracks.pop(0)
            # print("x:", x)
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
            time.sleep(0.05)

        self.shake_mouse()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()

    def check_status(self):
        slider_box = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[6]/div/div[1]/div[2]')))

        if slider_box.get_attribute('class') == 'geetest_slider geetest_success':
            print("success")
            return True
        else:
            print("error")
            return False

    def offcial_using(self):
        while True:
            self.get_verity_png()
            distance = self.get_distance() - BORDER if self.get_distance() else 0
            if distance == 0:
                return
            tracks = self.get_tracks_2(distance, 1, self.ease_out_quart)
            print("滑动轨迹:", tracks)
            self.move_to_gap(tracks)
            time.sleep(3)
            if not self.check_status():
                print("验证失败、刷新验证码从新验证")
                button_refresh = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[2]/div[2]/div[6]/div/div[2]/div/a[2]')))
                button_refresh.click()
                time.sleep(1)
                print("已刷新验证码，再次进行验证")
                time.sleep(1)
            else:
            	# 成功即退出
                break

    def test_success_rate(self, n):
        """
        测试通过率
        :param n:
        :return:
        """
        self.get_verity_png()
        distance = self.get_distance() - BORDER if self.get_distance() else 0
        if distance == 0:
            return

        tracks = self.get_tracks_2(distance, 1, self.ease_out_quart)
        print("滑动轨迹:", tracks)
        self.move_to_gap(tracks)
        time.sleep(3)
        slider_box = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[6]/div/div[1]/div[2]')))

        if slider_box.get_attribute('class') == 'geetest_slider geetest_success':
            print(f"{n + 1} success")
            return True
        else:
            print(f"{n + 1} success")
            return False

    def run(self, n=None):
        self.input_account_pwd()
        self.offcial_using()
        # if self.test_success_rate(n):
        #     return True
        # else:
        #     return False


if __name__ == '__main__':
    BiliBili = Crack()
    BiliBili.run()
    # count = 0
    # for i in range(100):
    #     if BiliBili.run(i):
    #         count += 1
    #
    # print(f"成功率{count}%")
