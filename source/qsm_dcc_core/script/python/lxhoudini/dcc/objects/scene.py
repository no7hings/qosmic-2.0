# coding:utf-8
import os

import re

import types

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.dcc.abstracts as bsc_dcc_abstracts

import lxbasic.dcc.objects as bsc_dcc_objects

import lxuniverse.objects as unv_objects

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core
# houdini
from ...core.wrap import *

from ... import core as hou_core


__all__ = [
    'Scene',
    'Selection',
]


# noinspection RegExpSimplifiable,PyUnusedLocal
class Scene(bsc_dcc_abstracts.AbsDccNodeScene):
    FILE_CLS = bsc_dcc_objects.StgFile
    UNIVERSE_CLS = unv_objects.ObjUniverse

    def __init__(self):
        super(Scene, self).__init__()

    @classmethod
    def get_houdini_absolutely_path_with_path(cls, path):
        path_ = path
        if '$' in path_:
            # noinspection RegExpRedundantEscape
            re_pattern = re.compile(r'[\$](.*?)[\/]', re.S)
            results = re.findall(re_pattern, path_)
            for environ_key in results:
                variant = '${}'.format(environ_key)
                if environ_key in os.environ:
                    environ_value = os.environ[environ_key]
                    path_ = path_.replace(variant, environ_value)
                else:
                    bsc_log.Log.trace_warning('Variant "{}" in "{}" is Not Available.'.format(variant, path_))
        return path_

    @classmethod
    def get_reference_files(cls):
        pass

    @classmethod
    def get_frame_range(cls):
        return hou.playbar.frameRange()

    @classmethod
    def set_frame_range(cls, start_frame, end_frame):
        hou.playbar.setFrameRange(start_frame, end_frame)
        hou.playbar.setPlaybackRange(start_frame, end_frame)
        hou.setFrame(start_frame)

    @classmethod
    def get_current_file_path(cls):
        return hou.hipFile.path()

    @classmethod
    def get_scene_is_dirty(cls):
        return hou.hipFile.hasUnsavedChanges()

    @classmethod
    def new_file(cls):
        hou.hipFile.clear(suppress_save_prompt=True)

    @classmethod
    def set_new_file_create_with_dialog_(cls, file_path):
        hou.hipFile.clear(suppress_save_prompt=False)

    @classmethod
    def new_file_with_dialog(cls, file_path, post_method=None):
        def pos_method_run_fnc_():
            if isinstance(post_method, (types.FunctionType, types.MethodType)):
                post_method(file_path)

        def yes_fnc_():
            hou.hipFile.save()
            #
            hou.hipFile.clear(suppress_save_prompt=True)
            #
            f = bsc_dcc_objects.StgFile(file_path)
            f.create_directory()
            #
            pos_method_run_fnc_()
            #
            hou.hipFile.setName(file_path)

        #
        def no_fnc_():
            hou.hipFile.clear(suppress_save_prompt=True)
            #
            f = bsc_dcc_objects.StgFile(file_path)
            f.create_directory()
            #
            pos_method_run_fnc_()
            #
            hou.hipFile.setName(file_path)

        #
        if cls.get_scene_is_dirty() is True:
            w = gui_core.GuiDialog.create(
                label='New',
                content=u'Scene has been modified, Do you want to save changed to "{}"'.format(
                    cls.get_current_file_path()
                ),
                window_size=(480, 160),
                #
                yes_method=yes_fnc_,
                no_method=no_fnc_,
                #
                yes_label='Save and new',
                no_label='Don\'t save and new'
            )
        else:
            no_fnc_()

    @classmethod
    def set_file_open_with_dialog(cls, file_path):
        pass

    @classmethod
    def save_to_file(cls, file_path):
        hou.hipFile.save(file_path)
        bsc_log.Log.trace_method_result(
            'scene save',
            u'file="{}"'.format(file_path)
        )

    @classmethod
    def set_file_save_with_dialog(cls):
        if cls.get_scene_is_dirty():
            if cls.get_is_default():
                f = gui_qt_core.QtWidgets.QFileDialog()
                s = f.getSaveFileName(
                    gui_qt_core.GuiQtHoudini.get_qt_main_window(),
                    caption='Save File',
                    dir=hou.hipFile.path(),
                    filter="Houdini Files (*.hip, *.hipnc)"
                )
                if s:
                    _ = s[0]
                    cls.save_to_file(_)
            else:
                pass

    @classmethod
    def get_default_file_path(cls):
        # /home/dongchangbao/untitled.hip
        user_directory_path = bsc_core.SysBaseMtd.get_home_directory()
        return '{}/untitled.hip'.format(user_directory_path)

    @classmethod
    def get_is_default(cls):
        return cls.get_current_file_path() == cls.get_default_file_path()

    @classmethod
    def open_file(cls, file_path):
        hou.hipFile.load(file_path)


class Selection(object):
    def __init__(self, *args):
        self._paths = args[0]

    @classmethod
    def _get_current_network_edit_(cls):
        for i in hou.ui.currentPaneTabs():
            if isinstance(i, hou.NetworkEditor):
                return i

    def select_all(self):
        [hou.node(i).setSelected(True) for i in self._paths]
        path = self._paths[-1]
        if hou.node(path) is not None:
            network_editor = self._get_current_network_edit_()
            if network_editor is not None:
                hou_node = hou.node(path)
                network_editor.setCurrentNode(hou_node)
                network_editor.homeToSelection()

    @classmethod
    def set_clear(cls):
        hou.clearAllSelected()

    @classmethod
    def get_selected_geos(cls):
        def add_fnc_(obj_):
            _path = obj_.path()
            if _path not in paths:
                paths.append(_path)
                lis.append(obj_)

        def sub_fnc_(obj_):
            _type_string = obj_.type().nameWithCategory()
            if _type_string == 'Object/geo':
                add_fnc_(obj_)
            elif _type_string == 'Object/instance':
                _obj = obj_.parm('instancepath').evalAsNode()
                if _obj is not None:
                    if _obj.type().nameWithCategory() == 'Object/geo':
                        add_fnc_(_obj)
            else:
                geo_objs = hou_core.HouBase.get_descendants(i, include=['Object/geo', 'Object/instance'])
                [sub_fnc_(_i) for _i in geo_objs]

        _ = hou.selectedNodes()
        paths = []
        lis = []
        for i in _:
            sub_fnc_(i)

        return lis

    @classmethod
    def get_selected_alembics(cls):
        def add_fnc_(obj_):
            _path = obj_.path()
            if _path not in paths:
                paths.append(_path)
                lis.append(obj_)

        paths = []
        lis = []
        geos = cls.get_selected_geos()
        for geo in geos:
            alembics = hou_core.HouBase.get_descendants(geo, include='Sop/alembic')
            [add_fnc_(i) for i in alembics]
        return lis
