# coding:utf-8
import lxresource as bsc_resource

key = 'usda/set/surface'

c = bsc_resource.RscExtendJinja.get_configure(key)

k = 'geo_extra'

t = bsc_resource.Jinja.get_template('{}/{}'.format(key, k))

raw = t.render(
    **c.value
)

print raw
