# coding:utf-8
from __future__ import print_function

import os
import sys

import time

import lxbasic.resource as bsc_resource

import lxbasic.permission as bsc_permission

from . import base as _base


class Verify:
    __PASS = False

    @classmethod
    def __main_fnc(cls, key, expiration_days):
        if cls.__PASS is False:
            result = cls.__match_fnc(key, expiration_days)
            if result is True:
                cls.__PASS = True
            return result
        return True

    @classmethod
    def __write_local_fnc(cls, key, json_path):
        result = _base.GuiApplication.exec_input_dialog(
            type='password',
            info='Entry password...',
            title='Password'
        )
        if result:
            if cls.__match_server_fnc(key, result) is True:
                data_dict = dict(
                    password=result,
                    timestamp=time.time()
                )
                iv, encrypted_data = bsc_permission.Encrypt.encrypt(
                    bsc_permission.Encrypt.generate_key_from_string('QOSMIC'),
                    data_dict
                )
                bsc_permission.Encrypt.save_encrypted_data_to_json(json_path, iv, encrypted_data)
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
        json_path = _base.GuiUtil.get_user_verify_file(key)
        if os.path.isfile(json_path) is False:
            return cls.__write_local_fnc(key, json_path)
        return cls.__read_local_fnc(key, json_path, expiration_days)

    @classmethod
    def __read_local_fnc(cls, key, json_path, expiration_days):
        iv, encrypted_data = bsc_permission.Encrypt.load_encrypted_data_from_json(
            json_path
        )
        data_dict = bsc_permission.Encrypt.decrypt(
            bsc_permission.Encrypt.generate_key_from_string('QOSMIC'),
            iv,
            encrypted_data
        )

        password = data_dict.get('password')
        if cls.__match_server_fnc(key, password):
            timestamp = data_dict.get('timestamp')
            if timestamp:
                d = 24*3600.0
                s_less = int(expiration_days*d)-(int(time.time()) - int(timestamp))
                sys.stderr.write('verify less: {} days.\n'.format(round(s_less/d, 3)))
                if s_less > 0:
                    return True

        return cls.__write_local_fnc(key, json_path)

    @classmethod
    def __match_server_fnc(cls, key, password):
        json_path = bsc_resource.BscExtendResource.get('verify/{}.json'.format(key))

        iv, encrypted_data = bsc_permission.Encrypt.load_encrypted_data_from_json(json_path)
        data_dict = bsc_permission.Encrypt.decrypt(
            bsc_permission.Encrypt.generate_key_from_string('QOSMIC'),
            iv,
            encrypted_data
        )
        return password == data_dict['password']

    @classmethod
    def execute(cls, key='default', expiration_days=1.0/24/60):
        def decorator(fnc):
            def wrapper(*args, **kwargs):
                if cls.__main_fnc(key, expiration_days):
                    fnc(*args, **kwargs)
            return wrapper
        return decorator
