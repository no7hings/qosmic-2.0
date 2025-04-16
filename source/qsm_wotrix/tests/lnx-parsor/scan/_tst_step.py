# coding:utf-8
import lnx_parsor.scan as lnx_srk_scan

stage = lnx_srk_scan.Stage()

root = stage.root()

project = root.project('QSM_TST')

print(project.steps())
