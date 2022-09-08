import re


class test:
    id = 44
    name = "yangpemg"
    data = "2341234"
    title = "测试报告"


s = '{"id":"#id#","name":"#name  #","data":"#data#","title":"#title#"}'

while re.search("#(.+?)#", s):
    res = re.search("#(.+?)#", s)
    print(res)
    itme = res.group()
    attr = res.group(1)
    value = getattr(test, attr)
    s = s.replace(itme, str(value))

print(s)
