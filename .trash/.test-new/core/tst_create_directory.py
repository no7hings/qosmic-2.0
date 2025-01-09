# coding:utf-8
import lxbasic.storage as bsc_storage

for i in range(100):
    bsc_storage.StgDirectoryOpt(
        'Z:/projects/QSM_TST/assets/chr/sam/workarea/user.nothings/rig.rigging/test_{}'.format(i)
    ).set_create()
