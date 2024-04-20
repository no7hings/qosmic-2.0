# coding:utf-8
import lxresource as bsc_resource

key = 'usda/set/asset-shot'

c = bsc_resource.RscExtendJinja.get_configure(
    key
)

c.update_from(
    dict(
        project='cgm',
        sequence='z88',
        role='chr',
        asset='nn_4y_test',
        step='rig',
        task='rigging',
        version='v012',
        asset_shot='z88380'
    )
)

c.set(
    'shot_asset',
    {
        'nn_4y_test': {
            'asset': '',
            'shot_asset': ''
        }
    }
)

print c

c.do_flatten()

usda_dict = c.get('usdas')
#
for k, v in usda_dict.items():
    t = bsc_resource.RscExtendJinja.get_template(
        '{}/{}'.format(key, k)
    )
    i_raw = t.render(
        **c.value
    )
    print i_raw
# c.set(
#     'geometry_uv_maps',
#     {
#         'surface_work_latest': '/l/prod/cjd/work/assets/chr/qunzhongnan_c/srf/surfacing/geometry/scene/v007/uv_map.hi.usd',
#         'surface_latest': '/l/prod/cjd/publish/assets/chr/qunzhongnan_c/srf/surfacing/qunzhongnan_c.srf.surfacing.v022/cache/usd/uv_map.usd'
#     }
# )
#
#
# raw = t.render(
#     c.value
# )
#
# print raw

