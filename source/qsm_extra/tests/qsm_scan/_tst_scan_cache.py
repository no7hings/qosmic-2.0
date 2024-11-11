# coding:utf-8
import qsm_scan as qsm_scan

root = qsm_scan.Stage().get_root()

print root

project = root.find_project('QSM_TST')

print project.find_assets(variants_extend=dict(role='chr'))

print len(project.find_assets())

print len(project.find_assets())


