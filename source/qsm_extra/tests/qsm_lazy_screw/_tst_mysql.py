# coding:utf-8
from peewee import MySQLDatabase, Model, CharField

# 创建 MySQL 数据库连接
db = MySQLDatabase(
    'motion_test',  # 数据库名称
    user='qosmic',   # 用户名
    password='qosmic',  # 密码
    host='10.32.21.16',       # 主机地址
    port=3306,               # 端口号，默认为 3306
    max_connections=32,
)

# 连接数据库
db.connect()
