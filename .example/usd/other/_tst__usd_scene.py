# coding:utf-8
import lxusd.dcc.objects as usd_dcc_objects

usd_file_path = '/production/shows/nsa_dev/assets/chr/td_test/user/team.srf/extend/geometry/usd/v023/payload.usda'
location = '/master/mod/hi'
location_source = '/master/hi'

s = usd_dcc_objects.Scene()

s.load_from_dot_usd(usd_file_path, location, location_source)

u = s.universe

print u.get_objs()

print u.get_obj('/master/hi')

# print u.get_obj('/master/hi').get_children()
