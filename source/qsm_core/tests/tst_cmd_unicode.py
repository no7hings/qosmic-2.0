# coding:utf-8
import json

import lxbasic.core as bsc_core

option_dict = dict(
    method='test-unicode',
    file=u'Z:/temeporaries/dongchangbao/playblast_tool/董昌宝/test.export.v009.ma'
)

o = bsc_core.ArgDictStringOpt(
    eval(json.dumps(option_dict))
).to_string()


cmd_script = r'rez-env maya-2019 qsm_dcc_main -- mayabatch -command "python(\"import lxsession.commands as ssn_commands;ssn_commands.execute_option_hook(option=\\\"{option}\\\")\")"'.format(
    option=o
)

print cmd_script

# bsc_core.PrcBaseMtd.execute_as_trace(
#     cmd_script
# )
