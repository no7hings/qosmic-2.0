# coding:utf-8
import lxbasic.storage as bsc_storage


class NodeContext(object):

    @classmethod
    def get_file_opt(cls):
        directory_path = bsc_storage.StgUser.get_user_directory()
        file_path = '{}/screw/node-context.json'.format(directory_path)
        return bsc_storage.StgFileOpt(file_path)

    @classmethod
    def save(cls, data):
        cls.get_file_opt().set_write(data)

    @classmethod
    def read(cls):
        return cls.get_file_opt().set_read()
