import json
import os

import pymysql

from loggerutils import logger


def find(name, path):
    """ 查找文件路径 """
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


class DataBase:
    @staticmethod
    def connect_db():
        """
        创建链接
        :return:
        """
        try:
            config = find("db_config.json", os.path.abspath("."))
            with open(config, "r") as file:
                load_dict = json.load(file)
                print(load_dict)
            return pymysql.connect(cursorclass=pymysql.cursors.DictCursor, **load_dict)
        except Exception as e:
            logger.error(f"cannot create mysql connect:{e}")

    def queryone(self, sql, param=None):
        """
        返回结果集的第一条数据
        :param sql: sql语句
        :param param: string|tuple|list
        :return: 字典列表 [{}]
        """
        con = self.connect_db()
        cur = con.cursor()

        row = None
        try:
            cur.execute(sql, param)
            row = cur.fetchone()
        except Exception as e:
            con.rollback()
            logger.error("[sql]:{} [param]:{}".format(sql, param))

        cur.close()
        con.close()
        return self.simple_value(row)

    def queryall(self, sql, param=None):
        """
        返回所有查询到的内容 (分页要在sql里写好)
        :param sql: sql语句
        :param param: tuple|list
        :return: 字典列表 [{},{},{}...] or [,,,]
        """
        con = self.connect_db()
        cur = con.cursor()

        rows = None
        try:
            cur.execute(sql, param)
            rows = cur.fetchall()
        except Exception as e:
            con.rollback()
            logger.error("[sql]:{} [param]:{}".format(sql, param))

        cur.close()
        con.close()
        return self.simple_list(rows)

    def insertmany(self, sql, arrays=None):
        """
        批量插入数据
        :param sql: sql语句
        :param arrays: list|tuple [(),(),()...]
        :return: 入库数量
        """
        con = self.connect_db()
        cur = con.cursor()

        cnt = 0
        try:
            cnt = cur.executemany(sql, arrays)
            con.commit()
        except Exception as e:
            con.rollback()
            logger.error("[sql]:{} [param]:{}".format(sql, arrays))

        cur.close()
        con.close()
        return cnt

    def insertone(self, sql, param=None):
        """
        插入一条数据
        :param sql: sql语句
        :param param: string|tuple
        :return: id
        """
        con = self.connect_db()
        cur = con.cursor()

        lastrowid = 0
        try:
            cur.execute(sql, param)
            con.commit()
            lastrowid = cur.lastrowid
        except Exception as e:
            con.rollback()
            logger.error("[sql]:{} [param]:{}".format(sql, param))

        cur.close()
        con.close()
        return lastrowid

    def execute(self, sql, param=None):
        """
        执行sql语句:修改或删除
        :param sql: sql语句
        :param param: string|list
        :return: 影响数量
        """
        con = self.connect_db()
        cur = con.cursor()

        cnt = 0
        try:
            cnt = cur.execute(sql, param)
            con.commit()
        except Exception as e:
            con.rollback()
            logger.error("[sql]:{} [param]:{}".format(sql, param))

        cur.close()
        con.close()
        return cnt

    @staticmethod
    def simple_list(rows):
        """
        结果集只有一列的情况, 直接使用数据返回
        :param rows: [{'id': 1}, {'id': 2}, {'id': 3}]
        :return: [1, 2, 3]
        """
        if not rows:
            return rows

        if len(rows[0].keys()) == 1:
            simple_list = []
            # print(rows[0].keys())
            key = list(rows[0].keys())[0]
            for row in rows:
                simple_list.append(row[key])
            return simple_list

        return rows

    @staticmethod
    def simple_value(row):
        """
        结果集只有一行, 一列的情况, 直接返回数据
        :param row: {'count(*)': 3}
        :return: 3
        """
        if not row:
            return None

        if len(row.keys()) == 1:
            # print(row.keys())
            key = list(row.keys())[0]
            return row[key]

        return row


if __name__ == '__main__':
    print("hello everyone!!!")
    mysqlOpt = DataBase()
    # print("删表:", execute('drop table test_users'))

    sql = '''
            CREATE TABLE `test_users` (
              `id` int(11) NOT NULL AUTO_INCREMENT,
              `email` varchar(255) NOT NULL,
              `password` varchar(255) NOT NULL,
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='测试用的, 可以直接删除';
            '''
    print("create table:", mysqlOpt.execute(sql))

    # 批量插入
    sql_str = "insert into test_users(email, password) values (%s, %s)"
    arrays = [
        ("aaa@126.com", "111111"),
        ("bbb@126.com", "222222"),
        ("ccc@126.com", "333333"),
        ("ddd@126.com", "444444")
    ]
    print("插入数据:", mysqlOpt.insertmany(sql_str, arrays))

    # 查询
    print("只取一行:", mysqlOpt.queryone("select * from test_users limit %s,%s", (0, 1)))  # 尽量使用limit
    print("查询全表:", mysqlOpt.queryall("select * from test_users"))

    # 条件查询
    print("一列:", mysqlOpt.queryall("select email from test_users where id <= %s", 2))
    print("多列:",
          mysqlOpt.queryall("select * from test_users where email = %s and password = %s", ("bbb@126.com", "222222")))

    # 更新|删除
    print("更新:", mysqlOpt.execute("update test_users set email = %s where id = %s", ('new@126.com', 1)))
    print("删除:", mysqlOpt.execute("delete from test_users where id = %s", 4))

    # 查询
    print("再次查询全表:", mysqlOpt.queryall("select * from test_users"))
    print("数据总数:", mysqlOpt.queryone("select count(*) from test_users"))
