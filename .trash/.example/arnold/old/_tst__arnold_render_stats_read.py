# coding:utf-8
import lxbasic.content as bsc_content

import lxbasic.core as bsc_core

f = '/l/prod/cjd/publish/assets/chr/qunzhongnv_b/srf/surfacing/qunzhongnv_b.srf.surfacing.v014/render/output/default.stats.0001.json'
# f = '/data/f/cjd__wuhu__debug/katana/stats_2.json'

c = bsc_content.Content(value=f)

ks = []
s = {}

for i in c.get_keys('*.bytes'):
    i_v = c.get(i)
    i_k = str(i_v)
    if i_v not in ks:
        ks.append(i_v)
    s.setdefault(i_k, []).append(i)

ks.sort()

ms = []
for i_k in ks:
    i_v = s[str(i_k)]
    for j_v in i_v:
        ms.append(int(i_k))

    print bsc_core.BscInteger.to_prettify_as_file_size(int(i_k)), i_v

print bsc_core.BscInteger.to_prettify_as_file_size(sum([abs(i) for i in ms[:-1]]))



