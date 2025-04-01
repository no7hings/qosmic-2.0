# coding:utf-8
from __future__ import print_function

import os

import sys

import time

import getpass

import lxbasic.resource as bsc_resource

import lxbasic.process as bsc_process

import lxbasic.storage as bsc_storage

from . import base as _base


class Verify:
    __PASSED = False

    @classmethod
    def __main_fnc(cls, key, expiration_days):
        if cls.__PASSED is False:
            result = cls.__match_fnc(key, expiration_days)
            if result is True:
                cls.__PASSED = True
            return result
        return True

    @classmethod
    def __write_local_fnc(cls, key, local_json_path):
        password = _base.GuiApplication.exec_input_dialog(
            type='password',
            info='Entry password...',
            title='Password for {}'.format(key)
        )
        if password:
            if cls.__match_server_fnc(key, password) is True:
                data_dict = dict(
                    password=password,
                    user=getpass.getuser(),
                    timestamp=time.time(),
                )
                encrypted_dict = bsc_process.Crypto.encrypt_to_dict(
                    'QOSMIC', data_dict
                )
                if encrypted_dict:
                    bsc_storage.StgFileOpt(local_json_path).set_write(encrypted_dict)
                    return True

            _base.GuiApplication.exec_message_dialog(
                'Password error.',
                title='Password',
                size=(320, 120),
                status='error',
            )
        return False

    @classmethod
    def __match_fnc(cls, key, expiration_days):
        local_json_path = _base.GuiUtil.get_user_verify_file(key)
        if os.path.isfile(local_json_path) is False:
            return cls.__write_local_fnc(key, local_json_path)
        return cls.__read_local_fnc(key, local_json_path, expiration_days)

    @classmethod
    def __read_local_fnc(cls, key, local_json_path, expiration_days):
        encrypted_dict = bsc_storage.StgFileOpt(local_json_path).set_read()

        data_dict = bsc_process.Crypto.decrypt_to_dict(
            'QOSMIC', encrypted_dict
        )
        if data_dict:
            password = data_dict.get('password')
            if cls.__match_server_fnc(key, password):
                user = data_dict.get('user')
                if user == getpass.getuser():
                    timestamp = data_dict.get('timestamp')
                    if timestamp:
                        d = 24*3600.0
                        s_less = int(expiration_days*d)-(int(time.time()) - int(timestamp))
                        sys.stderr.write('verify less: {} days.\n'.format(round(s_less/d, 3)))
                        if s_less > 0:
                            return True
                return cls.__write_local_fnc(key, local_json_path)
        return False

    @classmethod
    def __match_server_fnc(cls, key, password):
        serve_json_path = bsc_resource.BscExtendResource.get('verify/{}.json'.format(key))
        encrypted_dict = bsc_storage.StgFileOpt(serve_json_path).set_read()
        data_dict = bsc_process.Crypto.decrypt_to_dict(
            'QOSMIC', encrypted_dict
        )
        if data_dict:
            return password == data_dict.get('password')
        return False

    @classmethod
    def execute(cls, key='default', expiration_days=1.0/24/60):
        def decorator(fnc):
            def wrapper(*args, **kwargs):
                if cls.__main_fnc(key, expiration_days):
                    fnc(*args, **kwargs)
            return wrapper
        return decorator
