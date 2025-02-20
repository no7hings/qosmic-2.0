# coding:utf-8
import lxbasic.storage as bsc_storage

import lxbasic.scan as bsc_scan

import lnx_resora.resource_types.maya_scene.scripts as s

directory_path = 'Z:/temporaries/maya_scene_register_test'

directory_kwargs = dict(
    directory=directory_path
)

formats = ['ma', 'mb']
file_pattern = '{directory}//*.{format}'

file_paths = []

for i_format in formats:
    i_directory_kwargs = dict(directory_kwargs)
    i_directory_kwargs['format'] = i_format

    i_file_regex = file_pattern.format(
        **i_directory_kwargs
    )

    i_file_paths = bsc_scan.ScanGlob.glob_files(i_file_regex)

    if i_file_paths:
        file_paths.extend(i_file_paths)

s.MayaSceneRegisterBatch(
    'resource_maya_scene_16', file_paths
).execute()
