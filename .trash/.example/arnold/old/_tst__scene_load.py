# coding:utf-8
import collections

import lxarnold.startup as and_startup

and_startup.MtoaSetup('/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019').set_run()

import lxarnold.dcc.objects as and_dcc_objects

s = and_dcc_objects.Scene(option=dict(shader_rename=True))

s.load_from_dot_ass(
    '/production/shows/nsa_dev/assets/chr/td_test/user/team.srf/extend/look/ass/v001/default.ass',
    path_lstrip='/root/world/geo',
    path_mapper=collections.OrderedDict(
        [
            # source >> target
            # renderable
            #   model
            ('/master/hi', '/master/mod/hi'),
            ('/master/lo', '/master/mod/lo'),
            # auxiliary
            ('/master/aux/grm', '/master/grm'),
            ('/master/aux/cfx', '/master/cfx'),
            ('/master/aux/efx', '/master/efx'),
            ('/master/aux/misc', '/master/misc')
        ]
    )
)

u = s.universe

t = u.get_obj_type('mesh')

for i in t.get_objs():
    print i
