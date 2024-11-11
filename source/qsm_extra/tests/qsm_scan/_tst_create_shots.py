# coding:utf-8
import lxbasic.storage as bsc_storage


d = 'X:\QSM_TST_NEW'

for i in range(100):
    i_episode_dir_path = '{}/A{}'.format(d, str(i).zfill(3))
    bsc_storage.StgPath.create_directory(i_episode_dir_path)
    for j in range(10):
        j_sequence_dir_path = '{}/A{}_{}/动画'.format(i_episode_dir_path, str(i).zfill(3), str(j).zfill(3))
        bsc_storage.StgPath.create_directory(j_sequence_dir_path)
