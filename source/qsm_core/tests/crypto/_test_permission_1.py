# coding:utf-8
import time

import lxbasic.crypto.core as c

data = dict(
    password='admin',
    time=time.time()
)

key = c.Crypto.generate_key('QOSMIC')
print(repr(key))

password_dict = dict(
    password='admin'
)

iv, d = c.Crypto.encrypt(key, password_dict)
print(repr(data))

print(c.Crypto.decrypt(key, iv, d))

c.Crypto.write_encrypted_data_to_json(
    'E:/myworkspace/qosmic-2.0/source/qsm_resora/resources/verify/resora.json', iv, d
)

iv, d = c.Crypto.read_encrypted_data_from_json(
    'E:/myworkspace/qosmic-2.0/source/qsm_resora/resources/verify/resora.json'
)

print(c.Crypto.decrypt(key, iv, d))

