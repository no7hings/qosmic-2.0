# coding:utf-8
import lxresolver.core as rsv_core

import lxusd.rsv.objects as usd_rsv_objects

resolver = rsv_core.RsvBase.generate_root()

f = '/production/shows/nsa_dev/assets/env/tree_round_kit/user/work.dongchangbao/katana/scenes/surfacing/tree_round_kit.srf.surfacing.v000_001.katana'

rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(f)
if rsv_scene_properties:
    rsv_project = resolver.get_rsv_project(
        project=rsv_scene_properties.get('project')
    )
    rsv_asset = rsv_project.get_rsv_resource(
        asset=rsv_scene_properties.get('asset')
    )

    usd_rsv_objects.RsvUsdAssetSetCreator._create_asset_usd_file_fnc(
        '/production/shows/nsa_dev/assets/env/tree_round_kit/user/team.srf/extend/set/components-usd/v002/tree_round_kit.usda',
        rsv_asset,
        rsv_scene_properties
    )
