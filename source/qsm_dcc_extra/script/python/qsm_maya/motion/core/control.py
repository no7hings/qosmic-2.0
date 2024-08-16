# coding:utf-8
import re
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

from ... import core as _mya_core

from . import base as _base

from . import mirror_and_flip as _mirror_and_flip


class ControlMotionOpt(_base.MotionBase):
    KEY = 'control motion'

    @classmethod
    def to_control_key(cls, path):
        return path.split('|')[-1].split(':')[-1]

    @classmethod
    def to_control_direction_args(cls, control_key):
        ps = [
            (r'(.*)_L', cls.ControlDirections.Left, '{}_R'),
            (r'(.*)_R', cls.ControlDirections.Right, '{}_L'),
            (r'(.*)_M', cls.ControlDirections.Middle, None),
        ]
        for i_p, i_d, i_f in ps:
            i_r = re.match(i_p, control_key)
            if i_r:
                if i_f is not None:
                    return i_f.format(i_r.group(1)), i_d
                return None, i_d
        return None, cls.ControlDirections.Unknown

    def __init__(self, path):
        self._path = path
        self._namespace = _mya_core.DagNode.to_namespace(self._path)

    def get_data(self, includes=None):
        return _base.Motion.get(self._path, key_includes=includes)

    def apply_data(self, data, **kwargs):
        _base.Motion.apply(self._path, data, **kwargs)

    def transfer_to(self, path_dst, **kwargs):
        data = self.get_data()
        self.__class__(path_dst).apply_data(data, **kwargs)

    def get_curve_node_at(self, atr_name):
        return _mya_core.NodeAttribute.get_source_node(self._path, atr_name, 'animCurve')
    
    def get_all_curve_nodes(self, key_includes=None):
        return _base.Motion.get_all_curve_nodes(self._path, key_includes=key_includes)

    def find_node_at(self, atr_name, depth_maximum=2):
        def rcs_fnc_(path_, depth_):
            if depth_ >= depth_maximum:
                return
            depth_ += 1
            if cmds.nodeType(path_).startswith('animCurve'):
                return path_
            else:
                _paths = cmds.listConnections(path_, destination=0, source=1, skipConversionNodes=1) or []
                for _i_path in _paths:
                    _i_result = rcs_fnc_(_i_path, depth_)
                    if _i_result is not None:
                        return _i_result

        depth = 0

        path_next = _mya_core.NodeAttribute.get_source_node(self._path, atr_name)
        if path_next:
            return rcs_fnc_(path_next, depth)

    def find_transformation_locator_at(self, atr_name, depth_maximum=4):
        def rcs_fnc_(path_, depth_):
            if depth_ >= depth_maximum:
                return
            depth_ += 1
            if cmds.nodeType(path_).startswith('transform'):
                if _mya_core.NodeAttribute.get_is_value(path_, 'qsm_mark', 'move_locator') is True:
                    return path_
            else:
                _paths = cmds.listConnections(path_, destination=0, source=1, skipConversionNodes=1) or []
                for _i_path in _paths:
                    _i_result = rcs_fnc_(_i_path, depth_)
                    if _i_result is not None:
                        return _i_result

        depth = 0

        path_next = _mya_core.NodeAttribute.get_source_node(self._path, atr_name)
        if path_next:
            return rcs_fnc_(path_next, depth)

    def create_control_move_locator(self, locator_path):
        atr_names = [
            'translateX', 'translateY', 'translateZ',
            'rotateX', 'rotateY', 'rotateZ',
            # 'scaleX', 'scaleY', 'scaleZ'
        ]
        nodes = []

        name = _mya_core.DagNode.to_name(self._path)
        matrix_name = '{}_loc_mtx'.format(name)
        matrix_name = _mya_core.Node.create(matrix_name, 'decomposeMatrix')
        nodes.append(matrix_name)
        _mya_core.Connection.create(
            locator_path+'.worldMatrix[0]', matrix_name+'.inputMatrix'
        )
        for i_atr_name in atr_names:
            i_atr_name_output = 'output'+i_atr_name[0].upper()+i_atr_name[1:]

            i_animation_curve = self.get_curve_node_at(i_atr_name)

            i_plug_name = '{}_{}_loc_plg'.format(name, i_atr_name)
            i_plug_name = _mya_core.Node.create(i_plug_name, 'plusMinusAverage')
            nodes.append(i_plug_name)
            # keyframe or value
            if i_animation_curve is not None:
                _mya_core.Connection.create(
                    i_animation_curve+'.output', i_plug_name+'.input1D[0]'
                )
            else:
                i_value = _mya_core.NodeAttribute.get_value(self._path, i_atr_name)
                _mya_core.NodeAttribute.set_value(
                    i_plug_name, 'input1D[0]', i_value
                )
            # matrix
            _mya_core.Connection.create(
                matrix_name+'.'+i_atr_name_output, i_plug_name+'.input1D[1]'
            )
            i_value_offset = _mya_core.NodeAttribute.get_value(
                matrix_name, i_atr_name_output
            )
            _mya_core.NodeAttribute.set_value(
                i_plug_name, 'input1D[2]', -i_value_offset
            )
            _mya_core.Connection.create(
                i_plug_name+'.output1D', self._path+'.'+i_atr_name
            )

        container_name = '{}_loc_dgc'.format(name)
        container_node = _mya_core.Container.create(
            container_name, 'out_plusMinusAverage.png'
        )
        container_path = _mya_core.DagNode.parent_to(
            container_node, locator_path
        )
        _mya_core.Container.add_nodes(container_path, nodes)

    def remove_control_move_locator(self):
        atr_names = [
            'translateX', 'translateY', 'translateZ',
            'rotateX', 'rotateY', 'rotateZ',
        ]
        locator_paths = []

        name = _mya_core.DagNode.to_name(self._path)

        matrix_name = '{}_loc_mtx'.format(name)
        for i_atr_name in atr_names:
            i_locator_name = self.find_transformation_locator_at(i_atr_name, depth_maximum=5)
            if i_locator_name is None:
                continue

            i_atr_name_output = 'output'+i_atr_name[0].upper()+i_atr_name[1:]

            i_locator_path = _mya_core.DagNode.to_path(i_locator_name)
            locator_paths.append(i_locator_path)

            i_plug_name = '{}_{}_loc_plg'.format(name, i_atr_name)

            i_value_current = _mya_core.NodeAttribute.get_value(matrix_name, i_atr_name_output)
            i_value_offset = _mya_core.NodeAttribute.get_value(i_plug_name, 'input1D[2]')

            # maybe attribute has no animation curve
            i_animation_curve = self.find_node_at(i_atr_name, depth_maximum=5)
            if i_animation_curve is not None:
                _mya_core.NodeAttribute.break_source(
                    self._path, i_atr_name
                )
                _mya_core.Connection.create(
                    i_animation_curve+'.output', self._path+'.'+i_atr_name
                )
                _mya_core.NodeAttributeAnmCurveOpt(
                    self._path, i_atr_name
                ).offset_all_values(
                    i_value_current+i_value_offset
                )
                cmds.select(i_animation_curve)
                cmds.dgdirty()
            else:
                i_value = _mya_core.NodeAttribute.get_value(i_plug_name, 'input1D[0]')
                _mya_core.NodeAttribute.break_source(
                    self._path, i_atr_name
                )
                _mya_core.NodeAttribute.set_value(
                    self._path, i_atr_name, i_value+i_value_current+i_value_offset
                )

        if locator_paths:
            [_mya_core.Node.delete(x) for x in set(locator_paths)]
            cmds.select(self._path)
            cmds.dgdirty()

    def find_one_control(self, control_key):
        return self.find_one_control_fnc(control_key, self._namespace)

    def mirror_auto(self, **kwargs):
        path_src = self._path
        ctr_key_src = self.to_control_key(path_src)
        ctr_key_dst, direction = self.to_control_direction_args(ctr_key_src)
        # side
        if ctr_key_dst is not None:
            path_dst = self.find_one_control(ctr_key_dst)
            if path_dst is None:
                bsc_log.Log.trace_method_result(
                    self.KEY, 'control for "{}" is not found'.format(ctr_key_dst)
                )
                return
            # left or right
            if direction in {
                self.ControlDirections.Left, self.ControlDirections.Right
            }:
                _mirror_and_flip.MirrorAndFlip.mirror_side(path_src, path_dst, **kwargs)
        else:
            if direction in {
                self.ControlDirections.Middle
            }:
                _mirror_and_flip.MirrorAndFlip.mirror_middle(path_src, **kwargs)

    def mirror_side(self, scheme, **kwargs):
        path_src = self._path
        ctr_key_src = self.to_control_key(path_src)
        if scheme == self.MirrorSchemes.LeftToRight:
            ctr_key_dst, direction = self.to_control_direction_args(ctr_key_src)
            # check is side
            if ctr_key_dst is not None:
                path_dst = self.find_one_control(ctr_key_dst)
                if path_dst is None:
                    bsc_log.Log.trace_method_result(
                        self.KEY, 'control for "{}" is not found'.format(ctr_key_dst)
                    )
                    return
                    # left
                if direction == self.ControlDirections.Left:
                    _mirror_and_flip.MirrorAndFlip.mirror_side(path_src, path_dst, **kwargs)
        elif scheme == self.MirrorSchemes.RightToLeft:
            ctr_key_dst, direction = self.to_control_direction_args(ctr_key_src)
            # check is side
            if ctr_key_dst is not None:
                path_dst = self.find_one_control(ctr_key_dst)
                if path_dst is None:
                    bsc_log.Log.trace_method_result(
                        self.KEY, 'control for "{}" is not found'.format(ctr_key_dst)
                    )
                    return
                    # right
                if direction == self.ControlDirections.Right:
                    _mirror_and_flip.MirrorAndFlip.mirror_side(path_src, path_dst, **kwargs)

    def mirror_middle(self, **kwargs):
        path_src = self._path
        ctr_key_src = self.to_control_key(path_src)
        _, direction = self.to_control_direction_args(ctr_key_src)
        if direction == self.ControlDirections.Middle:
            _mirror_and_flip.MirrorAndFlip.mirror_middle(path_src, **kwargs)


