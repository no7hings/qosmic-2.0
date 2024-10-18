# coding:utf-8
import qsm_scan as qsm_scan

root = qsm_scan.Root.generate()

print root.projects
project = root.project('QSM_TST')
print project.find_assets(dict(role=['chr']))
# print project.assets
# print project.asset('sam')
# print project.sequences
# print project.shots
# #
# asset = project.asset('sam')
# print asset.tasks
# task = asset.task(root.EntityTasks.Rig)
#
# print task.find_result(
#     '{root}/{project}/Assets/{role}/{asset}/Rig/Final/scenes/{asset}_Skin.ma'
# )

