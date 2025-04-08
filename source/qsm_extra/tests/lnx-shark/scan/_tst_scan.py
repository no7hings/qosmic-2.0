# coding:utf-8
import lnx_shark.scan as lnx_srk_scan

root = lnx_srk_scan.Stage().root()

print(root.EntityPathPatterns.Project)

projects = root.projects()
