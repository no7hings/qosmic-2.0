# coding:utf-8
import re

name = 'test_gpu_assembly:region_0_AR_NS:skull1'
_ = name.split(':')
if len(_) > 1:
    ns = _[-2]
    print ns


