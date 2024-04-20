# coding:utf-8
import lxbasic.core as bsc_core

import lxresolver.core as rsv_core

r = rsv_core.RsvBase.generate_root()

p = r.get_rsv_project(
    project='cgm'
)


def post_fnc():
    t_e = bsc_core.SysBaseMtd.get_timestamp()

    # print p._rsv_obj_stack.get_objects()
    print 'Cost', t_e - t_s


t_s = bsc_core.SysBaseMtd.get_timestamp()
for i in p.get_rsv_resource_groups(
    branch='asset'
):
    i.get_rsv_tasks()

post_fnc()


