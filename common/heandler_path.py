import os

# 项目根目录的绝对路径
BASR_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 用例数据所在的目录
DATA_DTR = os.path.join(BASR_DIR, 'datas')
# 配置文件的根目录
CONF_DIR = os.path.join(BASR_DIR, 'conf')
# 日志文件所在目录
LOG_DIR = os.path.join(BASR_DIR, 'logs')
print(LOG_DIR)
# 报告所在的路径
REPORT_DIR = os.path.join(BASR_DIR, "reports")
# 用例模块所在的目录
CASES_DIR = os.path.join(BASR_DIR, "Testcases")
