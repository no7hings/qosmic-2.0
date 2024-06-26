# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.log as bsc_log

import lxbasic.session as bsc_session

from .. import core as _mya_core


class MainShelf(object):
    KEY = 'qosmic shelf'

    SHELF_NAME = 'Lazy Tool'

    SHELF_NAME_CHS = bsc_core.auto_unicode('懒人工具')
    
    SHELF_KEY = 'Lazy_Tool'

    OLD_SHELF_NAMES = [
        'QSM',
        SHELF_KEY,
        SHELF_NAME_CHS
    ]

    DATA = [
        (
            'general',
            [
                'dcc-tools/maya/qsm-asset-manager',
                'dcc-tools/maya/qsm-lazy-playblast',
            ]
        ),
        (
            'lazy-resource',
            [
                'dcc-tools/maya/qsm-lazy-resource-tool',
            ]
        ),
        (
            'lazy-cfx',
            [
                'dcc-tools/maya/qsm-lazy-cfx-tool',
            ]
        )
    ]

    def __init__(self):
        pass

    def create(self):
        bsc_log.Log.trace_method_result(
            self.KEY, 'create'
        )
        language = bsc_core.EnvBaseMtd.get_ui_language()

        # delete old
        for i in self.OLD_SHELF_NAMES:
            if _mya_core.Shelf.is_exists(i):
                _mya_core.Shelf.delete(i)
        # create new
        if bsc_core.EnvBaseMtd.get_ui_language() == 'chs':
            shelf_name = self.SHELF_NAME_CHS
        else:
            shelf_name = self.SHELF_NAME

        shelf = _mya_core.Shelf.create(shelf_name)

        for i_sep, i_keys in self.DATA:
            _mya_core.Shelf.create_separator(
                shelf,
                annotation=i_sep
            )
            for j_key in i_keys:
                j_args = bsc_session.Hook.get_args(j_key)
                if j_args:
                    j_session, j_fnc = j_args
                    j_label = j_session.get_gui_name_(language)
                    j_tool_tip = j_session.get_gui_tool_tip_(language)
                    j_image = j_session.gui_icon_file
                    j_cmd_script = 'import lxbasic.session as bsc_session; bsc_session.Hook.execute("{}")'.format(j_key)
                    _mya_core.Shelf.create_button(
                        shelf,
                        label=j_label,
                        image=j_image,
                        annotation=j_tool_tip,
                        command=j_cmd_script
                    )


