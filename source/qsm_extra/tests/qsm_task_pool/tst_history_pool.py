# coding:utf-8
import qsm_task.core as qsm_tsk_core

p = qsm_tsk_core.HistoryPool.generate()

print p


print p.new_entity(
    name='',
    file='Z:/temeporaries/dongchangbao/playblast/test_source.mov',
    task='/'
)

p.do_update()

for i in p.get_entities():
    print i.get('file')
    print i.get('task')
