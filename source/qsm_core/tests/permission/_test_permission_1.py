# coding:utf-8
import time

import lxbasic.permission as p

data = dict(
    password='admin',
    time=time.time()
)

key = p.Encrypt.generate_key_from_string('QOSMIC')
print(repr(key))

password_dict = dict(
    password='admin'
)

iv, d = p.Encrypt.encrypt(key, password_dict)
print(repr(data))

print(p.Encrypt.decrypt(key, iv, d))

p.Encrypt.save_encrypted_data_to_json(
    'E:/myworkspace/qosmic-2.0/source/qsm_resora/resources/verify/resora.json', iv, d
)

iv, d = p.Encrypt.load_encrypted_data_from_json(
    'E:/myworkspace/qosmic-2.0/source/qsm_resora/resources/verify/resora.json'
)

print(p.Encrypt.decrypt(key, iv, d))

