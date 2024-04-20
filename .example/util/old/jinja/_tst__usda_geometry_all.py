# coding:utf-8
import lxresource as bsc_resource

import lxbasic.storage as bsc_storage

key_name = 'auxiliary'

key = 'usda/geometry/all/{}'.format(key_name)

c = bsc_resource.RscExtendJinja.get_configure(
    key
)

t = bsc_resource.RscExtendJinja.get_template(key)

raw = t.render(
    **c.value
)

print raw

# bsc_storage.StgFileOpt(
#     '/production/shows/nsa_dev/assets/chr/td_test/user/team.mod/extend/geometry/usd/v002/{}.usda'.format(key_name)
# ).set_write(raw)


