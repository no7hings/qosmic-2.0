# coding:utf-8
import lxarnold.startup as and_startup

s = and_startup.MtoaSetup('/job/PLE/bundle/thirdparty/mtoa/5.2.2.1/Linux/2020')
s.set_run()
# s.add_xgen(
#     '/job/PLE/bundle/thirdparty/maya/2020.0/Linux/plug-ins/xgen'
# )
# s.add_libraries(
#     '/job/PLE/bundle/thirdparty/maya/2020.0/Linux/bin',
#     '/job/PLE/bundle/thirdparty/maya/2020.0/Linux/lib',
#     '/job/PLE/bundle/thirdparty/maya/2020.0/Linux/plug-ins/xgen/bin',
#     '/job/PLE/bundle/thirdparty/maya/2020.0/Linux/plug-ins/xgen/lib',
# )

from lxarnold.dcc import dcc_objects

f = '/l/prod/cg6/publish/assets/character/queen_white/texture/pub/ass/queen_white.hair.ass'

s = dcc_objects.Scene()

s.load_from_dot_ass(f)

ms = s.universe.get_obj_type('xgen_description').get_objs()

for g in ms:
    print g
