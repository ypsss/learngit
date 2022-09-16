import os
import unittest
import requests
from jsonpath import jsonpath
from unittestreport import ddt, list_data
from common.handler_exce import HeadleExcel
from common.heandler_path import DATA_DTR
from common.headler_conf import conf
from common.headler_log import my_log
from common.heander_mysql import HandMsql
from common.heandler_tools import replace_data
from common.heandler_fixture import BaseTest

@ddt
class TestWithraw(unittest.TestCase,BaseTest):
    exect = HeadleExcel(os.path.join(DATA_DTR, "testcase.xlsx"), "withdraw")
    cases = exect.read_data()
    db = HandMsql()

    @classmethod
    def setUpClass(cls) -> None:
        cls.user_login()


    @list_data(cases)
    def test_withraw(self, item):
        url = conf.get("env", "test_url") + item["url"]
        """数据替换"""
        item["data"] = replace_data(item["data"],TestWithraw)
        params = eval(item["data"])
        expected = eval(item["expected"])
        method = item['method'].lower()


        """接口请求"""
        response = requests.request(method=method, url=url, json=params, headers=self.header)
        print(response.json())
        res = response.json()
        print("预期结果 ", expected)
        print("实际结果 ", res)

        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected['msg'], res['msg'])

        except AssertionError as e:
            my_log.error("用例--【{}】---执行失败".format(item["title"]))
            my_log.exception(e)
            raise e
        else:
            my_log.info("用例--【{}】---执行通过".format(item["title"]))
