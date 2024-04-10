# coding:utf-8
import lxcontent.core as ctt_core

import lxresource as bsc_resource

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core
# maya
from .. import core as mya_core
# maya dcc
from ..dcc import objects as mya_dcc_objects


class ScpCbkEnvironment(object):
    KEY = 'workspace environment'

    def __init__(self):
        self._cfg = ctt_core.Content(
            value=bsc_resource.RscExtendConfigure.get_yaml(
                'katana/script/scene'
            )
        )
        self._cfg.do_flatten()

    @classmethod
    def save(cls, data):
        pass

    @classmethod
    def register(cls, data):
        for i_index, (i_key, i_env_key, i_env_value) in enumerate(data):
            bsc_core.EnvBaseMtd.set(
                i_env_key, i_env_value
            )
            bsc_log.Log.trace_method_result(
                cls.KEY,
                'register: key="{}", value="{}"'.format(i_env_key, i_env_value)
            )

    def add_from_resolver(self, *args, **kwargs):
        if 'filename' in kwargs:
            f = kwargs['filename']
        else:
            f = mya_dcc_objects.Scene.get_current_file_path()
        #
        import lxresolver.scripts as rsv_scripts

        return rsv_scripts.ScpEnvironment.get_data(f)

    def add_from_work_environment(self, *args, **kwargs):
        import lxshotgun.scripts as stg_scripts

        task_id = bsc_core.EnvBaseMtd.get(
            'QSM_TASK_ID'
        )
        return stg_scripts.ScpEnvironment.get_data(task_id)

    def add_from_scene(self, *args, **kwargs):
        return False, None

    @mya_core.MyaModifier.undo_run
    def execute(self, *args, **kwargs):
        if mya_core.MyaUtil.get_is_ui_mode():
            fncs = [
                self.add_from_resolver,
                self.add_from_work_environment,
                self.add_from_scene,
            ]
        else:
            fncs = [
                self.add_from_resolver,
                self.add_from_work_environment,
                self.add_from_scene,
            ]

        for i_fnc in fncs:
            i_result, i_data = i_fnc(*args, **kwargs)
            if i_result is True:
                self.register(i_data)
                self.save(i_data)
                return True

        bsc_log.Log.trace_method_error(
            self.KEY, 'failed to load form any where'
        )
