# coding:utf-8
import lxarnold.fnc.objects as and_fnc_objects

f = '/l/prod/cjd/publish/assets/chr/laohu_xiao/srf/surfacing/laohu_xiao.srf.surfacing.v038/cache/ass/laohu_xiao.ass'

f_0 = '/data/f/arnold_usd_export/test_1.properties.usda'

e = and_fnc_objects.LookPropertiesUsdExporter(
    option=dict(
        file=f_0,
        root='/master',
        location='/master',
        ass_file=f
    )
)

e.set_run()
