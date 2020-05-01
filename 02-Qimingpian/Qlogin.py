"""
@file:Qlogin.py
@time:2019/7/29-17:19
"""
import logging
import pickle
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def check_login(cookies=None):
    """
    cookie有效性验证
    :param cookies:
    :return:
    """
    check_url = "https://www.qimingpian.com/finosda/project/pinvestment"
    browser = webdriver.Chrome()
    browser.get(check_url)

    if cookies is not None:
        for cookie in cookies:
            browser.add_cookie(cookie)

    browser.refresh()
    time.sleep(3)

    try:
        text = browser.find_element_by_xpath("//span[@class='fs12 fc3 ml2']").text
    except Exception:
        text = ""

    browser.quit()
    return text


def login_selenium(index_url, telephone, cookies=None):
    """
    企名片selenium模拟登录
    :param index_url:
    :param telephone:
    :param cookies:
    :return:
    """
    chrome_options = webdriver.ChromeOptions()
    # 添加启动参数
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')
    # chrome_options.add_argument('--proxy-server={0}'.format(PROXY))
    # chrome_options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
    chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    # chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    # 添加实验性质的设置参数
    # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    browser = webdriver.Chrome(chrome_options=chrome_options)
    # browser.maximize_window()
    wait = WebDriverWait(browser, 10)
    browser.get(index_url)

    try:
        btn_click = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='app-login f-hblue']")))
        btn_click.click()
        time.sleep(3)
        hand_btn = browser.find_element_by_xpath("//div[@class='footer-logiin']")

        actions = ActionChains(browser)
        actions.move_to_element(hand_btn).click().perform()

        input_phone = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@class='c-phone-input']")))
        input_phone.send_keys(telephone)

        code_btn = browser.find_element_by_xpath("//button[@class='c-code-btn']")
        code_input = browser.find_element_by_xpath("//input[@class='c-code-input']")
        code_submit = browser.find_element_by_xpath("//button[@class='c-submit-btn']")
        code_btn.click()

        code = input("输入验证码:")
        code_input.send_keys(code)
        code_submit.click()

    except Exception as e:
        browser.quit()
        logging.warning("click error...")
        logging.warning(e)
        return

    time.sleep(3)

    try:
        text = browser.find_element_by_xpath("//span[@class='fs12 fc3 ml2']").text
    except Exception as err:
        text = ""

    # 判断登录是否成功,若成功则保存cookie到文件
    if "充值" in text:
        print("login success...")
        pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))
        time.sleep(1)
    else:
        print("login failed...")

    browser.quit()


if __name__ == '__main__':
    # url = "https://www.qimingpian.com/finosda/project/pinvestment"
    # phone = ""
    # login_selenium(url, phone)
    file_cookies = pickle.load(open("cookies.pkl", "rb"))
    text = check_login(file_cookies)
    print(text)
