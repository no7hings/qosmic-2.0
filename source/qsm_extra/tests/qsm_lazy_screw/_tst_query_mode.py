# coding:utf-8
from peewee import SqliteDatabase

# 创建数据库连接
db = SqliteDatabase('Z:/libraries/lazy-resource/.database/asset_test.db')

# 连接数据库
db.connect()

# 查询当前的 journal_mode
cursor = db.execute_sql('PRAGMA journal_mode;')
result = cursor.fetchone()

# 输出当前的 journal_mode
print result

# 关闭数据库连接
db.close()
