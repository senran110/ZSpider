# password: Ak+G32Zc/vPVM0PqATJehEt+Voi4Na18Gete90y0h/0aghM371zWYa9wQJZdQ1825//mGdlQjm+/xVabHGyv4GGUNd7CH0BZJzIiRbobbY3YHm0z9JqpSiWaQE6PAxnqihp3XTvc9/eyaymheHHZ9RmV+Drh1JP2Pq8pRlty+8k=
# persistent: true
# app: web
# phone: 17826xxxxx
import requests
import execjs


class FenBi:
    def __init__(self, phone, password):
        self.LoginUrl = "https://tiku.fenbi.com/api/users/loginV2?kav=12&app=web"
        self.session = requests.session()
        self.phone = phone
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "https://fenbi.com",
            "Referer": "https://fenbi.com/page/home",
            "Sec-Fetch-Mode": "cors",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        }
        self.ctx = self.load_js("nodeLearn3.js")
        self.password = self.generate_cipher_pwd(password)

    def load_js(self, filename):
        with open(filename, 'rb') as f:
            js = f.read().decode()

        ctx = execjs.compile(js)
        return ctx

    def generate_cipher_pwd(self, pwd):
        cipher_passwd = self.ctx.call("encryptPWD", pwd)
        return cipher_passwd

    def login(self):
        data = {
            "password": self.password,
            "persistent": True,
            "app": "web",
            "phone": self.phone
        }
        resp = self.session.post(self.LoginUrl, data=data, headers=self.headers)
        print(resp.text)


if __name__ == '__main__':
    phone = input('请输入账号:')
    password = input('请输入密码:')

    FB = FenBi(phone, password)
    FB.login()
