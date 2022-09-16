import os
import unittest
import requests
from jsonpath import jsonpath
from common.handler_exce import HeadleExcel
from common.heandler_path import DATA_DTR
from common.headler_conf import conf
from common.heander_mysql import HandMsql
from common.heandler_tools import replace_data
from common.heander_mysql import HandMsql


class BaseTest:

    @classmethod
    def admin_login(cls):
        url = conf.get('env', "test_url") + "/member/login"
        """管理人员登录"""
        params = {
            "mobile_phone": conf.get('test_data', 'admin_phone'),
            "pwd": conf.get('test_data', 'admin_pwd')
        }
        headers = eval(conf.get("env", "headers"))
        response = requests.post(url=url, json=params, headers=headers)
        res = response.json()
        admin_token = jsonpath(res, "$..token")[0]
        headers["Authorization"] = "Bearer " + admin_token
        cls.admin_header = headers
        cls.admin_member_id = jsonpath(res, "$..id")[0]

    @classmethod
    def user_login(cls):
        """用户登录"""
        url = conf.get("env", "test_url") + "/member/login"
        params = {
            "mobile_phone": conf.get('test_data', 'phone'),
            "pwd": conf.get('test_data', 'pwd')
        }
        headers = eval(conf.get("env", "headers"))
        response = requests.post(url=url, json=params, headers=headers)
        res = response.json()
        token = jsonpath(res, "$..token")[0]
        headers["Authorization"] = "Bearer " + token
        cls.header = headers
        cls.member_id = jsonpath(res, "$..id")[0]

    @classmethod
    def add_porject(cls):
        """添加项目"""
        url = conf.get('env', 'test_url') + '/loan/add'
        params = {"member_id": cls.member_id,
                  "title": "借钱实现财富自由",
                  "amount": 2000,
                  "loan_rate": 18.0,
                  "loan_term": 6,
                  "loan_date_type": 1,
                  "bidding_days": 1
                  }
        response = requests.post(url=url, json=params, headers=cls.header)
        res = response.json()
        cls.loan_id = jsonpath(res, '$..id')[0]

    @classmethod
    def audit(cls):
        """审核"""
        url = conf.get('env', 'test_url') + '/loan/audit'
        params = {
            'loan_id': cls.loan_id,
            'approved_or_not': True

        }

        res = requests.post(url=url, json=params, headers=cls.admin_header)
        return res
