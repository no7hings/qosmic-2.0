# coding:utf-8
from __future__ import print_function

import lxbasic.resource as bsc_resource

key = 'usda/set/surface'

c = bsc_resource.RscExtendJinja.get_configure(key)

k = 'geo_extra'

t = bsc_resource.RscExtendJinja.get_template('{}/{}'.format(key, k))

raw = t.render(
    **c.value
)

print(raw)
