# coding:utf-8
import lxbasic.dcc.core as bsc_dcc_core

d = bsc_dcc_core.DotMaOptOld(
        '/data/f/test_sequence/butterfly_a.ma'
    )

for i in d._get_obj_raws_():
    print i

for i in d.get_file_paths():
    print i
    print i['port_raw']
    print i['obj_type']
