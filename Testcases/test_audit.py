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
from common.heandler_fixture import BaseTest


@ddt
class TestAudit(unittest.TestCase, BaseTest):
    exect = HeadleExcel(os.path.join(DATA_DTR, "testcase.xlsx"), "audit")
    cases = exect.read_data()
    db = HandMsql()

    @classmethod
    def setUpClass(cls) -> None:
        cls.admin_login()
        cls.user_login()

    def setUp(self) -> None:
        self.add_porject()

    @list_data(cases)
    def test_audit(self, item):
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
