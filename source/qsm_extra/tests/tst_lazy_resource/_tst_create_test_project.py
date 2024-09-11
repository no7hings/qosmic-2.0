# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_general.scan as qsm_gnl_scan

scan_root = qsm_gnl_scan.Root.generate()

project = scan_root.project('QSM_TST')

assets = project.find_assets(dict(role=['chr']))

file_path_src = 'X:/QSM_TST/Assets/chr/sam/Rig/Final/scenes/sam_Skin.ma'

for i_asset in project.find_assets(dict(role=['chr'])):
    i_task = i_asset.task(scan_root.EntityTasks.Rig)
    i_file_path_tgt = i_task.to_storage_path(scan_root.StoragePatterns.MayaRigFile)

    bsc_storage.StgFileOpt(file_path_src).copy_to_file(i_file_path_tgt)
    