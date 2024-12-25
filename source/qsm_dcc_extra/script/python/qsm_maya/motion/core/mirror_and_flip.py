# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from ... import core as _mya_core

from . import base as _base


class MirrorAndFlip(_base.AbsMotion):

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
        for i in vector:
            # Making values positive,
            # so the denominator will be all values added togther
            i = abs(i)
            denominator += i

        percentage_strengt = []
        for i in vector:
            # Making vector positive
            # in order to get a strengt relative to the other axis
            i = abs(i)
            i_strengt = i / denominator
            percentage_strengt.append(i_strengt)
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
    def _mark_rotate(cls, path):
        dict_ = {}
        for i_axis in ['X', 'Y', 'Z']:
            i_key = 'rotate{}'.format(i_axis)
            if _mya_core.NodeAttribute.is_lock(path, i_key) is True:
                continue
            if _mya_core.NodeAttribute.has_source(path, i_key) is True:
                continue

            i_atr = _mya_core.NodeAttribute.to_atr_path(path, i_key)
            dict_[i_atr] = cmds.getAttr(i_atr)
        return dict_

    @classmethod
    def _zero_rotate(cls, data):
        for k, v in data.items():
            cmds.setAttr(k, 0)

    @classmethod
    def _recover_rotate(cls, data):
        for k, v in data.items():
            cmds.setAttr(k, v)

    @classmethod
    def get_axis_vector(cls, path):
        dict_ = {}
        # mark auto key
        auto_key_mark = cmds.autoKeyframe(state=1, query=1)
        if auto_key_mark:
            cmds.autoKeyframe(state=0)

        rotate_data = cls._mark_rotate(path)
        # zero rotate
        cls._zero_rotate(rotate_data)

        world_mat = cmds.xform(path, matrix=1, worldSpace=1, query=1)
        # Rounding the values in the world matrix
        for i, i_value in enumerate(world_mat):
            world_mat[i] = round(i_value, 3)

        dict_['x_axis'] = world_mat[0:3]
        dict_['y_axis'] = world_mat[4:7]
        dict_['z_axis'] = world_mat[8:11]
        # recover rotate
        cls._recover_rotate(rotate_data)
        # recover auto key
        if auto_key_mark:
            cmds.autoKeyframe(state=True)
        return dict_

    @classmethod
    def generate_side_mirror_keys(
        cls,
        path_src, path_dst,
        axis_vector_src, axis_vector_dst,
        mirror_axis, key_includes,
    ):
        list_ = []
        # Getting the direction of the axis on controller
        if axis_vector_src is None:
            axis_vector_src = cls.get_axis_vector(path_src)

        x_axis_vector_src = axis_vector_src['x_axis']
        y_axis_vector_src = axis_vector_src['y_axis']
        z_axis_vector_src = axis_vector_src['z_axis']

        # Getting the direction of the axis on opposite controller
        if axis_vector_dst is None:
            axis_vector_dst = cls.get_axis_vector(path_dst)

        x_axis_vector_dst = axis_vector_dst['x_axis']
        y_axis_vector_dst = axis_vector_dst['y_axis']
        z_axis_vector_dst = axis_vector_dst['z_axis']

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

        for i_key in key_includes:
            i_factor = cls.generate_side_attribute_value_factor(
                i_key,
                mirror_axis,
                mirror_atr_axis,
                x_dominating_src, y_dominating_src, z_dominating_src,
                x_dominating_dst, y_dominating_dst, z_dominating_dst
            )
            if i_factor == -1:
                list_.append(i_key)
        return list_

    @classmethod
    def generate_middle_mirror_keys(
        cls,
        path_src,
        axis_vector_src,
        mirror_axis, key_includes
    ):
        list_ = []

        if axis_vector_src is None:
            axis_vector_src = cls.get_axis_vector(path_src)

        x_axis_vector_src = axis_vector_src['x_axis']
        y_axis_vector_src = axis_vector_src['y_axis']
        z_axis_vector_src = axis_vector_src['z_axis']

        x_dominating_src = cls.get_dominating_by_axis_vector(x_axis_vector_src)
        y_dominating_src = cls.get_dominating_by_axis_vector(y_axis_vector_src)
        z_dominating_src = cls.get_dominating_by_axis_vector(z_axis_vector_src)

        mirror_atr_axis = cls.get_mirror_atr_axis_by_vector(
            mirror_axis,
            x_dominating_src,
            y_dominating_src,
            z_dominating_src,
        )

        for i_key in key_includes:
            i_factor = cls.get_middle_attribute_value_factor(
                i_key, mirror_atr_axis
            )
            if i_factor == -1:
                list_.append(i_key)
        return list_

    @classmethod
    def generate_side_attribute_value_factor(
        cls,
        atr_name,
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
    def get_middle_attribute_value_factor(
        cls,
        atr_name,
        mirror_atr_axis
    ):
        if atr_name.__contains__('translate'):
            if atr_name.__contains__(mirror_atr_axis):
                return -1
            return 1
        elif atr_name.__contains__('rotate'):
            if atr_name.__contains__(mirror_atr_axis):
                return 1
            return -1
        return 1

    @classmethod
    def mirror_side_for(cls, path_src, path_dst, **kwargs):
        """
        left or right only
        """
        key_includes = cmds.listAttr(path_src, keyable=True, unlocked=True)
        if 'data_override' in kwargs:
            data_src = kwargs.pop('data_override')
        else:
            data_src = _base.NodeMotion.generate_motion_properties_fnc(path_src, key_includes=key_includes)

        mirror_axis = 'X'

        mirror_keys = cls.generate_side_mirror_keys(
            path_src, path_dst,
            kwargs.get('axis_vector_src'), kwargs.get('axis_vector_dst'),
            mirror_axis, key_includes
        )

        _base.NodeMotion.apply_motion_properties_fnc(path_dst, data_src, mirror_keys=mirror_keys, **kwargs)

    @classmethod
    def mirror_middle_for(cls, path_src, **kwargs):
        """
        middle
        """
        key_includes = cmds.listAttr(path_src, keyable=True, unlocked=True)
        if 'data_override' in kwargs:
            data_src = kwargs.pop('data_override')
        else:
            data_src = _base.NodeMotion.generate_motion_properties_fnc(path_src, key_includes=key_includes)

        mirror_axis = 'X'

        mirror_keys = cls.generate_middle_mirror_keys(
            path_src,
            kwargs.get('axis_vector_src'),
            mirror_axis, key_includes
        )
        _base.NodeMotion.apply_motion_properties_fnc(path_src, data_src, mirror_keys=mirror_keys, **kwargs)
