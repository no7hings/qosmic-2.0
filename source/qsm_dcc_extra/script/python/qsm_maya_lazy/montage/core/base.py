# coding:utf-8
import collections
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import qsm_maya.core as qsm_mya_core


class Sketch(object):
    def __init__(self, path):
        self._path = path

    def get_data(self, key_includes):
        dict_ = {}
        for i_atr_name in key_includes:
            dict_[i_atr_name] = cmds.getAttr(self._path+'.'+i_atr_name)
        return dict_

    def get_rotation_between(self, path_upper):
        keys = [
            'rotateX', 'rotateY', 'rotateZ'
        ]
        a = self._path[len(path_upper)+1:]
        _ = a.split('|')
        c = len(_)
        data = []
        for i in range(c):
            i_path = '{}|{}'.format(path_upper, '|'.join(_[:i+1]))
            data.append(
                cmds.xform(i_path, rotation=1, worldSpace=0, query=1)
            )
        return {
            keys[idx]: sum(x) for idx, x in enumerate(zip(*data))
        }

    def get_orients(self):
        dict_ = {}
        for i_atr_name in [
            'rotateOrder',
            'jointOrientX',
            'jointOrientY',
            'jointOrientZ',
        ]:
            dict_[i_atr_name] = cmds.getAttr(self._path+'.'+i_atr_name)
        return dict_

    def apply_orients(self, orient):
        for k, v in orient.items():
            cmds.setAttr(
                self._path+'.'+k, v
            )

    def apply_rotations(self, rotations):
        pass

    def create_point_constraint_to_master_layer(self, target_node):
        # when is created, connect to exists
        results = qsm_mya_core.PointConstraint.get_all_from_source(target_node)
        if results:
            node = results[0]
            next_index = qsm_mya_core.PointConstraint.get_next_index(node)
            cmds.connectAttr(
                self._path+'.translate', node+'.target[{}].targetTranslate'.format(next_index)
            )
            cmds.connectAttr(
                self._path+'.rotatePivot', node+'.target[{}].targetRotatePivot'.format(next_index)
            )
            cmds.connectAttr(
                self._path+'.rotatePivotTranslate', node+'.target[{}].targetRotateTranslate'.format(next_index)
            )
            cmds.connectAttr(
                self._path+'.parentMatrix[0]', node+'.target[{}].targetParentMatrix'.format(next_index)
            )
            return node
        else:
            _ = cmds.pointConstraint(
                self._path, target_node,
                # maintainOffset=1, weight=1
            )
            node = _[0]
            return node

    def create_orient_constraint_to_master_layer(self, target_node):
        # when is created, connect to exists
        results = qsm_mya_core.OrientConstraint.get_all_from_source(target_node)
        if results:
            node = results[0]
            next_index = qsm_mya_core.OrientConstraint.get_next_index(node)
            cmds.connectAttr(
                self._path+'.rotate', node+'.target[{}].targetRotate'.format(next_index)
            )
            cmds.connectAttr(
                self._path+'.jointOrient', node+'.target[{}].targetJointOrient'.format(next_index)
            )
            cmds.connectAttr(
                self._path+'.rotateOrder', node+'.target[{}].targetRotateOrder'.format(next_index)
            )
            cmds.connectAttr(
                self._path+'.parentMatrix[0]', node+'.target[{}].targetParentMatrix'.format(next_index)
            )
            return node
        else:
            _ = cmds.orientConstraint(
                self._path, target_node, maintainOffset=1, weight=1
            )
            node = _[0]
            cmds.setAttr(node+'.interpType', 2)
            for i in [
                'offsetX',
                'offsetY',
                'offsetZ'
            ]:
                cmds.setAttr(
                    node+'.'+i, 0
                )
            return node

    def create_point_constraint_to_resource(self, target_node):
        _ = cmds.pointConstraint(
            self._path, target_node,
            # maintainOffset=1, weight=1
        )
        node = _[0]
        return node

    def create_orient_constraint_to_resource(self, target_node, clear_offset=True):
        _ = cmds.orientConstraint(
            self._path, target_node, maintainOffset=1, weight=1
        )
        node = _[0]
        cmds.setAttr(node+'.interpType', 2)
        if clear_offset is True:
            for i in [
                'offsetX',
                'offsetY',
                'offsetZ'
            ]:
                cmds.setAttr(
                    node+'.'+i, 0
                )
        return node

    def reset_rotations(self):
        for i in [
            'rotateX', 'rotateY', 'rotateZ'
        ]:
            cmds.setAttr(self._path+'.'+i, 0)

    def reset_translations(self):
        for i in [
            'translateX', 'translateY', 'translateZ',
        ]:
            cmds.setAttr(self._path+'.'+i, 0)

    def match_translations_from(self, source_node):
        for i in [
            'translateX', 'translateY', 'translateZ',
        ]:
            cmds.setAttr(
                self._path+'.'+i,
                cmds.getAttr(source_node+'.'+i)
            )

    def match_rotations_from(self, source_node):
        for i in [
            'rotateX', 'rotateY', 'rotateZ'
        ]:
            cmds.setAttr(
                self._path+'.'+i,
                cmds.getAttr(source_node+'.'+i)
            )
    
    def match_orients_from(self, source_node):
        for i in [
            'jointOrientX',
            'jointOrientY',
            'jointOrientZ'
        ]:
            cmds.setAttr(
                self._path+'.'+i,
                cmds.getAttr(source_node+'.'+i)
            )
    
    def match_all_from(self, source_node):
        self.match_rotations_from(source_node)
        self.match_orients_from(source_node)

    @classmethod
    def test(cls):
        print cls(
            qsm_mya_core.DagNode.to_path('sam_Skin:Elbow_R')
        ).get_rotation_between(
            qsm_mya_core.DagNode.to_path('sam_Skin:Shoulder_R')
        )


