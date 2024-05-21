# coding:utf-8
import lxbasic.resource as bsc_resource

ctt = bsc_resource.RscExtendConfigure.get_as_content(
    'rig/adv'
)
ctt.set('option.namespace', 'test')
ctt.do_flatten()

print ctt.get_as_content('skeleton_new')
