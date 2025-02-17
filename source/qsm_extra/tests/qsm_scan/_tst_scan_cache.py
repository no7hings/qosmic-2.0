# coding:utf-8
import lnx_scan as lnx_scan

stage = lnx_scan.Stage()

root = stage.get_root()

print root

project = root.project('QSM_TST')

for i_role in project.find_roles(variants_extend=dict(role=['chr', 'prp'])):
    print i_role.find_assets()

print project.find_assets(variants_extend=dict(role='chr'))

print len(project.assets)

print len(project.assets)


