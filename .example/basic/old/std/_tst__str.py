# coding:utf-8
import string

print

a = 'abcd'


for i in [v if seq == 0 else '{}: {}'.format(k.rjust(20), v) for seq, (k, v) in enumerate({'name': 'Test', 'tag': 'a, b'}.items())]:
    print i

