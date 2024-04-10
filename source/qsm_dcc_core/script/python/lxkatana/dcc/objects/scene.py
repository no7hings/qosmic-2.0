# coding:utf-8
import six

import types

import lxbasic.log as bsc_log

import lxbasic.dcc.objects as bsc_dcc_objects

import lxbasic.dcc.abstracts as bsc_dcc_abstracts

import lxuniverse.core as unr_core

import lxuniverse.objects as unv_objects

import lxgui.core as gui_core
# katana
from ...core.wrap import *

from ... import core as ktn_core


# noinspection PyUnusedLocal
class Scene(bsc_dcc_abstracts.AbsDccNodeScene):
    @classmethod
    def get_current_file_path(cls):
        _ = NodegraphAPI.GetProjectFile()
        if isinstance(_, six.string_types):
            return _.replace('\\', '/')

    @classmethod
    def set_file_path(cls, file_path):
        pass

    @classmethod
    def open_file(cls, file_path):
        file_obj = bsc_dcc_objects.StgFile(file_path)
        bsc_log.Log.trace_method_result(
            'katana-file open',
            'file="{}" is started'.format(file_path)
        )
        KatanaFile.Load(file_obj.path)
        bsc_log.Log.trace_method_result(
            'katana-file open',
            'file="{}" is completed'.format(file_path)
        )

    @classmethod
    def save_file(cls):
        file_path = cls.get_current_file_path()
        bsc_log.Log.trace_method_result(
            'katana-file save',
            'file="{}" is started'.format(file_path)
        )
        if file_path:
            KatanaFile.Save(file_path)
            bsc_log.Log.trace_method_result(
                'katana-file save',
                'file="{}" is completed'.format(file_path)
            )
        else:
            pass

    @classmethod
    def save_to_file(cls, file_path):
        file_obj = bsc_dcc_objects.StgFile(file_path)
        file_obj.create_directory()
        bsc_log.Log.trace_method_result(
            'katana-file save-to',
            'file="{}" is started'.format(file_path)
        )
        KatanaFile.Save(file_obj.path)
        bsc_log.Log.trace_method_result(
            'katana-file save-to',
            'file="{}" is completed'.format(file_path)
        )

    @classmethod
    def set_file_export_to(cls, file_path):
        # cls.save_file()
        src_file_path = cls.get_current_file_path()
        src_file_obj = bsc_dcc_objects.StgFile(src_file_path)
        src_file_obj.copy_to_file(
            file_path, replace=True
        )

    @classmethod
    def get_scene_is_dirty(cls):
        return KatanaFile.IsFileDirty()

    @classmethod
    def new_file(cls):
        return KatanaFile.New()

    @classmethod
    def set_current_frame(cls, frame):
        NodegraphAPI.GetRootNode().getParameter('currentTime').setValue(frame, 0)

    @classmethod
    def get_current_frame(cls):
        return NodegraphAPI.GetRootNode().getParameter('currentTime').getValue(0)

    @classmethod
    def get_frame_range(cls, frame=None):
        if isinstance(frame, (tuple, list)):
            star_frame, end_frame = frame
        elif isinstance(frame, (int, float)):
            star_frame = end_frame = frame
        else:
            star_frame = end_frame = cls.get_current_frame()
        return star_frame, end_frame

    @classmethod
    def set_frame_range(cls, *args):
        if len(args) == 2:
            star_frame, end_frame = args
        elif len(args) == 1:
            star_frame = end_frame = args
        else:
            raise TypeError()
        #
        NodegraphAPI.GetRootNode().getParameter('inTime').setValue(star_frame, 0)
        NodegraphAPI.GetRootNode().getParameter('workingInTime').setValue(star_frame, 0)
        NodegraphAPI.GetRootNode().getParameter('outTime').setValue(end_frame, 0)
        NodegraphAPI.GetRootNode().getParameter('workingOutTime').setValue(end_frame, 0)

    @classmethod
    def get_objs_by_type(cls, obj_type_name):
        if isinstance(obj_type_name, six.string_types):
            obj_type_names = [obj_type_name]
        elif isinstance(obj_type_name, (tuple, list)):
            obj_type_names = obj_type_name
        else:
            raise TypeError()

        lis = []
        for obj_type_name in obj_type_names:
            _ = NodegraphAPI.GetAllNodesByType(obj_type_name) or []
            for ktn_node in _:
                lis.append(ktn_node)
        return lis

    #
    FILE_CLS = bsc_dcc_objects.StgFile
    UNIVERSE_CLS = unv_objects.ObjUniverse

    def __init__(self, *args, **kwargs):
        super(Scene, self).__init__(*args, **kwargs)

    def _load_from_location_fnc(self, ktn_obj, root, include_obj_type=None):
        self._scene_graph_opt = ktn_core.KtnStageOpt(ktn_obj)
        tvl = self._scene_graph_opt._get_traversal_(root)
        while tvl.valid():
            i_obj_path = tvl.getLocationPath()
            i_obj_type_name = tvl.getLocationData().getAttrs().getChildByName('type').getData()[0]
            # print i_obj_type_name
            _obj = self._create_obj_(i_obj_type_name, i_obj_path)
            _obj.obj_opt = self._scene_graph_opt.generate_obj_opt(i_obj_path)
            tvl.next()

    def _create_obj_(self, obj_type_name, obj_path):
        obj_category_name = unr_core.UnrObjCategory.LYNXI
        #
        obj_category = self.universe.generate_obj_category(obj_category_name)
        obj_type = obj_category.generate_type(obj_type_name)
        _obj = obj_type.create_obj(obj_path)
        #
        if ktn_core.KtnUtil.get_is_ui_mode() is True:
            import lxgui.qt.core as gui_qt_core

            _obj.set_gui_attribute(
                'icon', gui_qt_core.GuiQtKatana.generate_qt_icon_by_name(obj_type_name)
            )
        return _obj

    @classmethod
    def set_file_open_with_dialog(cls, file_path):
        def yes_fnc_():
            cls.save_file()
            cls.open_file(file_path)

        #
        def no_fnc_():
            cls.open_file(file_path)

        #
        w = gui_core.GuiDialog.create(
            label='Save',
            content=u'Scene has been modified, Do you want to save changed to "{}"'.format(
                cls.get_current_file_path()
            ),
            window_size=(480, 160),
            #
            yes_method=yes_fnc_,
            no_method=no_fnc_,
            #
            yes_label='Save',
            no_label='Don\'t save'
        )

        result = w.get_result()
        if result is True:
            pass

    @classmethod
    def new_file_with_dialog(cls, file_path, post_method=None):
        def pos_method_run_fnc_():
            if isinstance(post_method, (types.FunctionType, types.MethodType)):
                post_method(file_path)

        #
        def yes_fnc_():
            cls.save_file()
            #
            cls.new_file()
            #
            f = bsc_dcc_objects.StgFile(file_path)
            f.create_directory()
            #
            pos_method_run_fnc_()
            #
            cls.save_to_file(file_path)

        #
        def no_fnc_():
            cls.new_file()
            #
            f = bsc_dcc_objects.StgFile(file_path)
            f.create_directory()
            #
            pos_method_run_fnc_()
            #
            cls.save_to_file(file_path)

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
    def save_file_with_dialog(cls):
        def yes_fnc_():
            cls.save_file()

        #
        def no_fnc_():
            pass

        #
        if cls.get_scene_is_dirty():
            w = gui_core.GuiDialog.create(
                label='Save Changed',
                content=(
                    u'Scene has been modified, Do you want to save changed to "{}"'
                ).format(
                    cls.get_current_file_path()
                ),
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                window_size=(480, 160),
                #
                yes_method=yes_fnc_,
                no_method=no_fnc_,
                #
                yes_label='Save',
                no_label='Don\'t save'
            )

            result = w.get_result()
            if result is True:
                pass

    @classmethod
    def import_from_file(cls, file_path):
        KatanaFile.Import(file_path)


