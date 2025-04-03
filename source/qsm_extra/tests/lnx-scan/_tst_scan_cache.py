# coding:utf-8
import lnx_shark.scan as lnx_srk_scan

stage = lnx_srk_scan.Stage()

root = stage.get_root()

print (root)

project = root.project('QSM_TST')

# for i_role in project.find_roles(variants_extend=dict(role=['chr', 'prp'])):
#     print (i_role.find_assets())

print (project.assets(role=['chr', 'prp']))
print (project.sequences(episode='A001'))
#
# print (len(project.assets()))
#
# print (len(project.assets()))


