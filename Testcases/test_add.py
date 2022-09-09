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
from common.heander_mysql import HandMsql


@ddt
class TestAdd(unittest.TestCase):
    exect = HeadleExcel(os.path.join(DATA_DTR, "testcase.xlsx"), "add")
    cases = exect.read_data()
    db = HandMsql()

    @classmethod
    def setUpClass(cls) -> None:
        url = conf.get("env", "test_url") + "/member/login"
        params = {
            "mobile_phone": conf.get('test_data', 'phone'),
            "pwd": conf.get('test_data', 'pwd')
        }
        header = eval(conf.get("env", "headers"))
        response = requests.post(url=url, json=params, headers=header)
        res = response.json()
        token = jsonpath(res, "$..token")[0]
        print(token)
        header["Authorization"] = "Bearer " + token
        cls.header = header
        cls.member_id = jsonpath(res, "$..id")[0]
        print(cls.member_id)

    @list_data(cases)
    def test_add(self, item):
        url = conf.get("env", "test_url") + item["url"]
        """数据替换"""
        item["data"] = replace_data(item["data"], TestAdd)
        params = eval(item["data"])
        expected = eval(item["expected"])
        method = item['method'].lower()
        """数据库校验"""
        sql = "SELECT * FROM futureloan.loan WHERE member_id={}".format(self.member_id)
        start_count = self.db.find_count(sql)
        print(start_count)
        print("请求数据库前的id",start_count)
        """接口请求"""
        response = requests.request(method=method, url=url, json=params, headers=self.header)
        print(response.json())
        res = response.json()
        print("预期结果 ", expected)
        print("实际结果 ", res)
        """数据校验"""
        end_count = self.db.find_count(sql)
        print("请求数据后的数据",end_count)
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected['msg'], res['msg'])
            if res['msg'] == "OK":
                self.assertEqual(int(end_count) - int(start_count), 1)
            else:
                self.assertEqual(int(end_count) - int(start_count), 0)
        except AssertionError as e:
            my_log.error("用例--【{}】---执行失败".format(item["title"]))
            my_log.exception(e)
            raise e
        else:
            my_log.info("用例--【{}】---执行通过".format(item["title"]))
