import os
from logging.handlers import RotatingFileHandler
from time import strftime
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

log_name = os.path.join(
    basedir, 'log/flask/flask_{}.log'.format(strftime('%Y%m%d')))

FLASK_LOG_FILE = os.getenv('FLASK_LOG_FILE') or log_name

if not os.path.exists(os.path.dirname(FLASK_LOG_FILE)):
    os.makedirs(os.path.dirname(FLASK_LOG_FILE))


def init_logger(verbose=1, log_name=None):
    # 1.获取日志器 暴露了应用程序代码能直接使用的接口。
    # 如果没有显式的进行创建，则默认创建一个root logger，并应用默认的日志级别(WARN)，
    logger = logging.getLogger(log_name)
    # 设置日志级别
    logger.setLevel(logging.DEBUG if verbose > 1 else logging.INFO)

    # 2.获取处理器 创建一个handler,用于写入日志文件
    # Formatter默认为%Y-%m-%d %H:%M:%S。
    f_handler = logging.FileHandler(FLASK_LOG_FILE, encoding='utf-8')
    # 为Handler添加Formatter,Formatter默认为%Y-%m-%d %H:%M:%S,
    # 创建方法: formatter = logging.Formatter(fmt=None, datefmt=None)
    # formatter = logging.Formatter(
    #     '[%(asctime)s %(filename)s:%(lineno)s] - %(message)s')
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    f_handler.setFormatter(formatter)  # 设置格式化器
    f_handler.setLevel(logging.DEBUG)  # 指定日志级别，低于被忽略

    # 再创建一个handler，用于输出到控制台
    console = logging.StreamHandler()

    # 3.将处理器添加到日志器中
    # 为Logger实例增加一个处理器,可添加多个handler
    logger.addHandler(console)
    logger.addHandler(f_handler)

    return logger


main_logger = init_logger(log_name='flask')
sub_logger = init_logger(log_name='flask.sub')

if __name__ == '__main__':
	main_logger.info("Flask Main")

# --------华丽的分割线------------#
# # 设置日志的记录等级
# logging.basicConfig(level=logging.DEBUG)
# # 创建日志记录器，指明日志保存的路径，每个日志文件的最大大小,保存的日志文件个数上限
# file_log_handler = RotatingFileHandler("logs/log",maxBytes=1024*1024*100,backupCount=10,encoding='utf-8')
# # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
# formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(messages)s')
# # 为刚创建的日志记录器设置日志记录格式
# file_log_handler.setFormatter(formatter)
# # 为全局的日志工具对象(flask app使用的)添加日志记录器
# logging.getLogger().addHandler(file_log_handler)
