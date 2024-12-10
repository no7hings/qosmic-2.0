# coding:utf-8
import qsm_scan as qsm_scan

stage = qsm_scan.Stage()

root = stage.get_root()

print root

project = root.project('QSM_TST')

print project.find_assets(variants_extend=dict(role='chr'))

print len(project.assets)

print len(project.assets)


