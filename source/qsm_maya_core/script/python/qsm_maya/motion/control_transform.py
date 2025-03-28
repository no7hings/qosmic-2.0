# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from .. import core as _mya_core


class ControlTransform:
    def __init__(self):
        pass

    @classmethod
    def _connect_output_locator(cls, main_control, output_group, constraint_node):
        cmds.disconnectAttr(
            '{}.translate'.format(main_control), '{}.target[0].targetTranslate'.format(constraint_node)
        )
        cmds.disconnectAttr(
            '{}.rotate'.format(main_control), '{}.target[0].targetRotate'.format(constraint_node)
        )
        atr_names = [
            ('translateX', 'targetTranslateX'),
            ('translateY', 'targetTranslateY'),
            ('translateZ', 'targetTranslateZ'),
            ('rotateX', 'targetRotateX'),
            ('rotateY', 'targetRotateY'),
            ('rotateZ', 'targetRotateZ'),
        ]
        for i_atr_name, i_atr_name_tgt in atr_names:
            i_curve_name = _mya_core.NodeAttributeKeyframe.find_curve_node(main_control, i_atr_name)
            i_layer_name = _mya_core.NodeAttributeKeyframe.find_layer_node(main_control, i_atr_name)

            i_atr_copy_name = 'copy_{}'.format(i_atr_name)
            if i_atr_name.startswith('translate'):
                _mya_core.NodeAttribute.create_as_float(
                    output_group, i_atr_copy_name
                )
            elif i_atr_name.startswith('rotate'):
                _mya_core.NodeAttribute.create_as_angle(
                    output_group, i_atr_copy_name
                )

            if i_layer_name is not None:
                raise RuntimeError()
            elif i_curve_name is not None:
                i_source = _mya_core.NodeAttribute.get_source(main_control, i_atr_name)
                _mya_core.NodeAttribute.connect_from(
                    output_group, i_atr_copy_name, i_source
                )
            else:
                i_value = _mya_core.NodeAttribute.get_value(main_control, i_atr_name)
                _mya_core.NodeAttribute.set_value(
                    output_group, i_atr_copy_name, i_value
                )

            _mya_core.NodeAttribute.connect_to(
                output_group, i_atr_copy_name, '{}.target[0].{}'.format(
                    constraint_node, i_atr_name_tgt
                )
            )

    @classmethod
    def _get_time_samples(cls, pair_blend_node):
        time_samples_set = set()
        atr_names = [
            'inTranslateX', 'inTranslateY', 'inTranslateZ',
            'inRotateX', 'inRotateY', 'inRotateZ',
        ]

        for i_atr_name in atr_names:
            i_atr_name_1 = '{}1'.format(i_atr_name)
            i_curve_name = _mya_core.NodeAttributeKeyframe.find_curve_node(pair_blend_node, i_atr_name_1)
            if i_curve_name:
                i_curve_opt = _mya_core.AnmCurveNodeOpt(i_curve_name)
                i_time_samples = i_curve_opt.get_time_samples()
                time_samples_set.update(i_time_samples)

        time_samples = list(time_samples_set)
        time_samples.sort()
        return time_samples

    @classmethod
    def check_is_valid(cls, main_control):
        atr_names = [
            'translateX', 'translateY', 'translateZ',
            'rotateX', 'rotateY', 'rotateZ'
        ]
        for i_atr_name in atr_names:
            i_layer_name = _mya_core.NodeAttributeKeyframe.find_layer_node(main_control, i_atr_name)
            if i_layer_name:
                return False
        return True

    @classmethod
    def create_locator_fnc(cls, main_control, root=None):
        if cls.check_is_valid(main_control) is False:
            return False

        name = _mya_core.DagNode.to_name(main_control)

        main_locator_name = '{}_loc'.format(name)
        output_group_name = 'output_grp'
        if root is not None:
            main_locator_path = '{}|{}'.format(root, main_locator_name)
        else:
            main_locator_path = '|{}'.format(main_locator_name)

        output_group_path = '{}|{}'.format(main_locator_path, output_group_name)

        if cmds.objExists(main_locator_path) is False:
            main_locator_path = _mya_core.DagNode.create_locator(main_locator_path)
            w, h, d = _mya_core.Transform.get_dimension(main_control)
            main_locator_shape = _mya_core.Transform.get_shape(main_locator_path)
            _mya_core.NodeAttribute.set_as_tuple(main_locator_shape, 'localScale', (w/2, 0, d/2))
            _mya_core.NodeDrawOverride.set_color(main_locator_path, (1.0, .0, .0))
            _mya_core.NodeAttribute.create_as_string(main_locator_path, 'qsm_mark', 'move_locator')
            # todo: use point constraint?
            _mya_core.PointConstraint.create(
                main_control, main_locator_path
            )
            _mya_core.PointConstraint.clear_all_from_source(main_locator_path)

        if cmds.objExists(output_group_path) is False:
            output_group_path = _mya_core.DagNode.create_transform(output_group_path)
            _mya_core.NodeDisplay.set_visible(output_group_path, False)

        constraint_node = _mya_core.ParentConstraint.create(
            main_control, output_group_path, break_parent_inverse=True
        )
        cls._connect_output_locator(main_control, output_group_path, constraint_node)

        _mya_core.ParentConstraint.create(
            output_group_path, main_control
        )
        pair_blend_node = _mya_core.NodeAttribute.get_source_node(
            main_control, 'translateX', 'pairBlend'
        )
        if pair_blend_node:
            # mode may not blend
            for i_atr_name in [
                'translateXMode', 'translateYMode', 'translateZMode',
                'rotateMode',
            ]:
                _mya_core.NodeAttribute.set_value(
                    pair_blend_node, i_atr_name, 0
                )

        # connect visibility for mark
        _mya_core.Connection.create(
            main_control+'.visibility', main_locator_path+'.visibility'
        )
        return True

    @classmethod
    def remove_locator_fnc(cls, main_locator):
        frame_mark = _mya_core.Frame.get_current()
        atr_names = [
            'inTranslateX',
            'inTranslateY',
            'inTranslateZ',
            'inRotateX',
            'inRotateY',
            'inRotateZ',
        ]

        main_locator_shape = _mya_core.Transform.get_shape(main_locator)
        main_control = cls.find_main_control(main_locator_shape)

        pair_blend_node = _mya_core.NodeAttribute.get_source_node(
            main_control, 'translateX', 'pairBlend'
        )
        # when has pairBlend, complete frame curve
        if pair_blend_node:
            # get all time samples
            time_samples = cls._get_time_samples(pair_blend_node)

            rebuild_dict = {}
            for i_frame in time_samples:
                _mya_core.Frame.set_current(i_frame)
                for j_atr_name in atr_names:
                    j_atr_name_1 = '{}1'.format(j_atr_name)
                    j_atr_name_2 = '{}2'.format(j_atr_name)
                    j_curve_name = _mya_core.NodeAttributeKeyframe.find_curve_node(pair_blend_node, j_atr_name_1)
                    j_value = _mya_core.NodeAttribute.get_value(pair_blend_node, j_atr_name_2)
                    key = (j_curve_name, j_atr_name_1)
                    rebuild_dict.setdefault(
                        key, []
                    ).append((i_frame, j_value))

            for k, v in rebuild_dict.items():
                i_curve_name, i_atr_name_1 = k
                i_samples = v
                if i_curve_name is not None:
                    i_curve_opt = _mya_core.AnmCurveNodeOpt(i_curve_name)
                    i_time_samples = i_curve_opt.get_time_samples()
                    if i_samples:
                        for j_frame, j_value in i_samples:
                            # when not time sample, create value at frame
                            if j_frame not in i_time_samples:
                                i_curve_opt.create_value_at_time(j_frame, j_value)
                            else:
                                i_curve_opt.set_value_at_time(j_frame, j_value)
                else:
                    if i_samples:
                        i_first_frame = i_samples[0][0]
                        i_curve_name = _mya_core.NodeAttributeKeyframe.create_at(
                            pair_blend_node, i_atr_name_1, i_first_frame
                        )
                        i_curve_opt = _mya_core.AnmCurveNodeOpt(i_curve_name)
                        for j_frame, j_value in i_samples:
                            i_curve_opt.create_value_at_time(j_frame, j_value)

            _mya_core.NodeAttribute.break_source(
                pair_blend_node, 'weight'
            )
            _mya_core.NodeAttribute.set_value(
                pair_blend_node, 'weight', 0
            )

            _mya_core.Frame.set_current(frame_mark)

        # when no pairBlend, update rest value
        else:
            constraint_nodes = _mya_core.ParentConstraint.get_all_from_source(main_control)
            if constraint_nodes:
                constraint_node = constraint_nodes[0]
                for i_atr_name_0, i_atr_name_1 in [
                    ('restTranslateX', 'constraintTranslateX'),
                    ('restTranslateY', 'constraintTranslateY'),
                    ('restTranslateZ', 'constraintTranslateZ'),
                    ('restRotateX', 'constraintRotateX'),
                    ('restRotateY', 'constraintRotateY'),
                    ('restRotateZ', 'constraintRotateZ')
                ]:
                    _mya_core.NodeAttribute.set_value(
                        constraint_node, i_atr_name_0,
                        _mya_core.NodeAttribute.get_value(constraint_node, i_atr_name_1)
                    )

        _mya_core.Node.delete(main_locator)

    @classmethod
    def find_main_control(cls, main_locator_shape):
        transform = _mya_core.Shape.get_transform(main_locator_shape)
        source = _mya_core.NodeAttribute.get_source_node(
            transform, 'visibility', 'transform'
        )
        if source:
            return source

    @classmethod
    def test_create(cls):
        for i in [
            'nurbsCircle1',
            'nurbsCircle2'
        ]:
            cls.create_locator_fnc(
                # 'mixamorig:Hips'
                i
            )

    @classmethod
    def test_remove(cls):
        for i in [
            'nurbsCircle1_loc',
            'nurbsCircle2_loc'
        ]:
            cls.remove_locator_fnc(
                i
            )
