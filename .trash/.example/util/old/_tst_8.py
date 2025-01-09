# coding:utf-8
import os
import argparse

f = '/l/prod/cg7/work/assets/chr/king_cloud/srf/surfacing/maya/images/tmp/light_light_camera2/cputime/king_cloud.srf.surfacing.v036.1001.exr'

s = os.stat(f)
print (s)
print oct(s.st_mode)[-3:]
print s.st_gid
print s.st_uid


def get_mode(mode):
    mode_list = ['d', 'r', 'w', 'x', 'r', 'w', 'x', 'r', 'w', 'x']
    mode_str = bin(mode)[-10:]
    ret = ''
    for index, flag in enumerate(mode_str):
        if flag == '1':
            ret += mode_list[index]
        else:
            ret += '-'
    return ret


print get_mode(s.st_mode)
