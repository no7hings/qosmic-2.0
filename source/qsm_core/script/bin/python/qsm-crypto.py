# coding:utf-8
from __future__ import print_function

import sys

import getopt

LOG_KEY = 'qsm-crypto'


def main(argv):
    try:
        sys.stdout.write('execute qsm-crypto from: "{}"\n'.format(__file__))
        opts, args = getopt.getopt(
            argv[1:],
            'hedk:j:',
            ['help', 'encrypt', 'decrypt', 'key_str=', 'json_str=']
        )

        encrypt = False
        decrypt = False
        key_str = None
        json_str = None
        for i_k, i_v in opts:
            if i_k in ('-h', '--help'):
                __print_help()
                sys.exit()
            elif i_k in ('-e', '--encrypt'):
                encrypt = True
            elif i_k in ('-d', '--decrypt'):
                decrypt = True
            elif i_k in ('-k', '--key_str'):
                key_str = i_v
            elif i_k in ('-j', '--json_str'):
                json_str = i_v

        if encrypt is True:
            __encrypt_fnc(key_str, json_str)
        elif decrypt is True:
            __decrypt_fnc(key_str, json_str)

    except getopt.GetoptError:
        sys.stdout.write('argv error\n')


def __print_help():
    sys.stdout.write(
        '***** qsm-crypto *****\n'
        '\n'
        '-h or --help: show help\n'
        '\n'
        'etc.\n'
        '...\n'
    )


def __encrypt_fnc(key_str, json_str):
    import json

    import lxbasic.crypto.core as bsc_cpt_core

    data_dict = json.loads(json_str)
    encrypted_dict = bsc_cpt_core.Crypto.encrypt_to_dict(key_str, data_dict)

    sys.stdout.write('encrypt_result='+json.dumps(encrypted_dict)+'\n')


def __decrypt_fnc(key_str, json_str):
    import json

    import lxbasic.crypto.core as bsc_cpt_core

    encrypted_dict = json.loads(json_str)

    data_dict = bsc_cpt_core.Crypto.decrypt_to_dict(key_str, encrypted_dict)
    sys.stdout.write('decrypt_result='+json.dumps(data_dict)+'\n')


if __name__ == '__main__':
    main(sys.argv)
