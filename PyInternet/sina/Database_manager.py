import pymysql

"""
数据库地址、账号、密码、数据库名
"""
ADDRESS = 'localhost'
USER_NAME = 'sina_database_user'
USER_PASSWORD = '111111'
DATABASE_NAME = 'sina_database'


class DatabaseManager:
    @staticmethod
    def init_database():
        return pymysql.connect(ADDRESS, USER_NAME, USER_PASSWORD, DATABASE_NAME)

    @staticmethod
    def close(cursor, db):
        if cursor:
            cursor.close()
        if db:
            db.close()