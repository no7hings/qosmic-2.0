# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core


class AbsMontage(object):
    ROOT_PATH = '|__MONTAGE__'

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
            Scapula_R='FKScapula_R',
            Shoulder_R='FKShoulder_R',
            Elbow_R='FKElbow_R',
            Wrist_R='FKWrist_R',
            Neck_M='FKNeck_M',
            Head_M='FKHead_M',
            Scapula_L='FKScapula_L',
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
            # fingers
            MiddleFinger1_R='FKMiddleFinger1_R',
            MiddleFinger2_R='FKMiddleFinger2_R',
            MiddleFinger3_R='FKMiddleFinger3_R',
            #
            ThumbFinger1_R='FKThumbFinger1_R',
            ThumbFinger2_R='FKThumbFinger2_R',
            ThumbFinger3_R='FKThumbFinger3_R',
            #
            IndexFinger1_R='FKIndexFinger1_R',
            IndexFinger2_R='FKIndexFinger2_R',
            IndexFinger3_R='FKIndexFinger3_R',
            #
            PinkyFinger1_R='FKPinkyFinger1_R',
            PinkyFinger2_R='FKPinkyFinger2_R',
            PinkyFinger3_R='FKPinkyFinger3_R',
            #
            RingFinger1_R='FKRingFinger1_R',
            RingFinger2_R='FKRingFinger2_R',
            RingFinger3_R='FKRingFinger3_R',
            #
            MiddleFinger1_L='FKMiddleFinger1_L',
            MiddleFinger2_L='FKMiddleFinger2_L',
            MiddleFinger3_L='FKMiddleFinger3_L',
            MiddleFinger4_L='FKMiddleFinger4_L',
            #
            ThumbFinger1_L='FKThumbFinger1_L',
            ThumbFinger2_L='FKThumbFinger2_L',
            ThumbFinger3_L='FKThumbFinger3_L',
            ThumbFinger4_L='FKThumbFinger4_L',
            #
            IndexFinger1_L='FKIndexFinger1_L',
            IndexFinger2_L='FKIndexFinger2_L',
            IndexFinger3_L='FKIndexFinger3_L',
            IndexFinger4_L='FKIndexFinger4_L',
            #
            PinkyFinger1_L='FKPinkyFinger1_L',
            PinkyFinger2_L='FKPinkyFinger2_L',
            PinkyFinger3_L='FKPinkyFinger3_L',
            PinkyFinger4_L='FKPinkyFinger4_L',
            #
            RingFinger1_L='FKRingFinger1_L',
            RingFinger2_L='FKRingFinger2_L',
            RingFinger3_L='FKRingFinger3_L',
            RingFinger4_L='FKRingFinger4_L',
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
        MoCap=dict(
            Root_M='Hips',
            Hip_R='RightUpLeg',
            Knee_R='RightLeg',
            Ankle_R='RightFoot',
            Toes_R='RightToeBase',
            ToesEnd_R=['RightToe_End', 'RightToeBaseEnd'],
            #
            Spine1_M='Spine',
            Spine2_M='Spine1',
            Chest_M='Spine2',
            Neck_M='Neck',
            Head_M='Head',
            HeadEnd_M=['HeadTop_End', 'HeadEnd'],
            #
            Scapula_R='RightShoulder',
            Shoulder_R='RightArm',
            Elbow_R='RightForeArm',
            Wrist_R='RightHand',
            #
            MiddleFinger1_R='RightHandMiddle1',
            MiddleFinger2_R='RightHandMiddle2',
            MiddleFinger3_R='RightHandMiddle3',
            MiddleFinger4_R='RightHandMiddle4',
            #
            ThumbFinger1_R='RightHandThumb1',
            ThumbFinger2_R='RightHandThumb2',
            ThumbFinger3_R='RightHandThumb3',
            ThumbFinger4_R='RightHandThumb4',
            #
            IndexFinger1_R='RightHandIndex1',
            IndexFinger2_R='RightHandIndex2',
            IndexFinger3_R='RightHandIndex3',
            IndexFinger4_R='RightHandIndex4',
            #
            PinkyFinger1_R='RightHandPinky1',
            PinkyFinger2_R='RightHandPinky2',
            PinkyFinger3_R='RightHandPinky3',
            PinkyFinger4_R='RightHandPinky4',
            #
            RingFinger1_R='RightHandRing1',
            RingFinger2_R='RightHandRing2',
            RingFinger3_R='RightHandRing3',
            RingFinger4_R='RightHandRing4',
            #
            Scapula_L='LeftShoulder',
            Shoulder_L='LeftArm',
            Elbow_L='LeftForeArm',
            Wrist_L='LeftHand',
            #
            MiddleFinger1_L='LeftHandMiddle1',
            MiddleFinger2_L='LeftHandMiddle2',
            MiddleFinger3_L='LeftHandMiddle3',
            MiddleFinger4_L='LeftHandMiddle4',
            #
            ThumbFinger1_L='LeftHandThumb1',
            ThumbFinger2_L='LeftHandThumb2',
            ThumbFinger3_L='LeftHandThumb3',
            ThumbFinger4_L='LeftHandThumb4',
            #
            IndexFinger1_L='LeftHandIndex1',
            IndexFinger2_L='LeftHandIndex2',
            IndexFinger3_L='LeftHandIndex3',
            IndexFinger4_L='LeftHandIndex4',
            #
            PinkyFinger1_L='LeftHandPinky1',
            PinkyFinger2_L='LeftHandPinky2',
            PinkyFinger3_L='LeftHandPinky3',
            PinkyFinger4_L='LeftHandPinky4',
            #
            RingFinger1_L='LeftHandRing1',
            RingFinger2_L='LeftHandRing2',
            RingFinger3_L='LeftHandRing3',
            RingFinger4_L='LeftHandRing4',
            #
            Hip_L='LeftUpLeg',
            Knee_L='LeftLeg',
            Ankle_L='LeftFoot',
            Toes_L='LeftToeBase',
            ToesEnd_L=['LeftToe_End', 'LeftToeBaseEnd'],
        )

    class AtrKeys:
        Root = [
            'translateX', 'translateY', 'translateZ',
            'rotateX', 'rotateY', 'rotateZ'
        ]
        Default = [
            'rotateX', 'rotateY', 'rotateZ'
        ]

    class Namespaces:
        Transfer = 'transfer'

    DEFAULT_MASTER_LOWER_HEIGHT = 8.36773617093
    DEFAULT_MASTER_HEIGHT = 15.2693830421
    DEFAULT_MASTER_UPPER_HEIGHT = 6.83376148885

    DEBUG_MODE = True

    @classmethod
    def find_spine_fnc(cls, sketch_root, sketch_key):
        return sketch_root.find_spine_for(sketch_key)

    @classmethod
    def create_root(cls):
        if cmds.objExists(cls.ROOT_PATH) is False:
            name = cls.ROOT_PATH.split('|')[-1]
            cmds.createNode(
                'dagContainer', name=name, shared=1, skipSelect=1
            )
            cmds.setAttr(
                cls.ROOT_PATH+'.iconName', 'folder-closed.png', type='string'
            )
        return cls.ROOT_PATH