class ControlsMotionOpt(_base.MotionBase):
    KEY = 'controls motion'

    @classmethod
    def get_args_from_selection(cls):
        dict_ = {}
        _ = cmds.ls(selection=1, long=1)
        for i_path in _:
            dict_.setdefault(
                _mya_core.DagNode.to_namespace(i_path), []
            ).append(i_path)
        return dict_

    @classmethod
    def get_args_from_selection_for_mirror(cls):
        dict_ = {}
        _ = cmds.ls(selection=1, long=1)
        for i_path in _:
            # ignore neither has "translate", "rotate"
            if cmds.objExists(i_path+'.translate') is False and cmds.objExists(i_path+'.rotate') is False:
                continue

            dict_.setdefault(
                _mya_core.DagNode.to_namespace(i_path), []
            ).append(i_path)
        return dict_

    def __init__(self, namespace, paths):
        self._namespace = namespace
        self._path_set = set(paths)

    def find_one_control(self, control_key):
        return self.find_one_control_fnc(control_key, self._namespace)

    def get_data(self):
        dict_ = {}
        for i_path in self._path_set:
            i_control_opt = ControlMotionOpt(i_path)
            i_data = i_control_opt.get_data()
            i_control_key = ControlMotionOpt.to_control_key(i_path)
            dict_[i_control_key] = i_data
        return dict_

    def export_to(self, file_path):
        bsc_storage.StgFileOpt(file_path).set_write(self.get_data())

    def load_from(self, file_path, **kwargs):
        self.apply_data(
            bsc_storage.StgFileOpt(file_path).set_read(), **kwargs
        )

    @_mya_core.Undo.execute
    def apply_data(self, data, **kwargs):
        bsc_log.Log.trace_method_result(
            self.KEY,
            'apply data: "{}"'.format(', '.join(['{}={}'.format(k, v) for k, v in kwargs.items()]))
        )

        control_key_excludes = kwargs.pop('control_key_excludes') if 'control_key_excludes' in kwargs else None

        for i_control_path in self._path_set:
            i_control_key = ControlMotionOpt.to_control_key(i_control_path)
            if control_key_excludes:
                if i_control_key in control_key_excludes:
                    continue

            if i_control_key in data:
                i_data = data[i_control_key]
                ControlMotionOpt(i_control_path).apply_data(i_data, **kwargs)

    @_mya_core.Undo.execute
    def mirror_auto(self, **kwargs):
        for i_path in self._path_set:
            ControlMotionOpt(i_path).mirror_auto(**kwargs)

    @_mya_core.Undo.execute
    def mirror_left_to_right(self, **kwargs):
        for i_path in self._path_set:
            # ignore neither has "translate", "rotate"
            if cmds.objExists(i_path+'.translate') is False and cmds.objExists(i_path+'.rotate') is False:
                continue
            ControlMotionOpt(i_path).mirror_side(
                self.MirrorSchemes.LeftToRight, **kwargs
            )

    @_mya_core.Undo.execute
    def mirror_middle(self, **kwargs):
        for i_path in self._path_set:
            # ignore neither has "translate", "rotate"
            if cmds.objExists(i_path+'.translate') is False and cmds.objExists(i_path+'.rotate') is False:
                continue
            ControlMotionOpt(i_path).mirror_middle(**kwargs)

    @_mya_core.Undo.execute
    def mirror_right_to_left(self, **kwargs):
        for i_path in self._path_set:
            # ignore neither has "translate", "rotate"
            if cmds.objExists(i_path+'.translate') is False and cmds.objExists(i_path+'.rotate') is False:
                continue
            ControlMotionOpt(i_path).mirror_side(
                self.MirrorSchemes.RightToLeft, **kwargs
            )

    @_mya_core.Undo.execute
    def flip(self, **kwargs):
        # mark data first
        data = self.get_data()
        for i_control_key, i_data in data.items():
            i_path = self.find_one_control(i_control_key)
            # ignore neither has "translate", "rotate"
            if cmds.objExists(i_path+'.translate') is False and cmds.objExists(i_path+'.rotate') is False:
                continue

            ControlMotionOpt(i_path).mirror_auto(data_override=i_data, **kwargs)


