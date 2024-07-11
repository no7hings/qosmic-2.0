# coding:utf-8
import re

import enum
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.OpenMaya as om

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

from ... import core as _mya_core


class ControlDirections(enum.IntEnum):
    Left = 0
    Right = 1
    Middle = 2
    Unknown = -1


class MirrorSchemes(enum.IntEnum):
    LeftToRight = 0
    RightToLeft = 1
    Auto = 2


class ControlMirror(object):

    @classmethod
    def is_dominants_same_and_not_mirror(cls, mirror_axis, dominent, opp_dominent):
        """
        Args:
            mirror_axis: The usedefined mirror axis
            dominent: The dominent axis of the controller
            opp_dominent: The dominent axis of the opposite controller

        Return:
            Returns a True if the dominent and opposite domient axis
            is the same. And they are not the same as the mirror axis,
            no matter if the dominent axis is positive or negative.
        """
        pos_mirror = dominent == opp_dominent and not dominent == mirror_axis
        neg_mirror = dominent == opp_dominent and not dominent == '-{}'.format(mirror_axis)
        # Returning False if any of the two statement is False
        if not pos_mirror or not neg_mirror:
            return False
        return True

    @classmethod
    def is_mirror_same_as_dominants(cls, mirror_axis, dominent, opp_dominent):
        """
        Args:
            mirror_axis: The usedefined mirror axis
            dominent: The dominent axis of the controller
            opp_dominent: The dominent axis of the opposite controller

        Return:
            Returns a True if the dominent and opposite domient axis
            is the same. And also the same as the mirror axis, no matter
            if the dominent axis is positive or negative.
        """
        return (
            mirror_axis == dominent
            and mirror_axis == opp_dominent
            or '-{}'.format(mirror_axis) == dominent
            and '-{}'.format(mirror_axis) == opp_dominent
        )

    @classmethod
    def get_mirror_atr_axis_by_vector(cls, mirror_axis, x_dominating, y_dominating, z_dominating):
        """
        Args:
            mirror_axis: A string with the mirror axis
            x_dominating: String with what world axis the x-axis is pointing to
            y_dominating: String with what world axis the y-axis is pointing to
            z_dominating: String with what world axis the z-axis is pointing to

        Returns:
            Returns what xyz axis pointing in the mirror axis
        """
        # Finding what axis is pointing the most to the mirror axis
        if mirror_axis == x_dominating or '-{}'.format(mirror_axis) == x_dominating:
            mirror_atr_axis = 'X'
        elif mirror_axis == y_dominating or '-{}'.format(mirror_axis) == y_dominating:
            mirror_atr_axis = 'Y'
        elif mirror_axis == z_dominating or '-{}'.format(mirror_axis) == z_dominating:
            mirror_atr_axis = 'Z'
        # In the perfect world this else statement is not needed,
        # however 2 axis can be eqaully spaced giving issues
        else:
            mirror_atr_axis = mirror_axis
        return mirror_atr_axis

    @classmethod
    def get_dominating_by_axis_vector(cls, vector):
        """
        Description:
            Getting what axis a vector is pointing the most to

        Args:
            vector: is a xyz list of 3 float values

        Returns:
            A string containing an axis. The axis can also be negative

        """
        # Making positive numbers
        denominator = 0
        for value in vector:
            # Making values positive,
            # so the denominator will be all values added togther
            value = abs(value)
            denominator += value
        percentage_strengt = []
        for value in vector:
            # Making value positive
            # in order to get a strengt relative to the other axis
            value = abs(value)
            strengt = value / denominator
            percentage_strengt.append(strengt)
        # Finding the axis with the highest percentage.
        # Since the percentage_strengt is a xyz list.
        # We can use the index to find xyz.
        index = percentage_strengt.index(max(percentage_strengt))
        if index == 0:
            dominating_axis = '-X' if vector[0] < 0 else 'X'
        elif index == 1:
            dominating_axis = '-Y' if vector[1] < 0 else 'Y'
        elif index == 2:
            dominating_axis = '-Z' if vector[2] < 0 else 'Z'
        else:
            dominating_axis = '-X' if vector[0] < 0 else 'X'
        return dominating_axis

    @classmethod
    def get_attribute_data(cls, ctrl_list):
        data = {}
        for ctrl in ctrl_list:
            # Getting data from controller and putting it in a dictionary
            data[ctrl] = {}
            # Checking if there exist attributes
            attributes = cmds.listAttr(ctrl, keyable=True, unlocked=True)
            if attributes:
                for attr in attributes:
                    # Seeing if attribute has incoming connection,
                    # and there cannot be modified
                    source_con = cmds.listConnections(
                        '{}.{}'.format(ctrl, attr),
                        source=True,
                        destination=False,
                    )
                    # Checking if source connenction is a key
                    key_source = cmds.listConnections(
                        '{}.{}'.format(ctrl, attr),
                        source=True,
                        type='animCurve',
                    )
                    if not source_con:
                        # Getting the value on the controller
                        # and storing it in data dict
                        value = cmds.getAttr('{}.{}'.format(ctrl, attr))
                        # Only store data if int or float type
                        if type(value) in [int, float]:
                            data[ctrl][attr] = value
                    elif key_source:
                        # Getting the value on the controller
                        # and storing it in data dict
                        value = cmds.getAttr('{}.{}'.format(ctrl, attr))
                        # Only store data if int or float type
                        if type(value) in [int, float]:
                            data[ctrl][attr] = value
        return data

    @classmethod
    def _rotate_to_zero(cls, ctrl):
        for attr in ['X', 'Y', 'Z']:
            if cmds.listAttr(
                '{}.rotate{}'.format(ctrl, attr), keyable=True, unlocked=True
            ):
                auto_key = cmds.autoKeyframe(state=True, query=True)
                if auto_key:
                    cmds.autoKeyframe(state=False)
                cmds.setAttr('{}.rotate{}'.format(ctrl, attr), 0)
                if auto_key:
                    cmds.autoKeyframe(state=True)

    @classmethod
    def _rotate_to(cls, ctrl, data):
        for attr in ['X', 'Y', 'Z']:
            if 'rotate{}'.format(attr) in data[ctrl].keys():
                auto_key = cmds.autoKeyframe(state=True, query=True)
                if auto_key:
                    cmds.autoKeyframe(state=False)
                cmds.setAttr(
                    '{}.rotate{}'.format(ctrl, attr),
                    data[ctrl]['rotate{}'.format(attr)],
                )
                if auto_key:
                    cmds.autoKeyframe(state=True)

    @classmethod
    def get_vector_data(cls, ctrl_list):
        vector_dict = {}
        cur_pos = {}
        # Storing the current position of the ctrl,
        # to get vector data in neutral position
        for ctrl in ctrl_list:
            cur_pos[ctrl] = cls.get_attribute_data([ctrl])
            # cls._rotate_to_zero(ctrl)
        for ctrl in ctrl_list:
            # getting controller vector in neutral position
            vector_dict[ctrl] = {}
            world_mat = cmds.xform(ctrl, matrix=True, worldSpace=True, query=True)
            # Rounding the values in the world matrix
            for i, value in enumerate(world_mat):
                rounded_value = round(value, 3)
                world_mat[i] = rounded_value
            vector_dict[ctrl]['x_axis'] = world_mat[0:3]
            vector_dict[ctrl]['y_axis'] = world_mat[4:7]
            vector_dict[ctrl]['z_axis'] = world_mat[8:11]

        # Setting ctrl back to its position
        # for ctrl in ctrl_list:
        #     cls._rotate_to(ctrl, cur_pos[ctrl])

        return vector_dict

    @classmethod
    def side_fnc(cls, path_src, path_dst, data, mirror_axis, vector_data):
        # Getting the direction of the axis on controller
        x_axis_vector_src = vector_data[path_src]['x_axis']
        y_axis_vector_src = vector_data[path_src]['y_axis']
        z_axis_vector_src = vector_data[path_src]['z_axis']
        # Getting the direction of the axis on opposite controller
        x_axis_vector_dst = vector_data[path_dst]['x_axis']
        y_axis_vector_dst = vector_data[path_dst]['y_axis']
        z_axis_vector_dst = vector_data[path_dst]['z_axis']

        x_dominating_src = cls.get_dominating_by_axis_vector(x_axis_vector_src)
        y_dominating_src = cls.get_dominating_by_axis_vector(y_axis_vector_src)
        z_dominating_src = cls.get_dominating_by_axis_vector(z_axis_vector_src)

        x_dominating_dst = cls.get_dominating_by_axis_vector(x_axis_vector_dst)
        y_dominating_dst = cls.get_dominating_by_axis_vector(y_axis_vector_dst)
        z_dominating_dst = cls.get_dominating_by_axis_vector(z_axis_vector_dst)

        mirror_atr_axis = cls.get_mirror_atr_axis_by_vector(
            mirror_axis,
            x_dominating_src,
            y_dominating_src,
            z_dominating_src,
        )

        for i_atr_name in data[path_src].keys():
            i_value_src = data[path_src][i_atr_name]
            i_value_factor = cls.generate_side_attribute_value_factor(
                i_atr_name, i_value_src,
                mirror_axis,
                mirror_atr_axis,
                x_dominating_src, y_dominating_src, z_dominating_src,
                x_dominating_dst, y_dominating_dst, z_dominating_dst
            )
            i_value_dst = i_value_src*i_value_factor
            if i_value_dst is not None:
                cmds.setAttr('{}.{}'.format(path_dst, i_atr_name), i_value_dst)

    @classmethod
    def side_attribute_value_fnc(
        cls,
        atr_name, value_src,
        mirror_axis,
        mirror_atr_axis,
        x_dominating_src, y_dominating_src, z_dominating_src,
        x_dominating_dst, y_dominating_dst, z_dominating_dst
    ):
        # scale
        if atr_name.__contains__('scale'):
            return value_src
        # Seeing if the controller has the
        # exact same orientation in the world
        elif (
            x_dominating_src == x_dominating_dst
            and y_dominating_src == y_dominating_dst
            and z_dominating_src == z_dominating_dst
        ):
            # The rotation on the mirror axis should be the same
            if atr_name.__contains__('rotate{}'.format(mirror_atr_axis)):
                return value_src
            # The rotation on the other axis should be the negative value
            elif atr_name.__contains__('rotate'):
                return -value_src
            # The translation on the mirror axis
            # should be the negative value
            elif atr_name.__contains__('translate{}'.format(mirror_atr_axis)):
                return -value_src
            # The translation on the other axis should be the same
            else:
                return value_src
        # translate
        elif atr_name.__contains__('translate'):
            # Checking if both of the dominant axis matches the mirror axis
            # this will get joints mirrored with behavior
            if cls.is_mirror_same_as_dominants(
                mirror_axis, x_dominating_src, x_dominating_dst
            ):
                return -value_src
            elif cls.is_mirror_same_as_dominants(
                mirror_axis, y_dominating_src, y_dominating_dst
            ):
                return -value_src
            elif cls.is_mirror_same_as_dominants(
                mirror_axis, z_dominating_src, z_dominating_dst
            ):
                return -value_src
            # Checking if the dominant axis matches,
            # since if it has the same axis it will need the same value
            # and the other axis need to be negative
            elif x_dominating_src == x_dominating_dst:
                if atr_name.__contains__(mirror_atr_axis):
                    return value_src
                elif atr_name.__contains__('X'):
                    return value_src
                else:
                    return -value_src
            elif y_dominating_src == y_dominating_dst:
                if atr_name.__contains__(mirror_atr_axis):
                    return value_src
                elif atr_name.__contains__('Y'):
                    return value_src
                else:
                    return -value_src
            elif z_dominating_src == z_dominating_dst:
                if atr_name.__contains__(mirror_atr_axis):
                    return value_src
                elif atr_name.__contains__('Z'):
                    return value_src
                else:
                    return -value_src
            else:
                return -value_src
        # rotate
        elif atr_name.__contains__('rotate'):
            # X
            if cls.is_dominants_same_and_not_mirror(
                mirror_axis, x_dominating_src, x_dominating_dst
            ):
                if atr_name.__contains__(mirror_atr_axis):
                    return -value_src
                elif atr_name.__contains__('X'):
                    return -value_src
                else:
                    return value_src
            # Y
            elif cls.is_dominants_same_and_not_mirror(
                mirror_axis, y_dominating_src, y_dominating_dst
            ):
                if atr_name.__contains__(mirror_atr_axis):
                    return -value_src
                elif atr_name.__contains__('Y'):
                    return -value_src
                else:
                    return value_src
            # Z
            elif cls.is_dominants_same_and_not_mirror(
                mirror_axis, z_dominating_src, z_dominating_dst
            ):
                if atr_name.__contains__(mirror_atr_axis):
                    return -value_src
                elif atr_name.__contains__('Z'):
                    return -value_src
                else:
                    return value_src
            else:
                return value_src
        else:
            return value_src

    @classmethod
    def generate_side_attribute_value_factor(
        cls,
        atr_name, value_src,
        mirror_axis,
        mirror_atr_axis,
        x_dominating_src, y_dominating_src, z_dominating_src,
        x_dominating_dst, y_dominating_dst, z_dominating_dst
    ):
        # scale
        if atr_name.__contains__('scale'):
            return 1
        # Seeing if the controller has the
        # exact same orientation in the world
        elif (
            x_dominating_src == x_dominating_dst
            and y_dominating_src == y_dominating_dst
            and z_dominating_src == z_dominating_dst
        ):
            # The rotation on the mirror axis should be the same
            if atr_name.__contains__('rotate{}'.format(mirror_atr_axis)):
                return 1
            # The rotation on the other axis should be the negative value
            elif atr_name.__contains__('rotate'):
                return -1
            # The translation on the mirror axis
            # should be the negative value
            elif atr_name.__contains__('translate{}'.format(mirror_atr_axis)):
                return -1
            # The translation on the other axis should be the same
            return 1
        # translate
        elif atr_name.__contains__('translate'):
            # Checking if both of the dominant axis matches the mirror axis
            # this will get joints mirrored with behavior
            if cls.is_mirror_same_as_dominants(
                mirror_axis, x_dominating_src, x_dominating_dst
            ):
                return -1
            elif cls.is_mirror_same_as_dominants(
                mirror_axis, y_dominating_src, y_dominating_dst
            ):
                return -1
            elif cls.is_mirror_same_as_dominants(
                mirror_axis, z_dominating_src, z_dominating_dst
            ):
                return -1
            # Checking if the dominant axis matches,
            # since if it has the same axis it will need the same value
            # and the other axis need to be negative
            elif x_dominating_src == x_dominating_dst:
                if atr_name.__contains__(mirror_atr_axis):
                    return 1
                elif atr_name.__contains__('X'):
                    return 1
                else:
                    return -1
            elif y_dominating_src == y_dominating_dst:
                if atr_name.__contains__(mirror_atr_axis):
                    return 1
                elif atr_name.__contains__('Y'):
                    return 1
                else:
                    return -1
            elif z_dominating_src == z_dominating_dst:
                if atr_name.__contains__(mirror_atr_axis):
                    return 1
                elif atr_name.__contains__('Z'):
                    return 1
                else:
                    return -1
            return -1
        # rotate
        elif atr_name.__contains__('rotate'):
            # X
            if cls.is_dominants_same_and_not_mirror(
                mirror_axis, x_dominating_src, x_dominating_dst
            ):
                if atr_name.__contains__(mirror_atr_axis):
                    return -1
                elif atr_name.__contains__('X'):
                    return -1
                return 1
            # Y
            elif cls.is_dominants_same_and_not_mirror(
                mirror_axis, y_dominating_src, y_dominating_dst
            ):
                if atr_name.__contains__(mirror_atr_axis):
                    return -1
                elif atr_name.__contains__('Y'):
                    return -1
                return 1
            # Z
            elif cls.is_dominants_same_and_not_mirror(
                mirror_axis, z_dominating_src, z_dominating_dst
            ):
                if atr_name.__contains__(mirror_atr_axis):
                    return -1
                elif atr_name.__contains__('Z'):
                    return -1
                return 1
            return 1
        return 1

    @classmethod
    def middle_fnc(cls, path, data, mirror_axis, vector_data):
        # Getting the direction of the axis on middle controller
        # Getting the direction of the axis on controller
        x_axis_vector_src = vector_data[path]['x_axis']
        y_axis_vector_src = vector_data[path]['y_axis']
        z_axis_vector_src = vector_data[path]['z_axis']
        
        x_dominating_src = cls.get_dominating_by_axis_vector(x_axis_vector_src)
        y_dominating_src = cls.get_dominating_by_axis_vector(y_axis_vector_src)
        z_dominating_src = cls.get_dominating_by_axis_vector(z_axis_vector_src)

        mirror_atr_axis = cls.get_mirror_atr_axis_by_vector(
            mirror_axis,
            x_dominating_src,
            y_dominating_src,
            z_dominating_src,
        )

        for i_atr_name in data[path].keys():
            i_value_src = data[path][i_atr_name]
            # Finding what axis is pointing the most to the mirror axis
            i_value_dst = cls.middle_attribute_value_fnc(i_atr_name, i_value_src, mirror_atr_axis)
            if i_value_dst is not None:
                cmds.setAttr('{}.{}'.format(path, i_atr_name), i_value_dst)

    @classmethod
    def middle_attribute_value_fnc(
        cls,
        atr_name, value_src,
        mirror_atr_axis
    ):
        if atr_name.__contains__('translate'):
            if atr_name.__contains__(mirror_atr_axis):
                return -value_src
            else:
                pass
        elif atr_name.__contains__('rotate'):
            if atr_name.__contains__(mirror_atr_axis):
                return value_src
            else:
                return -value_src

    @classmethod
    def execute_for_side(cls, path_src, path_dst):
        ctrl_list = [path_src, path_dst]
        data = cls.get_attribute_data(ctrl_list)
        vector_data = cls.get_vector_data(ctrl_list)
        mirror_axis = 'X'
        cls.side_fnc(
            path_src,
            path_dst,
            data=data,
            mirror_axis=mirror_axis,
            vector_data=vector_data,
        )

    @classmethod
    def execute_for_middle(cls, path):
        ctrl_list = [path]
        data = cls.get_attribute_data(ctrl_list)
        vector_data = cls.get_vector_data(ctrl_list)
        mirror_axis = 'X'
        cls.middle_fnc(
            path, data, mirror_axis, vector_data
        )


