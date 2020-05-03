try:
    import Configparser
except ImportError:
    import configparser

# 得到当前路径
filename = "D:/FreePoxyPool/config.ini"
cf = configparser.ConfigParser()
cf.read(filename, encoding="utf8")
cf.sections()
