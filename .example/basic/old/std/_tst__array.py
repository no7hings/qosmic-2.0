# coding:utf-8


a = range(12)

t_c = 3

print [tuple(a[i:i+t_c]) for i in range(0, len(a), t_c)]

