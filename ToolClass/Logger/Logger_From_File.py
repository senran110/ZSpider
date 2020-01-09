import logging.config
import os
import yaml


def setup_logging(default_path='config.yml', default_level=logging.DEBUG):
    """
    Setup logging configuration
    """
    path = default_path
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            config = yaml.load(f.read())
            logging.config.dictConfig(config)
            logger = logging.getLogger("main")

        return logger
    else:
        logging.basicConfig(level=default_level)
        print('the input path doesn\'t exist')


# 对应的是 root 一项配置，它指定了 handlers 是 console，即只输出到控制台
if '__main__' == __name__:
    logger = setup_logging(default_path='config.yml')
    # logging.debug('Start')
    # logging.info('Exec')
    # logging.info('Finished', exc_info=True)
    logger.warning('my linxi')
