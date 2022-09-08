import os

from configparser import ConfigParser

from common.heandler_path import CONF_DIR


class Config(ConfigParser):
    """创建对象时，直接加载配置文件的内容"""
    def __init__(self, conf_file):
        super().__init__()

        self.read(conf_file, encoding="utf-8")


conf = Config(os.path.join(CONF_DIR, 'cc.ini'))




if __name__ == '__main__':
    print(str(conf.get('mysql','host')))

