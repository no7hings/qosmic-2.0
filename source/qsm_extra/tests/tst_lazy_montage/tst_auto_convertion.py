# coding:utf-8
import qsm_lazy.montage.scripts as s


_ = s.StlConvertionOpt(
    'motion_test', '/ceshi_jichu_male_run_anim'
).generate_args()

print _[1]
