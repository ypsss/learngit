import requests
import unittest
import os
from jsonpath import jsonpath
from unittestreport import ddt, list_data
from common.handler_exce import HeadleExcel
from common.heandler_path import DATA_DTR
from common.headler_conf import conf
from common.headler_log import my_log
from common.heander_mysql import HandMsql
from common.heandler_tools import replace_data


@ddt
class Test_recharge(unittest.TestCase):
    exect = HeadleExcel(os.path.join(DATA_DTR, "testcase.xlsx"), "recharge")
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
    def test_recharge(self, item):
        url = conf.get("env", "test_url") + item["url"]
        """替换数据 """
        item["data"] = replace_data(item["data"], Test_recharge)
        params = eval(item["data"])
        expected = eval(item["expected"])
        method = item['method'].lower()

        '''''数据库校验'''''
        sql = 'SELECT leave_amount FROM futureloan.member WHERE mobile_phone="{}"'.format(
            conf.get('test_data', 'phone'))
        before_amount = self.db.find_one(sql)[0]
        print("请求之前数据库的金额为", before_amount)

        response = requests.request(method=method, url=url, json=params, headers=self.header)
        print(response.json())
        res = response.json()

        '''''请求之后数据库校验'''''
        afterwards_amount = self.db.find_one(sql)[0]
        print("请求之后数据库的金额为 ", afterwards_amount)

        print("预期结果 ", expected)
        print("实际结果 ", res)
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected['msg'], res['msg'])
            if res['msg'] == 'OK':
                self.assertEqual(int(afterwards_amount) - int(before_amount), int(params['amount']))
            else:
                self.assertEqual(int(afterwards_amount) - int(before_amount), 0)
        except AssertionError as e:
            my_log.error("用例--【{}】---执行失败".format(item["title"]))
            my_log.exception(e)
            raise e
        else:
            my_log.info("用例--【{}】---执行通过".format(item["title"]))