class ControlMotionOpt(object):

    @classmethod
    def to_control_key(cls, path):
        return path.split('|')[-1].split(':')[-1]

    @classmethod
    def to_control_direction_args(cls, control_key):
        ps = [
            (r'(.*)_L', ControlDirections.Left, '{}_R'),
            (r'(.*)_R', ControlDirections.Right, '{}_L'),
            (r'(.*)_M', ControlDirections.Middle, None),
        ]
        for i_p, i_d, i_f in ps:
            i_r = re.match(i_p, control_key)
            if i_r:
                if i_f is not None:
                    return i_f.format(i_r.group(1)), i_d
                return None, i_d
        return None, ControlDirections.Unknown

    def __init__(self, path):
        self._path = path
        self._namespace = _mya_core.DagNode.to_namespace(self._path)

    def get_data(self, includes=None):
        if isinstance(includes, (tuple, list)):
            atr_names = [x for x in includes if _mya_core.NodeAttribute.is_exists(self._path, x) is True]
        else:
            atr_names = _mya_core.NodeAttributes.get_all_keyable_names(self._path)

        list_ = []
        for i_atr_name in atr_names:
            # fixme: use attribute connection?
            i_curve_name = _mya_core.NodeAttribute.get_source_node(self._path, i_atr_name, 'animCurve')
            # i_curve_name = _mya_core.NodePortAnmCurveOpt(self._path, i_atr_name).get_node()
            if i_curve_name is not None:
                i_curve_type = cmds.nodeType(i_curve_name)
                i_infinities = [
                    _mya_core.NodeAttribute.get_value(i_curve_name, 'preInfinity'),
                    _mya_core.NodeAttribute.get_value(i_curve_name, 'postInfinity')
                ]
                i_curve_points = _mya_core.NodePortAnmCurveOpt(self._path, i_atr_name).get_points()
                list_.append((i_atr_name, i_curve_type, i_infinities, i_curve_points))
            else:
                i_value = _mya_core.NodeAttribute.get_value(self._path, i_atr_name)
                list_.append((i_atr_name, i_value))
        return list_

    def apply_data(self, data, **kwargs):
        force = kwargs.get('force', False)
        frame_offset = kwargs.get('frame_offset', 0)
        mirror_keys = kwargs.get('mirror_keys', [])
        for i_atr_data in data:
            # value
            if len(i_atr_data) == 2:
                _mya_core.NodeKeyframe.apply_value(self._path, i_atr_data, force=force, mirror_keys=mirror_keys)
            # animation curve
            if len(i_atr_data) == 4:
                _mya_core.NodeKeyframe.apply_curve(self._path, i_atr_data, frame_offset=frame_offset, force=force)

    def transfer_to(self, path_dst, **kwargs):
        data = self.get_data()
        self.__class__(path_dst).apply_data(data, **kwargs)

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
                _mya_core.NodePortAnmCurveOpt(
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

    def find_control(self, control_key):
        if self._namespace:
            _ = cmds.ls('{}:{}'.format(self._namespace, control_key), long=1)
            if _:
                return _[0]
        else:
            _ = cmds.ls(control_key, long=1)
            if _:
                return _[0]

    def mirror_auto(self, **kwargs):
        path_src = self._path
        control_key = self.to_control_key(path_src)
        control_key_, direction = self.to_control_direction_args(control_key)
        if control_key_ is not None:
            path_dst = self.find_control(control_key_)
            if direction in {
                ControlDirections.Left, ControlDirections.Right
            }:
                ControlMirror.execute_for_side(path_src, path_dst)
        else:
            if direction in {
                ControlDirections.Middle
            }:
                ControlMirror.execute_for_middle(path_src)


class ControlsMotionOpt(object):
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

    def __init__(self, namespace, paths):
        self._namespace = namespace
        self._path_set = set(paths)

    def find_control(self, control_key):
        if self._namespace:
            _ = cmds.ls('{}:{}'.format(self._namespace, control_key), long=1)
            if _:
                return _[0]
        else:
            _ = cmds.ls(control_key, long=1)
            if _:
                return _[0]

    def get_data(self):
        dict_ = {}
        for i_path in self._path_set:
            i_control_opt = ControlMotionOpt(i_path)
            i_motion = i_control_opt.get_data()
            i_control_key = ControlMotionOpt.to_control_key(i_path)
            dict_[i_control_key] = i_motion
        return dict_

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
                i_motion = data[i_control_key]
                ControlMotionOpt(i_control_path).apply_data(i_motion, **kwargs)

    def export_to(self, file_path):
        bsc_storage.StgFileOpt(file_path).set_write(self.get_data())

    def load_from(self, file_path, **kwargs):
        self.apply_data(
            bsc_storage.StgFileOpt(file_path).set_read(), **kwargs
        )

    def mirror_all(self, direction='left_to_right'):
        for i in self._path_set:
            pass
