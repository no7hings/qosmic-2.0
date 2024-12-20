# coding:utf-8
import qsm_shark.parse as c

stage = c.Stage()

project = stage.project('QSM_TST', space_key='source')

# for i_sequence in project.sequences(space_key='disorder'):
#     print i_sequence.shots()

# print project.asset('sam')

# print project.assets(role=['chr'])

print project.shots(sequence=['A001_002'])

# print project.shots(sequence=['A001_001'])
#
# for i_asset in project.assets(role=['chr']):
#     i_tasks = i_asset.tasks(step=['cfx', 'rig'])
#     for j_task in i_tasks:
#         print j_task.versions()
