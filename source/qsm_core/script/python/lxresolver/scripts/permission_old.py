# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

from .. import core as rsv_core


class RsvPermissionMtd(bsc_storage.StgSshMtd):
    @classmethod
    def set_entity_task_create(cls, **kwargs):
        r = rsv_core.RsvBase.generate_root()

        task_directory_paths = r.get_rsv_resource_task_directory_paths(**kwargs)
        for i_task_directory_path in task_directory_paths:
            bsc_storage.StgPathMtd.create_directory(i_task_directory_path)
            bsc_log.Log.trace_method_result(
                'directory create',
                'directory="{}"'.format(i_task_directory_path)
            )

        step_directory_paths = r.get_rsv_resource_step_directory_paths(**kwargs)
        for i_step_directory_path in step_directory_paths:
            i_group_name = '{}_grp'.format(kwargs['step'])
            if i_group_name in cls.GROUP_ID_QUERY:
                i_group_id = cls.GROUP_ID_QUERY[i_group_name]
                i_path = bsc_storage.StgPathMtd.set_map_to_nas(i_step_directory_path)
                i_kwargs = dict(
                    group_id=i_group_id,
                    path=i_path
                )
                cmd = 'chmod -R +a group {group_id} allow dir_gen_all,object_inherit,container_inherit "{path}"'.format(
                    **i_kwargs
                )
                cls._set_nas_cmd_run_(cmd)

    @classmethod
    def set_create(cls, **kwargs):
        r = rsv_core.RsvBase.generate_root()

        step_directory_paths = r.get_rsv_resource_step_directory_paths(**kwargs)
        for i_step_directory_path in step_directory_paths:
            i_group_name = '{}_grp'.format(kwargs['step'])
            i_group_id = cls.GROUP_ID_QUERY[i_group_name]
            i_path = bsc_storage.StgPathMtd.set_map_to_nas(i_step_directory_path)
            i_kwargs = dict(
                group_id=i_group_id,
                path=i_path
            )
            cmd = 'chmod -R +a group {group_id} allow dir_gen_all,object_inherit,container_inherit "{path}"'.format(
                **i_kwargs
            )
            cls._set_nas_cmd_run_(cmd)
