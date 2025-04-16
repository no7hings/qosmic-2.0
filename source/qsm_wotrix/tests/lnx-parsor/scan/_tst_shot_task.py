# coding:utf-8
import lnx_parsor.scan as lnx_srk_scan

stage = lnx_srk_scan.Stage()

root = stage.root()

project = root.project('QSM_TST')

for i in project.sequences():
    print(i)
    for j in i.shots():
        print(j)
        print(j.tasks())
