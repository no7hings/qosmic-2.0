# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.log as bsc_log

import lxbasic.resource as bsc_resource

import lxbasic.session as bsc_session

import lxgui.core as gui_core

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
                'dcc-tools/maya/qsm-lazy-playblast-tool',
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

    def create_old(self):
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

        c = bsc_resource.RscExtendConfigure.get_as_content(
            'maya/lazy-shelf'
        )

        build_data = c.get('build')

        for i_k, i_v in build_data.items():
            i_tool_tip = gui_core.GuiUtil.choice_tool_tip(
                language, i_v
            )

            _mya_core.Shelf.create_separator(
                shelf,
                annotation=i_tool_tip,
            )
            i_tools = c.get('build.{}.tools'.format(i_k))

            for j_k, j_v in i_tools.items():
                j_name = gui_core.GuiUtil.choice_name(language, j_v)
                j_tool_tip = gui_core.GuiUtil.choice_tool_tip(language, j_v)
                j_script = j_v['script']
                j_dbl_script = j_v.get('dbl_script') or ''
                i_button_style = j_v.get('button_style') or 'text_and_icon'
                if i_button_style == 'icon':
                    j_icon = gui_core.GuiIcon.get(j_v['icon'])
                    j_button = _mya_core.Shelf.create_button(
                        shelf,
                        label=j_name,
                        image=j_icon,
                        annotation=j_tool_tip,
                        command=j_script,
                        doubleClickCommand=j_dbl_script,
                        style='iconOnly',
                    )
                elif i_button_style == 'text_and_icon':
                    if language == 'chs':
                        j_button_name = j_v['button_name_chs']
                    else:
                        j_button_name = j_v['button_name']

                    j_icon = gui_core.GuiIcon.get(j_v['icon'])
                    background_rgb = bsc_core.RawTextOpt(j_name).to_rgb_1(maximum=1.0)
                    j_button = _mya_core.Shelf.create_button(
                        shelf,
                        label=j_name,
                        image=j_icon,
                        annotation=j_tool_tip,
                        command=j_script,
                        doubleClickCommand=j_dbl_script,
                        style='textOnly',
                        imageOverlayLabel=j_button_name,
                        overlayLabelColor=(1.0, 1.0, 1.0),
                        overlayLabelBackColor=(background_rgb[0], background_rgb[1], background_rgb[2], 1.0),
                        font='boldLabelFont',
                        align='center',
                    )
                else:
                    raise RuntimeError()

                action_data = j_v.get('actions')
                if action_data:
                    for k_k, k_v in action_data.items():
                        if language == 'chs':
                            k_name = k_v['name_chs']
                        else:
                            k_name = k_v['name']
                        _mya_core.Shelf.create_button_action(
                            j_button, k_name, k_v['script']
                        )
