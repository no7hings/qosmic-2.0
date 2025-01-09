# coding:utf-8
import lxbasic.core as bsc_core

return_dict = {}

cmd = r'rez-env maya-2019 -- mayabatch -command "python(\"print \\\"A\\\"\")"'

bsc_core.BscProcess.execute_as_trace(
    cmd
)
