# coding:utf-8
import lnx_resora_extra.animation.motion.scripts as s


_ = s.STDotAnimGenerate(
    'motion_test', '/ceshi_jichu_male_run_anim'
).generate_args()

print(_[1])
