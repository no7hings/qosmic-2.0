# coding:utf-8
import time

import lxbasic.process as p

data_dict = dict(
    password='admin',
    timestamp=time.time()
)

encrypted_dict = p.Crypto.encrypt_to_dict(
    'QOSMIC', data_dict
)

print(encrypted_dict)

print(
    p.Crypto.decrypt_to_dict(
        'QOSMIC', encrypted_dict
    )
)
