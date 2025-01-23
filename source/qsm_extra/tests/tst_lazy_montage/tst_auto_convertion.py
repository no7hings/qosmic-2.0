# coding:utf-8
import qsm_lazy_resource.extra.motion.scripts as s


_ = s.STDotAnimGenerate(
    'motion_test', '/ceshi_jichu_male_run_anim'
).generate_args()

print _[1]
