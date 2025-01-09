# coding:utf-8
import lxusd.core as usd_core

file_path = '/production/shows/nsa_dev/assets/chr/td_test/user/team.srf/extend/geometry/usd/v022/payload.usda'

s = usd_core.UsdStageOpt()

s.load_by_locations_fnc(
    file_path,
    locations=[
        ('/master/hi', '/master/mod/hi'),
        #
        '/master/hair',
        #
        ('/master/aux/grm', '/master/grm'),
        ('/master/aux/cfx', '/master/cfx'),
        ('/master/aux/efx', '/master/efx'),
        ('/master/aux/misc', '/master/misc')
    ],
    active_locations=['/master/aux']
)

print s.get_all_objs()

