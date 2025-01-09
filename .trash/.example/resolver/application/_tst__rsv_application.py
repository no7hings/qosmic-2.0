# coding:utf-8
import lxresolver.core as rsv_core

r = rsv_core.RsvBase.generate_root()

p = r.get_rsv_project(project='nsa_dev')

a = p.get_rsv_app('maya')

print a.get_command(['-- maya'])
