# coding:utf-8
import lnx_parsor.scan as lnx_srk_scan

root = lnx_srk_scan.Stage().root()

# print(root.EntityPathPatterns.Project)

# print(root.projects())

print(root.project('QSM_TST'))
