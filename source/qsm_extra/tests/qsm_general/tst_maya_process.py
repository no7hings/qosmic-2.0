# coding:utf-8
import qsm_general.core as qsm_gnl_core

import lxbasic.core as bsc_core

option_dict = dict(
    file=u'Z:/temeporaries/dongchangbao/playblast_tool/董昌宝/test.export.v009.ma'
)


cmd_script = qsm_gnl_core.MayaCacheProcess.generate_cmd_script_by_option_dict(
    'test-unicode', option_dict
)

print cmd_script

bsc_core.PrcBaseMtd.execute_as_trace(
    cmd_script
)
