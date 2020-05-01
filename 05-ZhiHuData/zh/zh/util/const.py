username = ''
password = ''
checkname = ''

encrypt_data_api = "http://localhost:8888/data"

# 要加密的参数
FORM_DATA = {
    'client_id': 'c3cef7c66a1843f8b3a9e6a1e3160e20',
    'grant_type': 'password',
    'source': 'com.zhihu.web',
    'username': '',
    'password': '',
    'lang': 'en',
    'ref_source': 'homepage',
    'utm_source': ''
}
# 请求头
headers = {
    'accept-encoding': 'gzip, deflate, br',
    'Host': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}

