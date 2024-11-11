# coding:utf-8
import qsm_scan as qsm_scan

root = qsm_scan.Stage().get_root()

print root

project = root.find_project('QSM_TST')

print project

assets = project.find_assets()
print assets

# episodes = project.find_episodes()
# print episodes
#
# for i in episodes:
#     print i.find_sequences()
#     print i.find_shots()

sequences = project.find_sequences()
print sequences
for i in sequences:
    print i.find_shots()

# shots = project.find_shots()
# print shots
