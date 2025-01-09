# coding:utf-8

a = [u'Z:/projects/QSM_TST/assets/chr/sam/workarea/user.nothings/mod.modeling/test_2', u'Z:/projects/QSM_TST/assets/chr/sam/workarea/user.nothings/mod.modeling/test_3', u'Z:/projects/QSM_TST/assets/chr/sam/workarea/user.nothings/mod.modeling/tset_1']

a.sort(key=lambda x: x.split('/')[-1])

print a
