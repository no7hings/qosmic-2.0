# coding:utf-8
from __future__ import print_function

import lnx_shark.scan as lnx_srk_scan

root = lnx_srk_scan.Stage().root()

print(root)

project = root.find_project('QSM_TST')

print(project)

assets = project.find_assets()
print(assets)

# episodes = project.find_episodes()
# print episodes
#
# for i in episodes:
#     print i.find_sequences()
#     print i.find_shots()

sequences = project.find_sequences()
print(sequences)
for i in sequences:
    print(i.find_shots())

# shots = project.find_shots()
# print shots
