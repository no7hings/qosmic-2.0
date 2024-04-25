# coding:utf-8
import six

import scandir

a = u'Z:/projects/QSM_TST/assets/chr/sam/work/user.nothings/mod.modeling/test_2/测试/scenes'

print scandir.scandir(a)

b = a.encode('utf-8')

print scandir.scandir(b)
