import pymysql

from zh.items import QuestionItem, UserItem


class ZhPipeline(object):
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DBNAME'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT')
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        if isinstance(item, QuestionItem):
            # table_name = item.pop('table')
            table_name = "question"
        elif isinstance(item, UserItem):
            # table_name = item.pop('table')
            table_name = "user"

        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = "REPLACE INTO %s (%s) VALUES (%s)" % (table_name, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()

        return item

    def close_spider(self, spider):
        self.db.close()


class DangdangPipeline(object):
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DBNAME'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWD'),
            port=crawler.settings.get('MYSQL_PORT')
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        # if isinstance(item, DangdangItem):
        #     table_name = item.pop('table_name')
        # elif isinstance(item, CommentItem):
        #     table_name = item.pop('table_name')

        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (item.table_name, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item

    def close_spider(self, spider):
        self.db.close()
