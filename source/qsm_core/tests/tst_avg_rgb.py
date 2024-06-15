# coding:utf-8
import lxbasic.cv.core as bsc_cv_core


print bsc_cv_core.Image(
    'E:/myworkspace/qosmic-2.0/source/qsm_resource/resources/icons/application/maya.png'
).get_average_rgbs()
