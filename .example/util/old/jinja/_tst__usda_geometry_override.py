# coding:utf-8
import lxbasic.storage as bsc_storage

import lxresource as bsc_resource

key_name = 'uv_map'

key = 'usda/geometry/all/{}'.format(key_name)

c = bsc_resource.RscExtendJinja.get_configure(
    key
)

t = bsc_resource.RscExtendJinja.get_template(key)

raw = t.render(
    **c.value
)

print raw

bsc_storage.StgFileOpt(
    '/production/shows/nsa_dev/assets/chr/td_test/user/team.srf/extend/geometry/usd/v022/{}.usda'.format(key_name)
).set_write(raw)



