# coding:utf-8
import sys

import getpass

QSM_SCHEME = 'default' if getpass.getuser() == 'nothings' else 'new'

sys.stdout.write(
    'qosmic is initialization, scheme is "{}"\n'.format(QSM_SCHEME)
)


def scheme_is_new():
    return QSM_SCHEME == 'new'
