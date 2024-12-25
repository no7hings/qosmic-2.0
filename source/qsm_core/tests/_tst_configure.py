# coding:utf-8
import lxbasic.resource as bsc_resource


c = bsc_resource.RscExtendConfigure.get_as_content('motion/motion_layer')

c.do_flatten()
print c