class MotionBase(object):
    LAYER_KEYS = [
        'key',
        'clip_start', 'clip_end',
        'start', 'speed', 'count',
        'source_start', 'source_end',
        'pre_cycle', 'post_cycle',
        'scale_start', 'scale_end', 'scale_offset',
        'pre_blend', 'post_blend',
        'layer_index',
        'is_bypass',
    ]

    class ChrMasterSketches:
        Root_M = 'Root_M'
        Hip_R = 'Hip_R'
        Knee_R = 'Knee_R'
        Ankle_R = 'Ankle_R'
        Toes_R = 'Toes_R'
        ToesEnd_R = 'ToesEnd_R'
        Spine1_M = 'Spine1_M'
        Spine2_M = 'Spine2_M'
        Chest_M = 'Chest_M'
        Neck_M = 'Neck_M'
        Head_M = 'Head_M'
        HeadEnd_M = 'HeadEnd_M'
        Scapula_R = 'Scapula_R'
        Shoulder_R = 'Shoulder_R'
        Elbow_R = 'Elbow_R'
        Wrist_R = 'Wrist_R'
        MiddleFinger1_R = 'MiddleFinger1_R'
        MiddleFinger2_R = 'MiddleFinger2_R'
        MiddleFinger3_R = 'MiddleFinger3_R'
        MiddleFinger4_R = 'MiddleFinger4_R'
        ThumbFinger1_R = 'ThumbFinger1_R'
        ThumbFinger2_R = 'ThumbFinger2_R'
        ThumbFinger3_R = 'ThumbFinger3_R'
        ThumbFinger4_R = 'ThumbFinger4_R'
        IndexFinger1_R = 'IndexFinger1_R'
        IndexFinger2_R = 'IndexFinger2_R'
        IndexFinger3_R = 'IndexFinger3_R'
        IndexFinger4_R = 'IndexFinger4_R'
        Cup_R = 'Cup_R'
        PinkyFinger1_R = 'PinkyFinger1_R'
        PinkyFinger2_R = 'PinkyFinger2_R'
        PinkyFinger3_R = 'PinkyFinger3_R'
        PinkyFinger4_R = 'PinkyFinger4_R'
        RingFinger1_R = 'RingFinger1_R'
        RingFinger2_R = 'RingFinger2_R'
        RingFinger3_R = 'RingFinger3_R'
        RingFinger4_R = 'RingFinger4_R'
        Scapula_L = 'Scapula_L'
        Shoulder_L = 'Shoulder_L'
        Elbow_L = 'Elbow_L'
        Wrist_L = 'Wrist_L'
        MiddleFinger1_L = 'MiddleFinger1_L'
        MiddleFinger2_L = 'MiddleFinger2_L'
        MiddleFinger3_L = 'MiddleFinger3_L'
        MiddleFinger4_L = 'MiddleFinger4_L'
        ThumbFinger1_L = 'ThumbFinger1_L'
        ThumbFinger2_L = 'ThumbFinger2_L'
        ThumbFinger3_L = 'ThumbFinger3_L'
        ThumbFinger4_L = 'ThumbFinger4_L'
        IndexFinger1_L = 'IndexFinger1_L'
        IndexFinger2_L = 'IndexFinger2_L'
        IndexFinger3_L = 'IndexFinger3_L'
        IndexFinger4_L = 'IndexFinger4_L'
        Cup_L = 'Cup_L'
        PinkyFinger1_L = 'PinkyFinger1_L'
        PinkyFinger2_L = 'PinkyFinger2_L'
        PinkyFinger3_L = 'PinkyFinger3_L'
        PinkyFinger4_L = 'PinkyFinger4_L'
        RingFinger1_L = 'RingFinger1_L'
        RingFinger2_L = 'RingFinger2_L'
        RingFinger3_L = 'RingFinger3_L'
        RingFinger4_L = 'RingFinger4_L'
        Hip_L = 'Hip_L'
        Knee_L = 'Knee_L'
        Ankle_L = 'Ankle_L'
        Toes_L = 'Toes_L'
        ToesEnd_L = 'ToesEnd_L'

        All = [
            Root_M,
            Hip_R,
            Knee_R,
            Ankle_R,
            Toes_R,
            ToesEnd_R,
            Spine1_M,
            Spine2_M,
            Chest_M,
            Neck_M,
            Head_M,
            HeadEnd_M,
            Scapula_R,
            Shoulder_R,
            Elbow_R,
            Wrist_R,
            MiddleFinger1_R,
            MiddleFinger2_R,
            MiddleFinger3_R,
            MiddleFinger4_R,
            ThumbFinger1_R,
            ThumbFinger2_R,
            ThumbFinger3_R,
            ThumbFinger4_R,
            IndexFinger1_R,
            IndexFinger2_R,
            IndexFinger3_R,
            IndexFinger4_R,
            Cup_R,
            PinkyFinger1_R,
            PinkyFinger2_R,
            PinkyFinger3_R,
            PinkyFinger4_R,
            RingFinger1_R,
            RingFinger2_R,
            RingFinger3_R,
            RingFinger4_R,
            Scapula_L,
            Shoulder_L,
            Elbow_L,
            Wrist_L,
            MiddleFinger1_L,
            MiddleFinger2_L,
            MiddleFinger3_L,
            MiddleFinger4_L,
            ThumbFinger1_L,
            ThumbFinger2_L,
            ThumbFinger3_L,
            ThumbFinger4_L,
            IndexFinger1_L,
            IndexFinger2_L,
            IndexFinger3_L,
            IndexFinger4_L,
            Cup_L,
            PinkyFinger1_L,
            PinkyFinger2_L,
            PinkyFinger3_L,
            PinkyFinger4_L,
            RingFinger1_L,
            RingFinger2_L,
            RingFinger3_L,
            RingFinger4_L,
            Hip_L,
            Knee_L,
            Ankle_L,
            Toes_L,
            ToesEnd_L,

        ]

        Basic = [
            Root_M,
            Hip_R,
            Knee_R,
            Ankle_R,
            Toes_R,
            Spine1_M,
            Spine2_M,
            Chest_M,
            Neck_M,
            Head_M,
            Scapula_R,
            Shoulder_R,
            Elbow_R,
            Wrist_R,
            MiddleFinger1_R,
            MiddleFinger2_R,
            MiddleFinger3_R,
            ThumbFinger1_R,
            ThumbFinger2_R,
            ThumbFinger3_R,
            IndexFinger1_R,
            IndexFinger2_R,
            IndexFinger3_R,
            Cup_R,
            PinkyFinger1_R,
            PinkyFinger2_R,
            PinkyFinger3_R,
            RingFinger1_R,
            RingFinger2_R,
            RingFinger3_R,
            Scapula_L,
            Shoulder_L,
            Elbow_L,
            Wrist_L,
            MiddleFinger1_L,
            MiddleFinger2_L,
            MiddleFinger3_L,
            ThumbFinger1_L,
            ThumbFinger2_L,
            ThumbFinger3_L,
            IndexFinger1_L,
            IndexFinger2_L,
            IndexFinger3_L,
            Cup_L,
            PinkyFinger1_L,
            PinkyFinger2_L,
            PinkyFinger3_L,
            RingFinger1_L,
            RingFinger2_L,
            RingFinger3_L,
            Hip_L,
            Knee_L,
            Ankle_L,
            Toes_L,
        ]

        ExtraQuery = {
            Elbow_R: Shoulder_R,
            Wrist_R: Elbow_R,
            Elbow_L: Shoulder_L,
            Wrist_L: Elbow_L,
            #
            Knee_R: Hip_R,
            Knee_L: Hip_L,
        }

    class ChrMasterControlMap:
        Default = dict(
            Root_M='RootX_M',
            Spine1_M='FKSpine1_M',
            Spine2_M='FKSpine2_M',
            Chest_M='FKChest_M',
            Shoulder_R='FKShoulder_R',
            Elbow_R='FKElbow_R',
            Wrist_R='FKWrist_R',
            Neck_M='FKNeck_M',
            Head_M='FKHead_M',
            Shoulder_L='FKShoulder_L',
            Elbow_L='FKElbow_L',
            Wrist_L='FKWrist_L',
            Hip_R='FKHip_R',
            Knee_R='FKKnee_R',
            Ankle_R='FKAnkle_R',
            Toes_R='FKToes_R',
            Hip_L='FKHip_L',
            Knee_L='FKKnee_L',
            Ankle_L='FKAnkle_L',
            Toes_L='FKToes_L',
        )

    class ChrMasterSketchMap:
        ADV = dict(
            Root_M='Root_M',
            Hip_R='Hip_R',
            Knee_R='Knee_R',
            Ankle_R='Ankle_R',
            Toes_R='Toes_R',
            ToesEnd_R='ToesEnd_R',
            Spine1_M='Spine1_M',
            Spine2_M='Spine2_M',
            Chest_M='Chest_M',
            Neck_M='Neck_M',
            Head_M='Head_M',
            HeadEnd_M='HeadEnd_M',
            Scapula_R='Scapula_R',
            Shoulder_R='Shoulder_R',
            Elbow_R='Elbow_R',
            Wrist_R='Wrist_R',
            MiddleFinger1_R='MiddleFinger1_R',
            MiddleFinger2_R='MiddleFinger2_R',
            MiddleFinger3_R='MiddleFinger3_R',
            MiddleFinger4_R='MiddleFinger4_R',
            ThumbFinger1_R='ThumbFinger1_R',
            ThumbFinger2_R='ThumbFinger2_R',
            ThumbFinger3_R='ThumbFinger3_R',
            ThumbFinger4_R='ThumbFinger4_R',
            IndexFinger1_R='IndexFinger1_R',
            IndexFinger2_R='IndexFinger2_R',
            IndexFinger3_R='IndexFinger3_R',
            IndexFinger4_R='IndexFinger4_R',
            Cup_R='Cup_R',
            PinkyFinger1_R='PinkyFinger1_R',
            PinkyFinger2_R='PinkyFinger2_R',
            PinkyFinger3_R='PinkyFinger3_R',
            PinkyFinger4_R='PinkyFinger4_R',
            RingFinger1_R='RingFinger1_R',
            RingFinger2_R='RingFinger2_R',
            RingFinger3_R='RingFinger3_R',
            RingFinger4_R='RingFinger4_R',
            Scapula_L='Scapula_L',
            Shoulder_L='Shoulder_L',
            Elbow_L='Elbow_L',
            Wrist_L='Wrist_L',
            MiddleFinger1_L='MiddleFinger1_L',
            MiddleFinger2_L='MiddleFinger2_L',
            MiddleFinger3_L='MiddleFinger3_L',
            MiddleFinger4_L='MiddleFinger4_L',
            ThumbFinger1_L='ThumbFinger1_L',
            ThumbFinger2_L='ThumbFinger2_L',
            ThumbFinger3_L='ThumbFinger3_L',
            ThumbFinger4_L='ThumbFinger4_L',
            IndexFinger1_L='IndexFinger1_L',
            IndexFinger2_L='IndexFinger2_L',
            IndexFinger3_L='IndexFinger3_L',
            IndexFinger4_L='IndexFinger4_L',
            Cup_L='Cup_L',
            PinkyFinger1_L='PinkyFinger1_L',
            PinkyFinger2_L='PinkyFinger2_L',
            PinkyFinger3_L='PinkyFinger3_L',
            PinkyFinger4_L='PinkyFinger4_L',
            RingFinger1_L='RingFinger1_L',
            RingFinger2_L='RingFinger2_L',
            RingFinger3_L='RingFinger3_L',
            RingFinger4_L='RingFinger4_L',
            Hip_L='Hip_L',
            Knee_L='Knee_L',
            Ankle_L='Ankle_L',
            Toes_L='Toes_L',
            ToesEnd_L='ToesEnd_L',
        )
        # noinspection SpellCheckingInspection
        Mixamo=dict(
            Root_M='Hips',
            Hip_R='RightUpLeg',
            Knee_R='RightLeg',
            Ankle_R='RightFoot',
            Toes_R='RightToeBase',
            ToesEnd_R='RightToe_End',
            #
            Spine1_M='Spine',
            Spine2_M='Spine1',
            Chest_M='Spine2',
            Neck_M='Neck',
            Head_M='Head',
            HeadEnd_M='HeadTop_End',
            #
            Scapula_R='RightShoulder',
            Shoulder_R='RightArm',
            Elbow_R='RightForeArm',
            Wrist_R='RightHand',
            #
            # MiddleFinger1_R='MiddleFinger1_R',
            # MiddleFinger2_R='MiddleFinger2_R',
            # MiddleFinger3_R='MiddleFinger3_R',
            # MiddleFinger4_R='MiddleFinger4_R',
            # ThumbFinger1_R='ThumbFinger1_R',
            # ThumbFinger2_R='ThumbFinger2_R',
            # ThumbFinger3_R='ThumbFinger3_R',
            # ThumbFinger4_R='ThumbFinger4_R',
            # IndexFinger1_R='IndexFinger1_R',
            # IndexFinger2_R='IndexFinger2_R',
            # IndexFinger3_R='IndexFinger3_R',
            # IndexFinger4_R='IndexFinger4_R',
            # Cup_R='Cup_R',
            # PinkyFinger1_R='PinkyFinger1_R',
            # PinkyFinger2_R='PinkyFinger2_R',
            # PinkyFinger3_R='PinkyFinger3_R',
            # PinkyFinger4_R='PinkyFinger4_R',
            # RingFinger1_R='RingFinger1_R',
            # RingFinger2_R='RingFinger2_R',
            # RingFinger3_R='RingFinger3_R',
            # RingFinger4_R='RingFinger4_R',
            #
            Scapula_L='LeftShoulder',
            Shoulder_L='LeftArm',
            Elbow_L='LeftForeArm',
            Wrist_L='LeftHand',
            #
            # MiddleFinger1_L='MiddleFinger1_L',
            # MiddleFinger2_L='MiddleFinger2_L',
            # MiddleFinger3_L='MiddleFinger3_L',
            # MiddleFinger4_L='MiddleFinger4_L',
            # ThumbFinger1_L='ThumbFinger1_L',
            # ThumbFinger2_L='ThumbFinger2_L',
            # ThumbFinger3_L='ThumbFinger3_L',
            # ThumbFinger4_L='ThumbFinger4_L',
            # IndexFinger1_L='IndexFinger1_L',
            # IndexFinger2_L='IndexFinger2_L',
            # IndexFinger3_L='IndexFinger3_L',
            # IndexFinger4_L='IndexFinger4_L',
            # Cup_L='Cup_L',
            # PinkyFinger1_L='PinkyFinger1_L',
            # PinkyFinger2_L='PinkyFinger2_L',
            # PinkyFinger3_L='PinkyFinger3_L',
            # PinkyFinger4_L='PinkyFinger4_L',
            # RingFinger1_L='RingFinger1_L',
            # RingFinger2_L='RingFinger2_L',
            # RingFinger3_L='RingFinger3_L',
            # RingFinger4_L='RingFinger4_L',
            #
            Hip_L='LeftUpLeg',
            Knee_L='LeftLeg',
            Ankle_L='LeftFoot',
            Toes_L='LeftToeBase',
            ToesEnd_L='LeftToe_End',
        )

    class AtrKeys:
        Root = [
            'translateX', 'translateY', 'translateZ',
            'rotateX', 'rotateY', 'rotateZ'
        ]
        Default = [
            'rotateX', 'rotateY', 'rotateZ'
        ]

    DEFAULT_MASTER_ROOT_HEIGHT = 8.36773617093

    DEBUG_MODE = True

    @classmethod
    def find_spine_fnc(cls, sketch_root, sketch_key):
        return sketch_root.find_spine_for(sketch_key)

    @classmethod
    def print_keys(cls):
        _ = cmds.ls('test:OFFSET', type='joint', long=1, dag=1)
        for i in _:
            i_key = qsm_mya_core.DagNode.to_name_without_namespace(i)
            # print '{}, '.format(i_key)
            # print '{} = \'{}\''.format(i_key, i_key)
            print '{}=\'{}\','.format(i_key, i_key)
