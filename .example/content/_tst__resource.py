# coding:utf-8
import lxresource as bsc_resource

c = bsc_resource.RscExtendConfigure.get_as_content(
    'texture/name'
)

c.do_flatten()

print c
