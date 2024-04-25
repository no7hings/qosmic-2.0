# coding:utf-8
import lxgeneral.dcc.objects as gnl_dcc_objects


d = gnl_dcc_objects.StgDirectory('/l/prod/cgm/work/assets/chr/grandma_test/srf/surfacing/zb/output/20220506')


fs = d.get_all_file_paths()

for i_f in fs:
    print i_f
    i_f_ = gnl_dcc_objects.StgFile(i_f)
    new_name = i_f_.name.replace('.disp.', '.z_disp.')
    # print new_name
    i_f_.set_rename(new_name)
