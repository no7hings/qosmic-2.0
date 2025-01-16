# coding:utf-8
import qsm_lazy_resource.scripts as s


_ = s.StlMotionGenerate(
    'motion_test', '/ceshi_jichu_male_run_anim'
).generate_args()

print _[1]
