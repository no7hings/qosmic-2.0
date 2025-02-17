# coding:utf-8
import lnx_scan as lnx_scan

root = lnx_scan.Stage().get_root()

print(root.projects)
project = root.project('QSM_TST')
print(project.find_assets(dict(role=['chr'])))
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

