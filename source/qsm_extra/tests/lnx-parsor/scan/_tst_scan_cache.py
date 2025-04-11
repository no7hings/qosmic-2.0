# coding:utf-8
import lnx_parsor.scan as lnx_srk_scan

stage = lnx_srk_scan.Stage()

root = stage.root()

print (root)

print(root.EntityVariantKeys.Asset)

project = root.project('QSM_TST')

for i in project.assets():
    print(i)
    # print(i.task('Rig'))

# for i in project.episodes():
#     print(i)
#
# for i in project.sequences():
#     for j in i.shots():
#         print(j)

# for i_role in project.roles(role=['chr', 'prp']):
#     print (i_role.assets())

# print (project.assets(role=['chr', 'prp']))
# print (project.sequences(episode='A001'))

# print(project.role('chr').assets())

#
# print (len(project.assets()))
#
# print (len(project.assets()))


