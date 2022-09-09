import unittest
import os
from unittestreport import ddt,list_data
from common.headler_conf import conf
from common.handler_exce import HeadleExcel


@ddt
class TestInvest(unittest.TestCase):
    exect = HeadleExcel(os.path.join(DATA_DTR, "testcase.xlsx"), "invest")
    cases = exect.read_data()



    @list_data(cases)
    def testinvest(self,itme):
        pass