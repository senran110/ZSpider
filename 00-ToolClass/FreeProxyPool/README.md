                                      ______                        ______             _
                                      | ___ \_                      | ___ \           | |
                                      | |_/ / \__ __   __  _ __   _ | |_/ /___   ___  | |
                                      |  __/|  _// _ \ \ \/ /| | | ||  __// _ \ / _ \ | |
                                      | |   | | | (_) | >  < \ |_| || |  | (_) | (_) || |___
                                      \_|   |_|  \___/ /_/\_\ \__  |\_|   \___/ \___/ \_____\
                                                             __ / /
                                                            /___ /
## [回到总目录](https://github.com/LeoLin9527/ZSpider)

## 知识点
1】单元测试

2】异步协程

3】生成器
## 使用说明
* 启动redis服务

* 安装依赖:
```shell
pip install -r requirements.txt
```

* 打开代理池和API
```shell
python run.py
```

* API调用

访问`http://127.0.0.1:8888/random`可以获取一个可用代理。  

访问`http://127.0.0.1:8888/count`可以获取代理池中可用代理的数量。  

## 补充知识
1、 元类(记住下面这个形式用法即可)
```python
class UpperAttrMetaclass(type):
    def __new__(cls, name, bases, dct):
        attrs = ((name, value) for name, value in dct.items() if not name.startswith('__')
        uppercase_attr  = dict((name.upper(), value) for name, value in attrs)
        return type.__new__(cls, name, bases, uppercase_attr)
```

2、print带颜色输出方式
 
书写格式：开头部分：\033[显示方式;前景色;背景色m + 结尾部分：\033[0m
 
3、生成局部依赖

`pipreqs /path/to/project`

自动生成项目相关的依赖到requirements.txt

若出现UnicodeDecodeError: 'gbk' codec can't decode byte 直接修改pipreqs.py 的75行，将encoding改为utf-8
