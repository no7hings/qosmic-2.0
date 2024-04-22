# coding:utf-8
import qsm_general.scan as qsm_gnl_scan

root = qsm_gnl_scan.Root.generate()

print root.projects
project = root.project('QSM_TST')
print project.assets
print project.asset('sam')
print project.sequences
print project.shots

asset = project.asset('sam')
print asset.tasks
task = asset.task(root.EntityTasks.Rig)

print task.find_result(
    '{root}/{project}/Assets/{role}/{asset}/Rig/Final/scenes/{asset}_Skin.ma'
)