class MirrorPasteOpt(_base.MotionBase):
    def find_one_control(self, control_key):
        return self.find_one_control_fnc(control_key, self._namespace)

    def __init__(self, namespace):
        self._namespace = namespace

    @_mya_core.Undo.execute
    def apply_data(self, data, **kwargs):
        for i_control_key, i_data in data.items():
            i_path = self.find_one_control(i_control_key)
            # ignore neither has "translate", "rotate"
            if cmds.objExists(i_path+'.translate') is False and cmds.objExists(i_path+'.rotate') is False:
                continue

            ControlMotionOpt(i_path).mirror_auto(data_override=i_data, **kwargs)

    def load_from(self, file_path, **kwargs):
        self.apply_data(
            bsc_storage.StgFileOpt(file_path).set_read(), **kwargs
        )


class ControlsBake(object):
    def __init__(self, paths):
        self._paths = paths

    def execute(self, start_frame, end_frame, frame_extend=0):
        """
bakeResults
-simulation true
-t "0:32"
-sampleBy 1
-oversamplingRate 1
-disableImplicitControl true
-preserveOutsideKeys true
-sparseAnimCurveBake false
-removeBakedAttributeFromLayer false
-removeBakedAnimFromLayer false
-bakeOnOverrideLayer false
-minimizeRotation true
-controlPoints false
-shape true
{"sam_Skin:Main"};
        """
        cmds.bakeResults(
            self._paths,
            time=(start_frame-frame_extend, end_frame+frame_extend),
            simulation=1,
            sampleBy=1,
            oversamplingRate=1,
            disableImplicitControl=1,
            preserveOutsideKeys=1,
            sparseAnimCurveBake=0,
            removeBakedAttributeFromLayer=0,
            removeBakedAnimFromLayer=0,
            bakeOnOverrideLayer=0,
            minimizeRotation=1,
            controlPoints=0,
            shape=0,
        )

    @classmethod
    def test(cls):
        cls(['sam_Skin:FKKnee_R', 'sam_Skin:FKKnee_L']).execute(0, 32)
