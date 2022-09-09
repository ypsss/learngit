import re
import random
from common.headler_conf import conf


def random_phone():
    """随机手机号"""
    phone = str(random.randint(13300000000, 13399999999))
    return phone


def replace_data(data, cls):
    """
    替换数据
    :param data:
    :param cls:
    :return:
    """
    while re.search("#(.+?)#", data):
        res = re.search("#(.+?)#", data)
        itme = res.group()
        attr = res.group(1)
        try:
            value = getattr(cls, attr)
        except AssertionError:
            value = conf.get("test_data", attr)
        data = data.replace(itme, str(value))
    return data


if __name__ == '__main__':
    print(random_phone())