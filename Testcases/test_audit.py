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
class TestAudit(unittest.TestCase):
    exect = HeadleExcel(os.path.join(DATA_DTR, "testcase.xlsx"), "audit")
    cases = exect.read_data()
    db = HandMsql()

    @classmethod
    def setUpClass(cls) -> None:
        url = conf.get("env", "test_url") + "/member/login"
        """管理人员登录"""
        params = {
            "mobile_phone": conf.get('test_data', 'admin_phone'),
            "pwd": conf.get('test_data', 'admin_pwd')
        }
        header = eval(conf.get("env", " headers"))
        response = requests.post(url=url, json=params, headers=header)
        res = response.json()
        admin_token = jsonpath(res, "$..token")[0]
        header["Authorization"] = "Bearer " + admin_token
        cls.admin_header = header
        cls.admin_member_id = jsonpath(res, "$..id")[0]
        """用户登录"""
        params = {
            "mobile_phone": conf.get('test_data', 'phone'),
            "pwd": conf.get('test_data', 'pwd')
        }
        header = eval(conf.get("env", "headers"))
        response = requests.post(url=url, json=params, headers=header)
        res = response.json()
        token = jsonpath(res, "$..token")[0]
        header["Authorization"] = "Bearer " + token
        cls.header = header
        cls.member_id = jsonpath(res, "$..id")[0]
        """类级别前置  用户的登录"""

    def setUp(self) -> None:
        """用例级别前置  添加项目"""
        url = conf.get('env', 'test_url') + '/loan/add'
        params = {"member_id": self.member_id,
                  "title": "借钱实现财富自由",
                  "amount": "2000",
                  "loan_rate": "18.0",
                  "loan_term": "6",
                  "loan_date_type": "1",
                  "bidding_days": "1"
                  }
        resource = requests.post(url=url, json=params, headers=self.header)
        res = resource.json()
        TestAudit.loan_id = jsonpath(res, '$..id')[0]

    @list_data(cases)
    def testaudit(self, item):
        url = conf.get('env', 'test_url') + item['url']
        item['data'] = replace_data(item['data'], TestAudit)
        params = eval(item['data'])
        methd = (item['method'])
        expected = eval(item['expected'])

        requestss = requests.request(method=methd, url=url, json=params, headers=self.admin_header)
        res = requestss.json()
        if res['msg'] == 'OK':
            TestAudit.pass_loan_id = self.loan_id

        print("实际结果", res)
        print("预期结果", expected)

        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected['msg'], res['msg'])
        except AssertionError as e:
            my_log.error("用例--【{}】---执行失败".format(item["title"]))
            my_log.exception(e)
            raise e
        else:
            my_log.info("用例--【{}】---执行通过".format(item["title"]))
