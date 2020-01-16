# PythonSpider 
![](https://img.shields.io/badge/requests-2.20.0-green.svg) 
![](https://img.shields.io/badge/PyExecJS-1.5.1-green.svg) 

## 前言
- 此仓库为本人学习爬虫的总目录，涉及基础JS逆向和APP端模拟爬取。
- 默认使用者对Python及nodeJs熟悉，依赖安装无问题。
- 个人博客：[点这里进入](http://fishmoon.xyz)

## 目录
####  原创工具类
1. 仓库地址：本仓库文件夹【ToolClass】
2. 放置本人原创/仿制的工具类及其他资料文件

####  红薯中文网小说（截至2020/1/9测试）
1. 仓库地址：本仓库文件夹【SweetPotato】
2. PC端：[神魂丹帝](https://www.hongshu.com/content/86560/146038-12572043.html)
3. 移动端：[神魂丹帝](https://g.hongshu.com/content/86560/12572043.html)
4. 分析文章：[见浙里](http://fishmoon.xyz/2019/07/30/Font%20%E7%BA%A2%E8%96%AF%E4%B8%AD%E6%96%87%E7%BD%91%E5%B0%8F%E8%AF%B4%E7%88%AC%E5%8F%96/)
5. 分析注意：调试JS时面对node环境下不存在window对象，可利用jsdom处理。打印输出的words结果存在差异，一般是同一份代码环境不同导致的，可以从对环境属性的判断进行调试。
6. **友情提醒：**单纯爬取小说而不是练习反爬处理时可以直接爬取PC端。

#### 企名片项目数据（截至2020/1/13测试）
1. 仓库地址：本仓库文件夹【qmingpian】
2. PC端：[企名科技](https://www.qimingpian.cn/finosda/project/pinvestment)
3. 分析文章：[见浙里](http://fishmoon.xyz/2019/10/08/JsCrack%20%E4%BC%81%E5%90%8D%E7%89%87encrypt_data%E8%A7%A3%E6%9E%90/)
4. **使用说明**：首先开启server文件夹下的接口，然后运行run_qmingpian.py。

## 补充内容
```
def method_one(source, dest):
    """
    利用内置模块递归拷贝目录树
    :param source:
    :param dest:
    :return:
    """
    shutil.copytree(source, dest, ignore=shutil.ignore_patterns('*.pyc', 'tmp*'))
```







