# coding:utf-8
import qsm_general.entity as qsm_gnl_entity

root = qsm_gnl_entity.Root()
print root.projects
project = root.project('QSM_TST')
print project.assets
print project.asset('sam')
print project.sequences
print project.shots

asset = project.asset('sam')
print asset.tasks

