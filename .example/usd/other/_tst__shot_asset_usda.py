# coding:utf-8
import lxresource as bsc_resource

key = 'usda/shot-asset-set'

t = bsc_resource.RscExtendJinja.get_template(
    key
)

c = bsc_resource.RscExtendJinja.get_configure(
    key
)

c.set('asset.role', 'chr')
c.set('asset.name', 'huayao')

c.set('shot.sequence', 'e10')
c.set('shot.name', 'e10130')

c.set('shot.set_file', '/l/prod/cjd/publish/shots/e10/e10130/set/registry/e10130.set.registry/manifest/usd/e10130.usda')

c.set(
    'shot_assets',
    {
        'huayao': '/assets/chr/huayao',
        'huayao1': '/assets/chr/huayao1'
    }
)

c.set(
    'geometry_uv_maps',
    {
        'surface_work_latest': '/l/prod/cjd/work/assets/chr/qunzhongnan_c/srf/surfacing/geometry/scene/v007/uv_map.hi.usd',
        'surface_latest': '/l/prod/cjd/publish/assets/chr/qunzhongnan_c/srf/surfacing/qunzhongnan_c.srf.surfacing.v022/cache/usd/uv_map.usd'
    }
)


raw = t.render(
    c.value
)

print raw

