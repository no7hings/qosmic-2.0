# coding:utf-8
import MySQLdb


class MySql(object):
    @classmethod
    def to_connection(cls, dtb_options, name):
        return MySQLdb.connect(
            user=dtb_options['user'],
            passwd=dtb_options['password'],
            host=dtb_options['host'],
            port=dtb_options['port']
        )

    @classmethod
    def create_database(cls, dtb_options, name):
        connection = MySQLdb.connect(
            user=dtb_options['user'],
            passwd=dtb_options['password'],
            host=dtb_options['host'],
            port=dtb_options['port']
        )

        cursor = connection.cursor()
        cursor.execute(
            "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s", (name,)
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.execute("CREATE DATABASE {}".format(name))

        cursor.close()
        connection.close()

    @classmethod
    def get_all_database_names(cls, dtb_options):
        list_ = []
        connection = MySQLdb.connect(
            user=dtb_options['user'],
            passwd=dtb_options['password'],
            host=dtb_options['host'],
            port=dtb_options['port']
        )

        cursor = connection.cursor()

        cursor.execute("SHOW DATABASES")

        databases = cursor.fetchall()
        for i_dtb in databases:
            list_.append(i_dtb[0])
        return list_

    @classmethod
    def database_is_exists(cls, dtb_options, name):
        connection = MySQLdb.connect(
            user=dtb_options['user'],
            passwd=dtb_options['password'],
            host=dtb_options['host'],
            port=dtb_options['port']
        )
        cursor = connection.cursor()
        cursor.execute(
            "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s", (name,)
        )
        return bool(cursor.fetchone())
