import logging
import os
from common.headler_conf import conf
from common.heandler_path import BASR_DIR


def create_log(name="zld.log", level="Debug", filename="zld.log", fh_level="DEBUG", sh_level="DEBUG"):
    # 创建日志收集器

    log = logging.getLogger(name)
    # 设置日志收集器收集日志的等级
    log.setLevel(level)

    # 输出到文件
    fh = logging.FileHandler(filename, encoding="utf-8")
    fh.setLevel(fh_level)
    log.addHandler(fh)

    # 输出到控制台
    sh = logging.StreamHandler()
    sh.setLevel(sh_level)
    log.addHandler(sh)

    # 设置日志输出的等级
    formats = '%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'
    log_format = logging.Formatter(formats)
    sh.setFormatter(log_format)
    fh.setFormatter(log_format)

    # 返回一个日志的收集器
    return log


my_log = create_log(
    name=conf.get("logging", "name"),
    level=conf.get("logging", "level"),
    fh_level=conf.get("logging", "fh_level"),
    sh_level=conf.get("logging", "sh_level"),
    filename=conf.get("logging", "filename"),
)

if __name__ == '__main__':
    print(create_log(my_log))
    print(create_log(log))
