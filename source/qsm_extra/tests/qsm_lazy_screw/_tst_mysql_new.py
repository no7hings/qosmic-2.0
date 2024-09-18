# coding:utf-8
from peewee import *
from playhouse.pool import PooledMySQLDatabase

# 配置数据库连接池
db = PooledMySQLDatabase(
    'motion_test',  # 数据库名称
    user='qosmic',   # 用户名
    password='qosmic',  # 密码
    host='10.32.21.16',       # 主机地址
    port=3306,               # 端口号，默认为 3306
    max_connections=4,  # 设置最大连接数
    stale_timeout=300  # 设置闲置连接超时
)


# 连接数据库
db.connect()
