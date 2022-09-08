import unittest

from common.heandler_path import CASES_DIR, REPORT_DIR

from unittestreport import TestRunner

suite = unittest.defaultTestLoader.discover(CASES_DIR)

runer = TestRunner(suite,
                   filename="练习测试报告",
                   report_dir=REPORT_DIR, )


runer.run()