import pymysql
from common.headler_conf import conf


class HandMsql:
    def __init__(self):
        # 1,建立连接
        self.conect = pymysql.connect(
            host=conf.get('mysql', 'host'),
            port=conf.getint('mysql', 'port'),
            user=conf.get('mysql', 'username'),
            password=conf.get('mysql', 'password'),
            charset='utf8')

    # 查询所有的sql语句
    def find_one_count(self, sql):
        with self.conect as cur:
            cur.execute(sql) 
            res = cur.fetchall()
            # 获取结果
        return res
        # 显示查询的一条sql语句

    def find_one(self, sql):
        with self.conect as cur:
            cur.execute(sql)
            res = cur.fetchone()
        return res

    # 显示条数
    def find_count(self, sql):
        with self.conect as cur:
            res = cur.execute(sql)
        return res


# 关闭连接


if __name__ == '__main__':
    sql1 = 'SELECT leave_amount FROM futureloan.member WHERE mobile_phone="13636781961";'
    db = HandMsql()
    ress = db.find_one(sql1)
    print(ress)
