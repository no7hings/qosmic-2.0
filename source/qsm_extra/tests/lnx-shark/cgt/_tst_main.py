# coding:utf-8
import lnx_shark.cgt as c

root = c.Stage().root()

project = root.project('WSX')

for i in project.sequences():
    for j in i.shots():
        print(j.path)
