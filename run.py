import unittest

from common.heandler_path import CASES_DIR, REPORT_DIR

from unittestreport import TestRunner

suite = unittest.defaultTestLoader.discover(CASES_DIR)


def run():
    runer = TestRunner(suite,
                       filename="练习测试报告",
                       report_dir=REPORT_DIR, )

    runer.run()
    # # 发送qq邮箱
    # runer.send_email(
    #     host='smtp.qq.com',
    #     port=465,
    #     user='1719100539@qq.com',
    #     password='euqrzvtgvqfvifca',
    #     to_addrs='1719100539@qq.com',
    #     is_file=True
    # )
    # # 发送钉钉
    # webwook = 'https://oapi.dingtalk.com/robot/send?access_token=afc706dfb679a5b5f9f4b52a55d3c04ade6d2e747fae7d7e01f1e18a8906d0f5'
    # runer.dingtalk_notice(url=webwook, key='测试')


if __name__ == '__main__':
    run()
