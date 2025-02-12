# coding:utf-8
import qsm_lazy_backstage.core as lzy_bks_core

p = lzy_bks_core.NoticePool.generate()

print(p)


print(p.new_entity(
    name='',
    file='Z:/temeporaries/dongchangbao/playblast/test_source.mov',
    task='/'
))

p.do_update()

for i in p.get_entities():
    print(i.get('file'))
    print(i.get('task'))
