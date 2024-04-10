# coding:utf-8
import lxkatana

lxkatana.set_reload()

import lxkatana.core as ktn_core

f = '/data/e/myworkspace/td/lynxi/script/python/.setup/katana/Macros/lx_cameras.yml'

m = ktn_core.NGMacro(
    NodegraphAPI.GetNode('cameras')
)

m.create_by_configure_file(
    f, 'cameras'
)

m.set_create_to_op_script_by_configure_file(f, ['camera__rotate__op_script', 'camera__viewport__op_script', 'cmera__look_checker__op_script'])
