# coding:utf-8
import qsm_shark.parse as c

stage = c.Stage()

print stage.projects(space_key='disorder')

project = stage.project('QSM_TST')

for i_sequence in project.sequences(space_key='disorder'):
    print i_sequence.shots()

# print project.asset('sam')

print project.assets(space_key='disorder')
