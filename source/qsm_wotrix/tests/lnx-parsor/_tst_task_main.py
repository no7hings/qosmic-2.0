# coding:utf-8
from __future__ import print_function

import lnx_parsor.parse as c


stage = c.Stage()

# print stage.projects()

print (stage.projects(space_key='disorder'))

project = stage.project('QSM_TST')
for i_asset in project.assets(role='chr'):
    print(i_asset)
    # print i_asset.task('cfx_rig', space_key='release')
    for j_task in i_asset.tasks():
        print('result:', j_task.version('001'))
        print(j_task)
        # print j_task.variants
        for k_version in j_task.versions():
            print(k_version)

print(project.asset('sam').variants)
print(project.episodes())
print(project.sequences())
print(project.shots())

print(project.sequence('A001_001').shots())

print(project.shots(sequence='A001_001'))

print(stage.project('QSM_TST').variants)

print(stage.all())

