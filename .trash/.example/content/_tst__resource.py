# coding:utf-8
import lxbasic.resource as bsc_resource

c = bsc_resource.BscExtendConfigure.get_as_content(
    'texture/name'
)

c.do_flatten()

print c
