# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from ... import core as _mya_core

from . import control as _control


class ControlMove(object):
    def __init__(self, path):
        pass

    @classmethod
    def create_locator_fnc(cls, main_control, root=None):
        name = _mya_core.DagNode.to_name(main_control)

        locator_name = '{}_loc'.format(name)
        if root is not None:
            locator_path = '{}|{}'.format(root, locator_name)
        else:
            locator_path = '|{}'.format(locator_name)

        if cmds.objExists(locator_path) is False:
            locator_path = _mya_core.DagNode.create_locator(locator_path)

            w, h, d = _mya_core.Transform.get_dimension(main_control)
            locator_shape = _mya_core.Transform.get_shape(
                locator_path
            )
            _mya_core.NodeAttribute.set_as_tuple(
                locator_shape, 'localScale', (w/2, 0, d/2)
            )
            _mya_core.NodeDrawOverride.set_color(
                locator_path, (1.0, .0, .0)
            )
            _mya_core.NodeAttribute.create_as_string(
                locator_path, 'qsm_mark', 'move_locator'
            )

            _mya_core.ParentConstraint.create(
                main_control, locator_path
            )
            _mya_core.ParentConstraint.clear_all_from_source(locator_path)

            _control.ControlMotionOpt(main_control).create_control_move_locator(
                locator_path
            )
            _mya_core.Connection.create(
                locator_path+'.visibility', main_control+'.visibility'
            )

        return locator_path

    @classmethod
    def remove_locator_fnc(cls, main_control):
        _control.ControlMotionOpt(main_control).remove_control_move_locator()

    @classmethod
    def find_main_control(cls, locator_shape):
        transform = _mya_core.Shape.get_transform(locator_shape)
        targets = _mya_core.NodeAttribute.get_target_nodes(
            transform, 'visibility', 'transform'
        )
        if targets:
            return targets[0]
