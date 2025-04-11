# coding:utf-8
import lnx_parsor.swap as s

root = s.Swap.generate_root()

project = root.project('QSM_TST')

for i in project.sequences():
    for j in i.shots():
        print(j.path)
