# coding:utf-8
import lxbasic.storage as bsc_storage

import lnx_scan as lnx_scan

scan_root = lnx_scan.Stage().get_root()

project = scan_root.project('QSM_TST')

assets = project.find_assets(dict(role=['chr']))

file_path_src = 'X:/QSM_TST/Assets/chr/sam/Rig/Final/scenes/sam_Skin.ma'

for i_asset in project.find_assets(dict(role=['chr'])):
    i_task = i_asset.task(scan_root.EntityTasks.Rig)
    i_file_path_tgt = i_task.to_storage_path(scan_root.FilePatterns.MayaRigFile)

    bsc_storage.StgFileOpt(file_path_src).copy_to_file(i_file_path_tgt)
    