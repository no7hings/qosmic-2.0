# coding:utf-8
from peewee import SqliteDatabase

db = SqliteDatabase('Z:/libraries/lazy-resource/.database/motion_test.db')

# 连接数据库
db.connect()

# 修改 journal_mode 为 DELETE
db.execute_sql('PRAGMA journal_mode=DELETE;')

# 关闭数据库连接
db.close()
