# coding:utf-8
# import parse
#
# parse_pattern = '\'{file}\'%{argument}'
# e = "'/l/prod/cjd/work/assets/prp/chengzhen_b_shuimian/srf/surfacing/texture/ocean_tex_v01/ocean_displace.%04d.tx'%int(frame%326+1001)"
#
# if e:
#     p = parse.parse(parse_pattern, e)
#     if p:
#         print p.named.get('file'), p.named.get('argument')
#
#
# "'/t/prod/cgm/output/shots/z95/z95020/efx/efx_ocean_songshu/songshu/bakeTexture1/oceanevaluate_L7/v0010/oceanevaluate_L7.dis.4334.%04d.exr'%(frame%326+120)"

import fnmatch

import lxbasic.core as bsc_core

print bsc_core.PtnFnmatchMtd.to_re_style('A')
print bsc_core.PtnFnmatchMtd.to_re_style('A*')
