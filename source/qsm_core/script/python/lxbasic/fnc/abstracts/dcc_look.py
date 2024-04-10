# coding:utf-8
import lxcontent.core as ctt_core

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from . import base as bsc_fnc_abs_base


class AbsFncImporterForLookYmlDcc(bsc_fnc_abs_base.AbsFncOptionBase):
    OPTION = dict(
        file='',
        root='',
        #
        material_assign_force=True,
        look_pass='default',
        version='v000',
        #
        auto_rename_node=True
    )

    def __init__(self, option):
        super(AbsFncImporterForLookYmlDcc, self).__init__(option)
        bsc_log.Log.trace_method_result(
            'look-yml-import',
            'file="{}"'.format(self._option['file'])
        )
        file_path = self.get('file')
        if bsc_storage.StgPathMtd.get_is_exists(file_path) is True:
            self._time_tag = bsc_core.TimestampOpt(
                bsc_storage.StgFileOpt(file_path).get_modify_timestamp()
                ).get_as_tag_36()
            self._raw = ctt_core.Content(
                value=self.get('file')
            )
        else:
            raise RuntimeError()

    def get_look_pass_names(self):
        _ = self._raw.get_keys(
            'root.*.properties.customize-attributes.pg_lookpass.enumerate-strings'
        )
        if _:
            key = _[0]
            return self._raw.get(key)
        return []
