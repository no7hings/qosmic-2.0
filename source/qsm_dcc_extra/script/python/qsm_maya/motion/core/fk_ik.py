# coding:utf-8
import copy
import functools
import math
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.api.OpenMaya as om2

import lxbasic.resource as bsc_resource

from ... import core as _mya_core


class FKIKSwitch(object):
    def __init__(self, namespace):
        self._namespace = namespace

        self._cfg = bsc_resource.RscExtendConfigure.get_as_content('rig/adv_fk_ik_switch')
        self._cfg.do_flatten()

    @classmethod
    def guess_args(cls, cfg):
        _ = cmds.ls(selection=1, long=1)
        if _:
            control_path = _[0]
            namespace = _mya_core.DagNode.to_namespace(control_path)
            if namespace:
                if cmds.objExists('{}:Main'.format(namespace)) is False:
                    return

                direction = control_path[-1]
                if direction not in ['L', 'R', 'M']:
                    return

                if direction in ['L', 'R']:
                    keys = cfg.get_keys('limb_switch.*.controls.*.control')
                    for i_key in keys:
                        i_value = cfg.get(i_key)
                        i_control = '{}:{}'.format(namespace, i_value.format(direction=direction))
                        if cmds.objExists(i_control):
                            i_control_path = _mya_core.DagNode.to_path(i_control)
                            if i_control_path == control_path:
                                i_main_key = i_key.split('.')[1]
                                if i_main_key.endswith('ik'):
                                    i_main_key_inverse = i_main_key[:-2]+'fk'
                                else:
                                    i_main_key_inverse = i_main_key[:-2]+'ik'
                                i_data = cfg.get_as_content('limb_switch.{}'.format(i_main_key_inverse))
                                return i_data, namespace, direction
                elif direction in ['M']:
                    return

    @classmethod
    def execute_auto(cls, *args, **kwargs):
        cfg = bsc_resource.RscExtendConfigure.get_as_content('rig/adv_fk_ik_switch')
        cfg.do_flatten()

        args = cls.guess_args(cfg)
        if args:
            cls.switch_limb_auto(*args)

    @classmethod
    def compute_translation_offset(cls, source, target):
        return [
            x[0]-x[1]
            for x in
            zip(
                cmds.xform(source, translation=1, worldSpace=1, query=1),
                cmds.xform(target, translation=1, worldSpace=1, query=1)
            )
        ]

    @classmethod
    def compute_rotation_offset(cls, source, target):
        return [
            x[0]-x[1]
            for x in
            zip(
                cmds.xform(source, rotation=1, worldSpace=1, query=1),
                cmds.xform(target, rotation=1, worldSpace=1, query=1)
            )
        ]

    @classmethod
    def match_translate(cls, source, target):
        cmds.xform(
            target,
            translation=cmds.xform(source, translation=1, worldSpace=1, query=1),
            worldSpace=1
        )

    @classmethod
    def match_rotate(cls, source, target):
        r_src = cls.to_world_rotation(source)
        o_src = cmds.getAttr(source+'.rotateOrder')
        o_tgt = cmds.getAttr(target+'.rotateOrder')
        if o_tgt != o_src:
            r_tgt = r_src.reorder(o_tgt)
        else:
            r_tgt = r_src
        x, y, z = cls.decompose_rotation(r_tgt)
        cmds.xform(
            target,
            rotation=(x, y, z),
            worldSpace=1
        )

    @classmethod
    def decompose_rotation(cls, rotation):
        return (
            math.degrees(rotation.x),
            math.degrees(rotation.y),
            math.degrees(rotation.z)
        )

    @classmethod
    def to_world_rotation(cls, path):
        return om2.MEulerRotation(
            om2.MVector(*[math.radians(x) for x in cmds.xform(path, rotation=1, worldSpace=1, query=1)]),
            cmds.getAttr(path+'.rotateOrder')
        )

    @classmethod
    def mark_control_key_auto(cls, control, frame):
        attributes = _mya_core.NodeAttributes.get_all_keyable_names(control)
        for i_atr in attributes:
            i_control_curve_opt = _mya_core.NodeAttributeKeyframeOpt(control, i_atr)
            i_control_curve_opt.create_value_at_time(
                frame, _mya_core.NodeAttribute.get_value(control, i_atr)
            )

    @classmethod
    @_mya_core.Undo.execute
    def switch_limb_auto(cls, content, namespace, direction, mark_key=True):
        frame = _mya_core.Frame.get_current_time()
        selection_mark = cmds.ls(selection=1) or []
        options = dict(
            direction=direction,
            namespace=namespace
        )
        # check blend
        blend_control = ('{namespace}:'+content.get('blend_control.path')).format(**options)
        blend_port = content.get('blend_control.port')
        blend_value = content.get('blend_control.value')
        blend_value_pre = _mya_core.NodeAttribute.get_value(blend_control, blend_port)
        if blend_value_pre == blend_value:
            return
        # mark pre key
        if mark_key is True:
            blend_curve_opt = _mya_core.NodeAttributeKeyframeOpt(blend_control, blend_port)
            blend_curve_opt.create_value_at_time(frame-1, blend_value_pre)
            blend_curve_opt.set_out_tangent_type_at_time(frame-1, 'step')
        # mark correspond controls key
        if mark_key is True:
            correspond_controls = content.get('correspond_controls')
            if correspond_controls:
                for k, v in correspond_controls.items():
                    i_control = '{}:{}'.format(namespace, v['control'].format(**options))
                    cls.mark_control_key_auto(i_control, frame)
        # switch controls
        controls = content.get('controls')
        if controls:
            for k, v in controls.items():
                i_control = '{}:{}'.format(namespace, v['control'].format(**options))
                if cmds.objExists(i_control) is False:
                    continue

                i_match_translation = v.get('match_translation')
                if i_match_translation is True:
                    i_source = '{}:{}'.format(namespace, v['source'].format(**options))
                    cls.match_translate(i_source, i_control)
                i_match_rotation = v.get('match_rotation')
                if i_match_rotation is True:
                    i_source = '{}:{}'.format(namespace, v['source'].format(**options))
                    cls.match_rotate(i_source, i_control)
                #
                i_reset_translation = v.get('reset_translation')
                if i_reset_translation is True:
                    _mya_core.NodeAttribute.set_as_tuple(i_control, 'translate', (0, 0, 0))

                i_reset_rotation = v.get('reset_rotation')
                if i_reset_rotation is True:
                    _mya_core.NodeAttribute.set_as_tuple(i_control, 'rotate', (0, 0, 0))

                i_copy_rotation = v.get('copy_rotation')
                if i_copy_rotation:
                    i_source = '{}:{}'.format(namespace, v['source'].format(**options))
                    cmds.setAttr(i_control+'.rotate', *cmds.getAttr(i_source+'.rotate')[0])

                i_reset_attributes = v.get('reset_attributes')
                if i_reset_attributes:
                    for j_k, j_v in i_reset_attributes.items():
                        _mya_core.NodeAttribute.set_value(i_control, j_k, j_v)
                # mark key
                if mark_key is True:
                    cls.mark_control_key_auto(i_control, frame)
        # switch pole
        pole = content.get('pole')
        if pole:
            pole_control = '{}:{}'.format(namespace, pole['control'].format(**options))
            start = '{}:{}'.format(namespace, pole['start'].format(**options))
            middle = '{}:{}'.format(namespace, pole['middle'].format(**options))
            end = '{}:{}'.format(namespace, pole['end'].format(**options))
            distance_source = '{}:{}'.format(namespace, pole['distance_source'].format(**options))
            cls.match_pole(pole_control, start, middle, end, distance_source)
            if mark_key is True:
                cls.mark_control_key_auto(pole_control, frame)
        # apply new blend
        cmds.setAttr(blend_control+'.FKIKBlend', blend_value)
        if mark_key is True:
            _mya_core.NodeAttributeKeyframeOpt(blend_control, blend_port).create_value_at_time(
                frame, blend_value
            )

        cmds.select(clear=1)
        # if selection_mark:
        #     cmds.select(selection_mark)

    @classmethod
    def switch_torso_to_ik(cls, content, namespace, direction):
        options = dict(
            namespace=namespace,
            direction=direction
        )
        blend_control = '{}:{}'.format(namespace, 'FKIKSpine_{direction}'.format(**options))
        blend_value = 10
        start = cmds.getAttr(blend_control+'.startJoint')
        end = cmds.getAttr(blend_control+'.endJoint')

        keys = []
        for i in cmds.ls('{}:{}'.format(namespace, start), long=1, dag=1):
            keys.append(_mya_core.DagNode.to_name_without_namespace(i))
            if i.endswith('|{}:{}'.format(namespace, end)):
                break

        ik_splines = cmds.ls('{namespace}:Spine*_{direction}'.format(**options), long=1)
        print ik_splines

        for i_key in keys:
            print i_key

    @classmethod
    def switch_torso_to_fk(cls, content, namespace, direction):
        options = dict(
            namespace=namespace,
            direction=direction
        )
        blend_control = '{}:{}'.format(namespace, 'FKIKSpine_{direction}'.format(**options))
        blend_value = 0
        start = cmds.getAttr(blend_control+'.startJoint')
        end = cmds.getAttr(blend_control+'.endJoint')

        keys = []
        for i in cmds.ls('{}:{}'.format(namespace, start), long=1, dag=1):
            keys.append(_mya_core.DagNode.to_name_without_namespace(i))
            if i.endswith('|{}:{}'.format(namespace, end)):
                break

        for i_key in keys:
            i_options = copy.copy(options)
            i_options.update(dict(key=i_key))
            i_ikx = '{namespace}:IKX{key}_{direction}'.format(**i_options)
            i_fx = '{namespace}:FK{key}_{direction}'.format(**i_options)
            if (
                cmds.objExists(i_ikx) is False
                or cmds.objExists(i_fx) is False
            ):
                continue
            i_translation = cmds.xform(i_ikx, translation=1, worldSpace=1, query=1)
            i_rotation = cmds.xform(i_ikx, rotation=1, worldSpace=1, query=1)
            i_parts = cmds.ls('{namespace}:IKX{key}Part*_{direction}'.format(**i_options), long=1)
            if i_parts:
                i_part = i_parts[-1]
                i_rotation = cmds.xform(i_part, rotation=1, worldSpace=1, query=1)
            cmds.xform(i_fx, translation=i_translation, rotation=i_rotation, worldSpace=1)
        # switch blend
        cmds.setAttr(blend_control+'.FKIKBlend', blend_value)

    @classmethod
    def compute_distance(cls, start, end):
        x, y, z = cmds.xform(start, translation=1, worldSpace=1, query=1)
        x_dst, y_dst, z_dst = cmds.xform(end, translation=1, worldSpace=1, query=1)
        return math.sqrt((x-x_dst)**2+(y-y_dst)**2+(z-z_dst)**2)

    @classmethod
    def match_pole(cls, control, start, middle, end, distance_source):
        loc_0 = cmds.createNode('transform')
        loc_1 = cmds.createNode('transform', parent=loc_0)
        # noinspection PyBroadException
        try:
            t = [
                sum(x)/2 for x in
                zip(
                    cmds.xform(start, translation=1, worldSpace=1, query=1),
                    cmds.xform(end, translation=1, worldSpace=1, query=1)
                )
            ]
            cmds.xform(loc_0, translation=t, worldSpace=1)
            cmds.aimConstraint(middle, loc_0, aimVector=[1, 0, 0])
            cmds.setAttr(
                loc_1+'.translateX', cls.compute_distance(middle, loc_0)+cls.compute_distance(distance_source, control)
            )
            cls.match_translate(
                loc_1, control
            )
        except Exception:
            pass

        finally:
            cmds.delete(loc_0)

    @classmethod
    def test(cls):
        FKIKSwitch.execute_auto()
        # cls.switch_torso_to_ik(None, 'sam_Skin', 'M')
