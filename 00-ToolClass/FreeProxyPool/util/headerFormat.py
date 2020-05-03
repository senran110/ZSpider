

def header_formatter(headers):
    """
    按行分隔，按冒号组成字典
    运行后复制控制台输出
    :param headers:
    :return:
    """
    hs = headers.split('\n')
    b = [k for k in hs if len(k)]
    e = b
    f = {(i.split(":")[0], i.split(":", 1)[1].strip()) for i in e}

    g = sorted(f)

    print("{")
    for k, v in g:
        print(repr(k).replace('\'', '"'), repr(v).replace('\'', '"'), sep=':', end=",\n")

    print("}")


if __name__ == '__main__':
    myheaders = """
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
"""

    header_formatter(myheaders)
