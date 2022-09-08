import requests
import unittest
import os
from unittestreport import ddt, list_data
from common.handler_exce import HeadleExcel
from common.heandler_path import DATA_DTR
from common.headler_conf import conf
from common.headler_log import my_log
from common.heandler_data import random_phone


@ddt
class TestReqister(unittest.TestCase):
    exect = HeadleExcel(os.path.join(DATA_DTR, "testcase.xlsx"), "register")
    cases = exect.read_data()
    print(cases)
    test_url = conf.get('env', 'test_url')
    header = eval(conf.get('env', "headers"))

    @list_data(cases)
    def test_reqister(self, item):
        url = self.test_url + item['url']
        phone = random_phone()
        print(phone)
        item["data"] = item["data"].replace("#phone#", phone)
        print(item['data'])
        params = eval(item['data'])
        expected = eval(item["expected"])
        method = item['method']
        response = requests.request(method=method, url=url, json=params, headers=self.header)
        print(response.json())
        res = response.json()
        print("实际结果 ", res)
        print("预期结果 ", expected)
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected['msg'], res['msg'])
        except AssertionError as e:
            my_log.error("用例--【{}】---执行失败".format(item["title"]))
            my_log.exception(e)
            raise e
        else:
            my_log.info("用例--【{}】---执行通过".format(item["title"]))
