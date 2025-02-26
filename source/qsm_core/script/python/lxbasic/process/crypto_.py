# coding:utf-8
import sys

import json

import subprocess

from ..crypto import core as _cpt_core


class Crypto:
    @classmethod
    def encrypt_to_dict(cls, key_str, data_dict):
        if _cpt_core.CRYPTO_FLAG is True:
            return _cpt_core.Crypto.encrypt_to_dict(
                key_str, data_dict
            )
        return cls.encrypt_to_dict_prc(key_str, data_dict)

    @classmethod
    def encrypt_to_dict_prc(cls, key_str, data_dict):
        cmd_script = r'rez-env qsm_main -- qsm-crypto -e -k "{}" -j "{}"'.format(
            key_str,
            json.dumps(data_dict).replace('"', '\\"')
        )

        result = subprocess.Popen(cmd_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = result.communicate()

        if result.returncode != 0:
            sys.stderr.write(stderr+'\n')
            return dict()

        lines = stdout.strip().split('\n')
        if lines:
            result_key = 'encrypt_result='
            line = lines[-1]
            if line.startswith(result_key):
                json_str = line[len(result_key):]
                return json.loads(json_str)
        return dict()

    @classmethod
    def decrypt_to_dict(cls, key_str, encrypted_dict):
        if _cpt_core.CRYPTO_FLAG is True:
            return _cpt_core.Crypto.decrypt_to_dict(
                key_str, encrypted_dict
            )
        return cls.decrypt_to_dict_prc(key_str, encrypted_dict)

    @classmethod
    def decrypt_to_dict_prc(cls, key_str, encrypted_dict):
        cmd_script = r'rez-env qsm_main -- qsm-crypto -d -k "{}" -j "{}"'.format(
            key_str,
            json.dumps(encrypted_dict).replace('"', '\\"')
        )

        result = subprocess.Popen(cmd_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = result.communicate()

        if result.returncode != 0:
            sys.stderr.write(stderr+'\n')
            return dict()

        lines = stdout.strip().split('\n')
        if lines:
            result_key = 'decrypt_result='
            line = lines[-1]
            if line.startswith(result_key):
                json_str = line[len(result_key):]
                return json.loads(json_str)
        return dict()
