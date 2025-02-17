# coding:utf-8
import lxbasic.core as bsc_core

import qsm_lazy_resource.resource_types.motion.scripts as s

s.MoCapDotFbxMotionRegisterBatch(
    'Z:/resources/mixamo',
).execute()

# args = s.MoCapDotFbxMotionGenerate('motion_splice', '/0DAC3C2C-F402-6636-DB97-CE11A6E139E5').generate_args()
# # r'rez-env maya-2020 mtoa qsm_maya_main -- mayabatch -command "python(\"import lxsession.commands as ssn_commands;ssn_commands.execute_option_hook(option=\\\"option_hook_key=dcc-process/maya-cache-process&method=mocap_fbx_motion_generate&method_option=03F80C39ED9DF45016EE933BFED8C7A0\\\")\")"'
# cmd_script = args[1]
# print cmd_script
#
# bsc_core.BscProcess.execute_as_trace(
#     cmd_script
# )
