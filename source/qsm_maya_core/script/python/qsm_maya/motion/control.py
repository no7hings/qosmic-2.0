# coding:utf-8
import re
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

from .. import core as _mya_core

from ..general import core as _mya_gnl_core

from . import base as _base

from . import mirror_and_flip as _mirror_and_flip


class ControlNamespaceExtra(object):
    @classmethod
    def find_one_control_fnc(cls, control_key, namespace):
        if namespace:
            _ = cmds.ls('{}:{}'.format(namespace, control_key), long=1)
            if _:
                return _[0]
        else:
            _ = cmds.ls(control_key, long=1)
            if _:
                return _[0]

    def _init_namespace_extra(self, namespace):
        self._namespace = namespace

    def find_one_control(self, control_key):
        return self.find_one_control_fnc(control_key, self._namespace)


class ControlMotionOpt(
    ControlNamespaceExtra,
    _base.AbsMotion
):
    LOG_KEY = 'control motion'

    @classmethod
    def to_control_key(cls, path):
        return path.split('|')[-1].split(':')[-1]

    @classmethod
    def to_control_direction_args(cls, control_key):
        # todo: set "Main" as middle?
        # if control_key == 'Main':
        #     return None, cls.ControlDirections.Middle

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
        self._init_namespace_extra(_mya_core.DagNode.extract_namespace(self._path))

    def generate_motion_properties(self, key_includes=None):
        return _base.NodeMotion.generate_motion_properties_fnc(self._path, key_includes)

    def generate_pose_properties(self, key_includes=None):
        return _base.NodeMotion.generate_pose_properties_fnc(self._path, key_includes)

    def apply_motion_properties(self, data, **kwargs):
        _base.NodeMotion.apply_motion_properties_fnc(self._path, data,  **kwargs)

    def apply_pose_properties(self, data, **kwargs):
        _base.NodeMotion.apply_pose_properties_fnc(self._path, data, **kwargs)

    def get_curve_node_at(self, atr_name):
        return _mya_core.NodeAttribute.get_source_node(self._path, atr_name, 'animCurve')
    
    def get_all_curve_nodes(self, key_includes=None):
        return _base.NodeMotion.get_all_curve_nodes(self._path, key_includes=key_includes)

    # move
    def connect_move_locator(self, locator_path):
        atr_names = [
            'translateX', 'translateY', 'translateZ',
            'rotateX', 'rotateY', 'rotateZ',
            # 'scaleX', 'scaleY', 'scaleZ'
        ]
        nodes = []

        path = self._path

        name = _mya_core.DagNode.to_name(path)
        matrix_name = '{}_loc_mtx'.format(name)
        matrix_name = _mya_core.Node.create(matrix_name, 'decomposeMatrix')
        nodes.append(matrix_name)
        _mya_core.Connection.create(
            locator_path+'.worldMatrix[0]', matrix_name+'.inputMatrix'
        )
        for i_atr_name in atr_names:
            i_atr_name_output = 'output'+i_atr_name[0].upper()+i_atr_name[1:]

            i_curve = _mya_core.NodeAttributeKeyframe.find_curve_node(path, i_atr_name)
            i_layer = _mya_core.NodeAttributeKeyframe.find_layer_node(path, i_atr_name)

            i_plug_name = '{}_{}_loc_plg'.format(name, i_atr_name)
            i_plug_name = _mya_core.Node.create(i_plug_name, 'plusMinusAverage')
            nodes.append(i_plug_name)
            # keyframe or value
            if i_layer is not None:
                i_source = _mya_core.NodeAttribute.get_source(path, i_atr_name)
                _mya_core.NodeAttribute.connect_from(
                    i_plug_name, 'input1D[0]', i_source
                )
            elif i_curve is not None:
                i_source = _mya_core.NodeAttribute.get_source(path, i_atr_name)
                _mya_core.NodeAttribute.connect_from(
                    i_plug_name, 'input1D[0]', i_source
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

    def find_move_curve_node_at(self, atr_name, depth_maximum=2):
        def rcs_fnc_(path_, depth_):
            if depth_ >= depth_maximum:
                return

            depth_ += 1
            if cmds.nodeType(path_).startswith('animBlendNodeAdditive'):
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

    def find_move_layer_node_at(self, atr_name, depth_maximum=2):
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

    def find_move_locator_at(self, atr_name, depth_maximum=4):
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

    def remove_move_locator(self):
        atr_names = [
            'translateX', 'translateY', 'translateZ',
            'rotateX', 'rotateY', 'rotateZ',
        ]
        locator_paths = []

        path = self._path
        name = _mya_core.DagNode.to_name(self._path)

        matrix_name = '{}_loc_mtx'.format(name)
        for i_atr_name in atr_names:
            i_locator_name = self.find_move_locator_at(i_atr_name, depth_maximum=5)
            if i_locator_name is None:
                continue

            i_atr_name_output = 'output'+i_atr_name[0].upper()+i_atr_name[1:]

            i_locator_path = _mya_core.DagNode.to_path(i_locator_name)
            locator_paths.append(i_locator_path)

            i_plug_name = '{}_{}_loc_plg'.format(name, i_atr_name)

            i_value_current = _mya_core.NodeAttribute.get_value(matrix_name, i_atr_name_output)
            i_value_offset = _mya_core.NodeAttribute.get_value(i_plug_name, 'input1D[2]')

            # maybe attribute has no animation curve?
            i_layer = self.find_move_layer_node_at(i_atr_name, depth_maximum=5)
            i_curve = self.find_move_curve_node_at(i_atr_name, depth_maximum=5)
            if i_layer is not None:
                i_source = _mya_core.NodeAttribute.get_source(i_plug_name, 'input1D[0]')
                # maybe use break connect, ignore it
                if not i_source:
                    continue

                _mya_core.NodeAttribute.break_source(
                    path, i_atr_name
                )
                # connect layer
                _mya_core.Connection.create(
                    i_source, path+'.'+i_atr_name
                )
                # offset curve
                i_main_curve = _mya_core.NodeAttributeKeyframe.find_curve_node(path, i_atr_name)
                if i_main_curve:
                    _mya_core.AnmCurveNodeOpt(i_main_curve).offset_all_values(
                        i_value_current+i_value_offset
                    )
                    cmds.select(i_layer)
                    cmds.dgdirty()
                else:
                    # original value
                    i_value = _mya_core.NodeAttribute.get_value(i_plug_name, 'input1D[0]')
                    _mya_core.NodeAttribute.set_value(
                        path, i_atr_name, i_value+i_value_current+i_value_offset
                    )
            elif i_curve is not None:
                i_source = _mya_core.NodeAttribute.get_source(i_plug_name, 'input1D[0]')
                # maybe use break connect, ignore it
                if not i_source:
                    continue

                _mya_core.NodeAttribute.break_source(
                    path, i_atr_name
                )
                _mya_core.Connection.create(
                    i_source, path+'.'+i_atr_name
                )
                # offset curve
                _mya_core.AnmCurveNodeOpt(i_curve).offset_all_values(
                    i_value_current+i_value_offset
                )
                cmds.select(i_curve)
                cmds.dgdirty()
            else:
                i_value = _mya_core.NodeAttribute.get_value(i_plug_name, 'input1D[0]')
                _mya_core.NodeAttribute.break_source(
                    path, i_atr_name
                )
                _mya_core.NodeAttribute.set_value(
                    path, i_atr_name, i_value+i_value_current+i_value_offset
                )

        if locator_paths:
            [_mya_core.Node.delete(x) for x in set(locator_paths)]
            cmds.select(path)
            cmds.dgdirty()

        cmds.select(clear=1)

    # mirror
    def do_mirror_auto(self, **kwargs):
        path_src = self._path
        ctr_key_src = self.to_control_key(path_src)
        ctr_key_dst, direction = self.to_control_direction_args(ctr_key_src)
        # side
        if ctr_key_dst is not None:
            path_dst = self.find_one_control(ctr_key_dst)
            if path_dst is None:
                bsc_log.Log.trace_method_warning(
                    self.LOG_KEY, 'control for "{}" is not found'.format(ctr_key_dst)
                )
                return
            # left or right
            if direction in {
                self.ControlDirections.Left, self.ControlDirections.Right
            }:
                # override axis vector
                if 'axis_vector_dict' in kwargs:
                    axis_vector_dict = kwargs.pop('axis_vector_dict')
                    # key may not in dict
                    kwargs['axis_vector_src'] = axis_vector_dict.get(path_src)
                    kwargs['axis_vector_dst'] = axis_vector_dict.get(path_dst)

                _mirror_and_flip.MirrorAndFlip.mirror_side_for(path_src, path_dst, **kwargs)
        else:
            if direction in {
                self.ControlDirections.Middle
            }:
                # override axis vector
                if 'axis_vector_dict' in kwargs:
                    axis_vector_dict = kwargs.pop('axis_vector_dict')
                    kwargs['axis_vector_src'] = axis_vector_dict.get(path_src)

                _mirror_and_flip.MirrorAndFlip.mirror_middle_for(path_src, **kwargs)

    def do_mirror_side(self, scheme, **kwargs):
        path_src = self._path
        ctr_key_src = self.to_control_key(path_src)
        if scheme == self.MirrorSchemes.LeftToRight:
            ctr_key_dst, direction = self.to_control_direction_args(ctr_key_src)
            # check is side
            if ctr_key_dst is not None:
                path_dst = self.find_one_control(ctr_key_dst)
                if path_dst is None:
                    bsc_log.Log.trace_method_warning(
                        self.LOG_KEY, 'control for "{}" is not found'.format(ctr_key_dst)
                    )
                    return
                # left
                if direction == self.ControlDirections.Left:
                    # override axis vector
                    if 'axis_vector_dict' in kwargs:
                        axis_vector_dict = kwargs.pop('axis_vector_dict')
                        kwargs['axis_vector_src'] = axis_vector_dict.get(path_src)
                        kwargs['axis_vector_dst'] = axis_vector_dict.get(path_dst)

                    _mirror_and_flip.MirrorAndFlip.mirror_side_for(path_src, path_dst, **kwargs)
        elif scheme == self.MirrorSchemes.RightToLeft:
            ctr_key_dst, direction = self.to_control_direction_args(ctr_key_src)
            # check is side
            if ctr_key_dst is not None:
                path_dst = self.find_one_control(ctr_key_dst)
                if path_dst is None:
                    bsc_log.Log.trace_method_warning(
                        self.LOG_KEY, 'control for "{}" is not found'.format(ctr_key_dst)
                    )
                    return
                    # right
                if direction == self.ControlDirections.Right:
                    # override axis vector
                    if 'axis_vector_dict' in kwargs:
                        axis_vector_dict = kwargs.pop('axis_vector_dict')
                        kwargs['axis_vector_src'] = axis_vector_dict.get(path_src)
                        kwargs['axis_vector_dst'] = axis_vector_dict.get(path_dst)

                    _mirror_and_flip.MirrorAndFlip.mirror_side_for(path_src, path_dst, **kwargs)

    def do_mirror_middle(self, **kwargs):
        path_src = self._path
        ctr_key_src = self.to_control_key(path_src)
        _, direction = self.to_control_direction_args(ctr_key_src)
        if direction == self.ControlDirections.Middle:
            # override axis vector
            if 'axis_vector_dict' in kwargs:
                axis_vector_dict = kwargs.pop('axis_vector_dict')
                kwargs['axis_vector_src'] = axis_vector_dict.get(path_src)

            _mirror_and_flip.MirrorAndFlip.mirror_middle_for(path_src, **kwargs)


class ControlMirrorPasteOpt(
    ControlNamespaceExtra,
    _base.AbsMotion
):

    def __init__(self, namespace):
        self._init_namespace_extra(namespace)

    @_mya_core.Undo.execute
    def apply_motion_dict(self, data, **kwargs):
        if not data:
            return

        if isinstance(data, dict):
            for i_control_key, i_data in data.items():
                i_path = self.find_one_control(i_control_key)
                # ignore neither has "translate", "rotate"
                if cmds.objExists(i_path+'.translate') is False and cmds.objExists(i_path+'.rotate') is False:
                    continue

                ControlMotionOpt(i_path).do_mirror_auto(data_override=i_data, **kwargs)

    def load_motion_from(self, file_path, **kwargs):
        self.apply_motion_dict(
            bsc_storage.StgFileOpt(file_path).set_read(), **kwargs
        )