# noinspection PyUnusedLocal
class Selection(object):
    def __init__(self, *args):
        self._obj_paths = args[0]
        pathsep = ktn_core.KtnUtil.OBJ_PATHSEP
        self._node_graph_ktn_objs = []
        self._scene_graph_obj_paths = []
        for i in self._obj_paths:
            if i.startswith('/rootNode'):
                node_graph_ktn_obj = NodegraphAPI.GetNode(i.split(pathsep)[-1])
                if node_graph_ktn_obj is not None:
                    self._node_graph_ktn_objs.append(node_graph_ktn_obj)
            elif i.startswith('/root'):
                self._scene_graph_obj_paths.append(str(i))

    @classmethod
    def get_selected_paths(cls, include=None):
        return [i.getName() for i in NodegraphAPI.GetAllSelectedNodes() or []]

    def select_all(self):
        if self._node_graph_ktn_objs:
            NodegraphAPI.SetAllSelectedNodes(
                self._node_graph_ktn_objs
            )
            #
            ktn_obj = self._node_graph_ktn_objs[-1]
            #
            NodegraphAPI.SetNodeEdited(
                ktn_obj,
                edited=True, exclusive=True
            )
            #
            if hasattr(ktn_obj, 'getParent'):
                parent_ktn_obj = ktn_obj.getParent()
                ktn_core.GuiNodeGraphTabOpt().set_current_node(parent_ktn_obj)
                ktn_core.GuiNodeGraphTabOpt().set_selection_view_fit()
        #
        if self._scene_graph_obj_paths:
            ktn_core.KtnSGSelectionOpt(
                self._scene_graph_obj_paths
            ).select_all()

    @classmethod
    def set_clear(cls):
        NodegraphAPI.SetAllSelectedNodes([])
        ktn_core.KtnSGSelectionOpt.set_clear()
