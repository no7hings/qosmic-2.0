# coding:utf-8
import os.path

import six

a = u'Z:/projects/QSM_TST/assets/chr/sam/work/user.nothings/mod.modeling/test_2/测试/scenes'

print os.path.exists(u'Z:/projects/QSM_TST/assets/chr/sam/work/user.nothings/mod.modeling/test_2/测试/scenes')

print os.path.exists('Z:/projects/QSM_TST/assets/chr/sam/work/user.nothings/mod.modeling/test_2/测试/scenes')

print isinstance(a, six.text_type)

b = a.encode('utf-8')

print os.path.exists(b)

print isinstance(b, six.text_type)

a = '测试'

b = 'b'

a0 = a.decode('utf-8')
b0 = b.decode('utf-8')

print '{}{}'.format(a0, b0)
