# coding:utf-8
import subprocess

import lxbasic.core as bsc_core

return_dict = {}

try:
    bsc_core.BscProcess.execute_as_block(
        r'/job/PLE/support/wrappers/paper-bin lxdcc_lib@/home/dongchangbao/packages/lxdcc_lib/9.9.99 lxdcc@/home/dongchangbao/packages/lxdcc/9.9.99 lxdcc_gui@/home/dongchangbao/packages/lxdcc_gui/9.9.99 lxdcc_rsc@/home/dongchangbao/packages/lxdcc_rsc/9.9.99 maya@2019.2 paper_wrap_maya@master-5 paper_extend_maya@/home/dongchangbao/packages/paper_extend_maya/9.99.99 paper_extend_maya_stable@master-1 usd@20.11 mtoa@4.2.1.1 --join-cmd maya -batch -command "python(\"importlib=__import__(\\\"importlib\\\");ssn_commands=importlib.import_module(\\\"lxsession.commands\\\");ssn_commands.execute_option_hook(option=\\\"option_hook_key="dcc-process/maya-process"&geometry_abc_file=/production/library/resource/all/3d_plant_proxy/yegrass_n009_rsc/v0001/geometry/abc/yegrass_n009_rsc.abc&geometry_usd_file=/production/library/resource/all/3d_plant_proxy/yegrass_n009_rsc/v0001/geometry/usd/yegrass_n009_rsc.usd&method=scene-to-geometry&scene_maya_file=/production/library/resource/all/3d_plant_proxy/yegrass_n009_rsc/v0001/scene/maya/yegrass_n009_rsc.ma&use_update_mode=False&with_geometry_abc=True&with_geometry_usd=True\\\")\")"',
        clear_environ='auto',
        return_dict=return_dict
    )

except subprocess.CalledProcessError:
    pass

finally:
    print return_dict
