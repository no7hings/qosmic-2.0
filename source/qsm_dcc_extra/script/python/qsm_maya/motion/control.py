# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from .. import core as _mya_core


class ControlOpt(object):
    @classmethod
    def to_control_name(cls, path):
        return path.split('|')[-1].split(':')[-1]

    @classmethod
    def apply_value(cls, path, atr_data, force=False):
        atr_name, value = atr_data
        if _mya_core.NodeAttribute.is_exists(path, atr_name) is False:
            return
        if _mya_core.NodeAttribute.is_lock(path, atr_name) is True:
            # when node is from reference, ignore
            if _mya_core.Reference.is_from_reference(path) is True:
                return
            if force is True:
                _mya_core.NodeAttribute.unlock(path, atr_name)
            else:
                return
        if _mya_core.NodeAttribute.has_source(path, atr_name) is True:
            if force is True:
                result = _mya_core.NodeAttribute.break_source(path, atr_name)
                if result is False:
                    return
            else:
                return
        value_dst = _mya_core.NodeAttribute.get_value(path, atr_name)
        if value != value_dst:
            _mya_core.NodeAttribute.set_value(path, atr_name, value)

    @classmethod
    def apply_curve(cls, path, atr_data, frame_offset=0, force=False):
        atr_name, curve_type, infinities, curve_points = atr_data
        if _mya_core.NodeAttribute.is_exists(path, atr_name) is False:
            return
        if _mya_core.NodeAttribute.is_lock(path, atr_name) is True:
            # when node is from reference, ignore
            if _mya_core.Reference.is_from_reference(path) is True:
                return
            if force is True:
                _mya_core.NodeAttribute.unlock(path, atr_name)
            else:
                return
        if _mya_core.NodeAttribute.has_source(path, atr_name) is True:
            if force is True:
                _mya_core.NodeAttribute.break_source(path, atr_name)
            else:
                return

        curve_name = '{}_{}'.format(
            path.split('|')[-1].split(':')[-1],
            atr_name.replace('.', '_')
        )
        curve_name_new = cmds.createNode(curve_type, name=curve_name, skipSelect=1)

        i_atr_path_src = '{}.output'.format(curve_name_new)
        i_atr_path_dst = '{}.{}'.format(path, atr_name)
        _mya_core.Connection.create(i_atr_path_src, i_atr_path_dst)

        _mya_core.AnimationCurveOpt(path, atr_name).set_points(curve_points, frame_offset=frame_offset)

        _mya_core.NodeAttribute.set_value(
            curve_name_new, 'preInfinity', infinities[0]
        )
        _mya_core.NodeAttribute.set_value(
            curve_name_new, 'postInfinity', infinities[0]
        )

    def __init__(self, path):
        self._path = path

    def get_animation(self):
        list_ = []
        for i_atr_name in _mya_core.NodeAttributes.get_all_keyable_names(self._path):
            i_curve_name = _mya_core.NodeAttribute.get_source_node(self._path, i_atr_name, 'animCurve')
            if i_curve_name is not None:
                i_curve_type = cmds.nodeType(i_curve_name)
                i_infinities = [
                    _mya_core.NodeAttribute.get_value(i_curve_name, 'preInfinity'),
                    _mya_core.NodeAttribute.get_value(i_curve_name, 'postInfinity')
                ]
                i_curve_points = _mya_core.AnimationCurveOpt(self._path, i_atr_name).get_points()
                list_.append((i_atr_name, i_curve_type, i_infinities, i_curve_points))
            else:
                i_value = _mya_core.NodeAttribute.get_value(self._path, i_atr_name)
                list_.append((i_atr_name, i_value))
        return list_

    def apply_animation(self, motion, frame_offset=0, force=False):
        for i_atr_data in motion:
            if len(i_atr_data) == 2:
                self.apply_value(self._path, i_atr_data, force=force)
            else:
                self.apply_curve(self._path, i_atr_data, frame_offset=frame_offset, force=force)

    def transfer_animation_to(self, path_dst, **kwargs):
        motion = self.get_animation()
        self.__class__(path_dst).apply_animation(motion, **kwargs)

    def get_animation_curve_at(self, atr_name):
        return _mya_core.NodeAttribute.get_source_node(self._path, atr_name, 'animCurve')

    def find_animation_curve_at(self, atr_name, depth_maximum=2):
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

    def create_transformation_locator(self, locator_path):
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

            i_animation_curve = self.get_animation_curve_at(i_atr_name)

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

    def remove_transformation_locator(self):
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
            i_animation_curve = self.find_animation_curve_at(i_atr_name, depth_maximum=5)
            if i_animation_curve is not None:
                _mya_core.NodeAttribute.break_source(
                    self._path, i_atr_name
                )
                _mya_core.Connection.create(
                    i_animation_curve+'.output', self._path+'.'+i_atr_name
                )
                _mya_core.AnimationCurveOpt(
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




