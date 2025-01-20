# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from ... import core as _mya_core

from . import control as _control


class ControlMove:
    @classmethod
    def test(cls):
        cls.create_locator_fnc(
            'nurbsCircle1'
        )

    def __init__(self, path):
        pass

    @classmethod
    def create_locator_fnc(cls, main_control, root=None):
        name = _mya_core.DagNode.to_name(main_control)

        main_locator_name = '{}_loc'.format(name)
        if root is not None:
            main_locator_path = '{}|{}'.format(root, main_locator_name)
        else:
            main_locator_path = '|{}'.format(main_locator_name)

        if cmds.objExists(main_locator_path) is False:
            main_locator_path = _mya_core.DagNode.create_locator(main_locator_path)

            w, h, d = _mya_core.Transform.get_dimension(main_control)
            main_locator_shape = _mya_core.Transform.get_shape(
                main_locator_path
            )
            _mya_core.NodeAttribute.set_as_tuple(
                main_locator_shape, 'localScale', (w/2, 0, d/2)
            )
            _mya_core.NodeDrawOverride.set_color(
                main_locator_path, (1.0, .0, .0)
            )
            _mya_core.NodeAttribute.create_as_string(
                main_locator_path, 'qsm_mark', 'move_locator'
            )

            _mya_core.ParentConstraint.create(
                main_control, main_locator_path
            )
            _mya_core.ParentConstraint.clear_all_from_source(main_locator_path)

            _control.ControlMotionOpt(main_control).connect_move_locator(
                main_locator_path
            )
            _mya_core.Connection.create(
                main_control+'.visibility', main_locator_path+'.visibility'
            )

        return main_locator_path

    @classmethod
    def remove_locator_fnc(cls, main_control):
        _control.ControlMotionOpt(main_control).remove_move_locator()

    @classmethod
    def find_main_control(cls, main_locator_shape):
        transform = _mya_core.Shape.get_transform(main_locator_shape)
        source = _mya_core.NodeAttribute.get_source_node(
            transform, 'visibility', 'transform'
        )
        if source:
            return source
