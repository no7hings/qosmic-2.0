# coding:utf-8
import lxgeneral.dcc.core as gnl_dcc_core

o = gnl_dcc_core.DotMaOpt(
    'Z:/temeporaries/dongchangbao/cfx/test_ma_ascii.ma'
)

for i in o.get_node_paths():
    print(i)
