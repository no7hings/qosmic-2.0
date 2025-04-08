# coding:utf-8
from __future__ import print_function

import lnx_shark.scan as lnx_srk_scan

root = lnx_srk_scan.Stage().root()

print(root)

project = root.project('QSM_TST')

print(project)

assets = project.assets()
print(assets)

# episodes = project.episodes()
# print (episodes)
#
# for i in episodes:
#     print (i.sequences())
#     print (i.shots())

sequences = project.sequences()
print(sequences)
for i in sequences:
    print(i.shots())

# shots = project.shots()
# print (shots)
