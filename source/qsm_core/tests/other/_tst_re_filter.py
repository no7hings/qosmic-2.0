# coding:utf-8
import re

s = '{directory}/Assets/{role}/{asset}/*/*/scenes/{asset}_Skin.ma'
s_1 = s

r = re.finditer(r'\*+', s, re.IGNORECASE)

for i_seq, i in enumerate(r):
    i_start, i_end = i.span()
    s_1 = s_1.replace(s[i_start:i_end], '{{var_{}}}'.format(i_seq), 1)

print s_1
