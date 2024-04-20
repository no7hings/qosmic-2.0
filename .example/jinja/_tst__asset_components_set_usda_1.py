# coding:utf-8
import lxresource as bsc_resource

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

key = 'usda/asset-set-v003'

t = bsc_resource.RscExtendJinja.get_template(
    key
)

c = bsc_resource.RscExtendJinja.get_configure(
    key
)

c.set('asset.set_file', '/production/shows/nsa_dev/assets/env/tree_round_kit/shared/set/registry/tree_round_kit.set.registry/cache/usd/tree_round_kit.usda')
c.set('asset.project', 'nsa_dev')
c.set('asset.role', 'env')
c.set('asset.name', 'tree_round_kit')

raw = t.render(c.get_value())

print raw

bsc_storage.StgFileOpt(
    '/production/shows/nsa_dev/assets/env/tree_round_kit/user/team.srf/extend/set/components-usd/v002/tree_round_kit.usda'
).set_write(raw)
