# coding:utf-8

mxc = 2

d = 2

c = 0
for i in range(mxc):
    index = c
    #
    column = index % d
    row = int(index/d)
    print index, row, column
    c += 1
