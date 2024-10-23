# coding:utf-8
import collections
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

import lxbasic.core as bsc_core

import lxbasic.content as bsc_content

import lxbasic.model as bsc_model

import lxbasic.resource as bsc_resource

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from . import base as _base

from . import component as _component

from . import control as _control

from . import resource as _resource


class CharacterCurve(object):
    CURVE_TYPE_MAP = dict(
        translateX='animCurveTL',
        translateY='animCurveTL',
        translateZ='animCurveTL',
        rotateX='animCurveTA',
        rotateY='animCurveTA',
        rotateZ='animCurveTA',
        scaleX='animCurveTU',
        scaleY='animCurveTU',
        scaleZ='animCurveTU',
        visiblity='animCurveTU'
    )

    @classmethod
    def create(cls, path, atr_key, atr_name, values, start_frame, translation_scale=1.0):
        curve_name = '{}_{}'.format(
            path.split('|')[-1].split(':')[-1],
            atr_name.replace('.', '_')
        )
        curve_type = cls.CURVE_TYPE_MAP[atr_key]
        curve_name_new = cmds.createNode(curve_type, name=curve_name, skipSelect=1)

        atr_path_src = '{}.output'.format(curve_name_new)
        atr_path_tgt = '{}.{}'.format(path, atr_name)
        qsm_mya_core.Connection.create(atr_path_src, atr_path_tgt)

        curve_opt = qsm_mya_core.AnmCurveNodeOpt(curve_name_new)

        if atr_key in {
            'translateX',
            'translateY',
            'translateZ'
        }:
            value_scale = translation_scale
        else:
            value_scale = 1.0

        for i_index, i_value in enumerate(values):
            i_frame = i_index+start_frame
            curve_opt.create_value_at_time(i_frame, i_value*value_scale)

        return curve_name_new


class SketchCurve(object):
    CURVE_TYPE_MAP = dict(
        translateX='animCurveTL',
        translateY='animCurveTL',
        translateZ='animCurveTL',
        rotateX='animCurveTA',
        rotateY='animCurveTA',
        rotateZ='animCurveTA',
        scaleX='animCurveTU',
        scaleY='animCurveTU',
        scaleZ='animCurveTU',
        visiblity='animCurveTU'
    )

    @classmethod
    def to_curve_node_name(cls, sketch_path, atr_name):
        return '{}_{}'.format(
            sketch_path.split('|')[-1],
            atr_name.replace('.', '_')
        )

    @classmethod
    def create(cls, sketch_path, atr_name):
        curve_name = cls.to_curve_node_name(sketch_path, atr_name)
        if qsm_mya_core.Node.is_exists(curve_name) is True:
            return curve_name

        curve_type = cls.CURVE_TYPE_MAP[atr_name]
        curve_name_new = cmds.createNode(curve_type, name=curve_name, skipSelect=1)

        atr_path_src = '{}.output'.format(curve_name_new)
        atr_path_tgt = '{}.{}'.format(sketch_path, atr_name)
        qsm_mya_core.Connection.create(atr_path_src, atr_path_tgt)
        # setAttr "test:Hip_L_rotateZ.postInfinity" 4;
        qsm_mya_core.NodeAttribute.set_value(
            curve_name_new, 'preInfinity', 4
        )
        qsm_mya_core.NodeAttribute.set_value(
            curve_name_new, 'postInfinity', 4
        )
        return curve_name_new

    @classmethod
    def find_node(cls, sketch_path, atr_name):
        return qsm_mya_core.NodeAttribute.get_source_node(
            sketch_path, atr_name
        )

    @classmethod
    def appy_data(cls, curve_node, atr_name, values, start_frame, translation_scale):
        curve_opt = qsm_mya_core.AnmCurveNodeOpt(curve_node)

        if atr_name in {
            'translateX',
            'translateY',
            'translateZ'
        }:
            value_scale = translation_scale
        else:
            value_scale = 1.0

        for i_index, i_value in enumerate(values):
            i_frame = i_index+start_frame
            curve_opt.create_value_at_time(i_frame, i_value*value_scale)


class AdvMotionLayerBase(object):
    PROPERTY_KEYS_MAP = dict(
        transform=[
            'translateX',
            'translateY',
            'translateZ',
            'rotateX',
            'rotateY',
            'rotateZ',
        ],
        joint=[
            'translateX',
            'translateY',
            'translateZ',
            'rotateX',
            'rotateY',
            'rotateZ',
            'rotateOrder',
            'jointOrientX',
            'jointOrientY',
            'jointOrientZ',
        ]
    )

    MASTER_LAYER_NAME = 'MASTER_LAYER'
    LAYER_NAME = 'LAYER'

    def __init__(self, location):
        self._location = qsm_mya_core.DagNode.to_path(location)

    @classmethod
    def save_to(cls, location, file_path):
        location = qsm_mya_core.DagNode.to_path(location)
        c = bsc_content.Dict()
        _ = cmds.ls(location, dag=1, long=1) or []
        for i_path in _:
            if i_path == location:
                continue

            i_key = 'dag_nodes.{}'.format('/'.join(i_path[len(location):].split('|')))
            i_type = cmds.nodeType(i_path)

            i_properties = collections.OrderedDict()
            for j_key in cls.PROPERTY_KEYS_MAP[i_type]:
                i_properties[j_key] = cmds.getAttr(i_path+'.'+j_key)
            c.set(
                i_key,
                collections.OrderedDict(
                    [
                        ('type', i_type),
                        ('properties', i_properties)
                    ]
                )
            )
        #
        c.save_to(file_path)

    @classmethod
    def create_as_master_layer(cls, namespace):
        location = '{}:{}'.format(namespace, cls.MASTER_LAYER_NAME)
        if qsm_mya_core.Node.is_exists(location) is False:
            location = _component.MotionLayerGraph(
                namespace, 'motion/motion_master_layer'
            ).create_all()
            qsm_mya_core.NodeAttribute.create_as_string(
                location, 'qsm_type', 'motion_master_layer'
            )
            qsm_mya_core.NodeAttribute.create_as_message(
                location, 'qsm_resource'
            )
            cmds.addAttr(
                location, longName='qsm_layers',
                numberOfChildren=100, attributeType='compound'
            )
            for i in range(100):
                cmds.addAttr(
                    location, longName='layer_{}'.format(i),
                    attributeType='message',
                    parent='qsm_layers'
                )
            return True, location
        return False, location

    @classmethod
    def create_as_layer(cls, namespace):
        location = '{}:{}'.format(namespace, cls.LAYER_NAME)
        if qsm_mya_core.Node.is_exists(location) is False:
            clip_location = _component.MotionClipGraph(namespace).create_all()
            # blend_location = _component.MotionBlendGraph(namespace).create_all()
            location = _component.MotionLayerGraph(
                namespace, 'motion/motion_layer'
            ).create_all()
            qsm_mya_core.Container.add_dag_nodes(
                location,
                [
                    clip_location,
                    # blend_location
                ]
            )
            return True, location
        return False, location

    @classmethod
    def test_save(cls):
        pass
        # cls.save_to(
        #     '|LAYER',
        #     'E:/myworkspace/qosmic-2.0/source/qsm_dcc_extra/configures/motion/motion_layer_new_0.yml'
        # )

    @classmethod
    def test_build(cls):
        cls.create_as_layer(
            'test'
        )


# master
class AbsAdvMotionLayer(_base.MotionBase):

    @classmethod
    def update_root_start_opt(cls, motion_layer_opt, motion_layer_opt_last, start_frame):
        motion_layer_opt_last._node_opt.set('output_end', start_frame-1)
        pre_root_opt = qsm_mya_core.EtrNodeOpt(motion_layer_opt_last.find_root_end())
        motion_layer_opt._node_opt.set(
            'root_start_input_from', motion_layer_opt_last._node_opt.get('key')
        )

        for i_key, i_atr_src in [
            ('root_start_input_tx', 'translateX'),
            ('root_start_input_ty', 'translateY'),
            ('root_start_input_tz', 'translateZ'),
            ('root_start_input_rx', 'rotateX'),
            ('root_start_input_ry', 'rotateY'),
            ('root_start_input_rz', 'rotateZ')
        ]:
            i_curve_path = motion_layer_opt.get_message_from(i_key+'_curve')
            if i_curve_path is None:
                continue

            i_curve_opt = qsm_mya_core.AnmCurveNodeOpt(i_curve_path)
            i_curve_opt.create_value_at_time(start_frame, pre_root_opt.get(i_atr_src))
            i_curve_opt.set_tangent_types_at_time(start_frame, 'auto', 'step')

    @classmethod
    def update_root_start_for_self(cls, motion_layer_opt, start_frame):
        motion_layer_opt._node_opt.set('output_end', start_frame-1)
        pre_root_opt = qsm_mya_core.EtrNodeOpt(motion_layer_opt.find_root_start_src())
        motion_layer_opt._node_opt.set(
            'root_start_input_from', motion_layer_opt._node_opt.get('key')
        )

        for i_key, i_atr_src in [
            ('root_start_input_tx', 'translateX'),
            ('root_start_input_ty', 'translateY'),
            ('root_start_input_tz', 'translateZ'),
            ('root_start_input_rx', 'rotateX'),
            ('root_start_input_ry', 'rotateY'),
            ('root_start_input_rz', 'rotateZ')
        ]:
            i_curve_path = motion_layer_opt.get_message_from(i_key+'_curve')
            if i_curve_path is None:
                continue

            i_curve_opt = qsm_mya_core.AnmCurveNodeOpt(i_curve_path)
            i_curve_opt.create_value_at_time(start_frame, pre_root_opt.get(i_atr_src))
            i_curve_opt.set_tangent_types_at_time(start_frame, 'auto', 'step')

    @classmethod
    def find_master_layer_path(cls):
        _ = cmds.ls('*:MASTER_LAYER')
        if _:
            return _[0]

    def __init__(self, location):
        self._location = location
        self._namespace = qsm_mya_core.DagNode.to_namespace(self._location)

        self._node_opt = qsm_mya_core.EtrNodeOpt(self._location)

        self._sketches = cmds.ls(self._location, type='joint', long=1, dag=1) or []

        self._cache_dict = {}
        self._cache_all()

    def get_root(self):
        return self._location

    def find_offset_location(self):
        _ = cmds.ls('{}:OFFSET'.format(self._namespace), long=1)
        if _:
            return _[0]

    def find_layer_offset_location(self):
        _ = cmds.ls('{}:LAYER_OFFSET'.format(self._namespace), long=1)
        if _:
            return _[0]

    def find_root_sketch(self):
        _ = cmds.ls('{}:{}'.format(self._namespace, self.ChrMasterSketches.Root_M), long=1)
        if _:
            return _[0]

    def _cache_all(self):
        self._cache_dict.clear()

        for i_path in self._sketches:
            i_sketch_key = qsm_mya_core.DagNode.to_name_without_namespace(i_path)
            self._cache_dict[i_sketch_key] = i_path

    def get(self, sketch_key):
        return self._cache_dict.get(sketch_key)

    def get_all(self):
        return self._cache_dict.values()

    def reset(self):
        for i_sketch_key in self.ChrMasterSketches.Basic:
            i_sketch = self.get(i_sketch_key)
            if i_sketch_key == self.ChrMasterSketches.Root_M:
                _base.Sketch(i_sketch).reset_translations()
            _base.Sketch(i_sketch).reset_rotations()

    def apply_root_scale(self, scale):
        qsm_mya_core.NodeAttribute.set_as_tuple(
            self._location, 'scale', (scale, scale, scale)
        )
        
    def get_root_scale(self):
        return qsm_mya_core.NodeAttribute.get_value(
            self._location, 'scale'
        )[0][0]

    def set(self, key, value):
        self._node_opt.set(key, value)


class AdvChrMotionLayer(AbsAdvMotionLayer):
    CLIP_ATR_KEYS = [
        'startFrame',
        'preCycle',
        'postCycle',
        'scale',
        'hold',  # cut, etc. -5
        'sourceStart',
        'sourceEnd',
    ]

    @classmethod
    @qsm_mya_core.Undo.execute
    def create_for(cls, namespace):
        is_create, location = AdvMotionLayerBase.create_as_layer(
            namespace
        )
        if is_create is True:
            layer_opt = cls(location)
            layer_opt.set('key', namespace)
            cls.create_curves_for(layer_opt)
            return layer_opt
        return cls(location)

    @classmethod
    def create_curves_for(cls, layer_opt):
        curve_nodes = []
        time_container = layer_opt.get_time_container()
        for i_sketch_key in layer_opt.ChrMasterSketches.Basic:
            i_sketch = layer_opt.get(i_sketch_key)
            if i_sketch is None:
                continue

            if i_sketch_key == layer_opt.ChrMasterSketches.Root_M:
                i_atr_names = layer_opt.AtrKeys.Root
            else:
                i_atr_names = layer_opt.AtrKeys.Default

            for j_atr_name in i_atr_names:
                j_curve_node = SketchCurve.create(
                    i_sketch, j_atr_name,
                )
                qsm_mya_core.Connection.create(
                    time_container+'.output_source_time', j_curve_node+'.input'
                )
                curve_nodes.append(j_curve_node)

        qsm_mya_core.Container.add_nodes(time_container, curve_nodes)

    @classmethod
    def apply_data_for(
        cls,
        layer_opt, data,
        start_frame=1,
        pre_cycle=0, post_cycle=1,
        pre_blend=4, post_blend=4
    ):
        location = layer_opt.get_root()
        sketch_data = data['sketches']

        frame_count = data['frame_count']
        root_height = data['root_height']

        master_root_height = cls.DEFAULT_MASTER_ROOT_HEIGHT
        translation_scale = master_root_height/root_height

        speed = 1.0

        source_start = 1
        source_end = source_start+frame_count-1

        clip_start = start_frame
        clip_end = clip_start+frame_count*post_cycle-1
        count = clip_end-clip_start+1

        qsm_mya_core.NodeAttribute.set_value(
            location, 'output_end', clip_end
        )
        # clip
        qsm_mya_core.NodeAttribute.set_value(
            location, 'clip_start', clip_start
        )
        qsm_mya_core.NodeAttribute.set_value(
            location, 'clip_end', clip_end
        )
        # basic
        qsm_mya_core.NodeAttribute.set_value(
            location, 'start', clip_start
        )
        qsm_mya_core.NodeAttribute.set_value(
            location, 'speed', speed
        )
        qsm_mya_core.NodeAttribute.set_value(
            location, 'count', count
        )
        # cycle
        qsm_mya_core.NodeAttribute.set_value(
            location, 'source_start', source_start
        )
        qsm_mya_core.NodeAttribute.set_value(
            location, 'source_end', source_end
        )
        qsm_mya_core.NodeAttribute.set_value(
            location, 'pre_cycle', pre_cycle
        )
        qsm_mya_core.NodeAttribute.set_value(
            location, 'post_cycle', post_cycle
        )
        # scale
        qsm_mya_core.NodeAttribute.set_value(
            location, 'scale_start', clip_start
        )
        qsm_mya_core.NodeAttribute.set_value(
            location, 'scale_end', clip_end
        )
        # blend
        qsm_mya_core.NodeAttribute.set_value(
            location, 'pre_blend', pre_blend
        )
        qsm_mya_core.NodeAttribute.set_value(
            location, 'post_blend', post_blend
        )
        #
        qsm_mya_core.NodeAttribute.set_value(
            location, 'valid_start', clip_start
        )
        qsm_mya_core.NodeAttribute.set_value(
            location, 'valid_end', clip_end
        )
        # old variant
        qsm_mya_core.NodeAttribute.set_value(
            location, 'blend_start_time', clip_start
        )
        qsm_mya_core.NodeAttribute.set_value(
            location, 'blend_end_time', clip_end
        )
        #
        for i_sketch_key, i_v in sketch_data.items():
            i_sketch_path = layer_opt.get(i_sketch_key)
            i_orients = i_v['orients']
            i_time_samples = i_v['time_samples']
            cls.apply_orient_for(i_sketch_path, i_orients)
            cls.apply_time_samples_for_(i_sketch_path, i_time_samples, source_start, translation_scale)

        # connect main_weight to constraint
        weight_attributes = layer_opt.get_constraint_weight_attributes()
        for i_weight_atr in weight_attributes:
            cmds.connectAttr(
                location+'.main_weight_bypass', i_weight_atr,
                force=1
            )
        return clip_start, clip_end

    @classmethod
    def test(cls):
        pass

    @classmethod
    def test_1(cls):
        motion_layer_opt = cls.create_for(
            'test_1'
        )
        data = bsc_storage.StgFileOpt(
            'E:/myworkspace/qosmic-2.0/source/qsm_dcc_extra/resources/motion/sam_run_forward.json'
            # 'E:/myworkspace/qosmic-2.0/source/qsm_dcc_extra/resources/motion/mixamo_run_forward.json'
        ).set_read()
        cls.apply_data_for(motion_layer_opt, data, post_cycle=3)

    def __init__(self, *args, **kwargs):
        super(AdvChrMotionLayer, self).__init__(*args, **kwargs)

    def get_time_container(self):
        return qsm_mya_core.NodeAttribute.get_as_message(
            self._location, 'TIME'
        )

    @classmethod
    def apply_orient_for(cls, sketch_path, orients):
        for i_k, i_v in orients.items():
            cmds.setAttr(sketch_path+'.'+i_k, i_v)

    @classmethod
    def apply_time_samples_for_(cls, sketch_path, time_samples, start_frame, translation_scale=1.0):
        for i_atr_name, i_values in time_samples.items():
            i_curve_node_name = SketchCurve.to_curve_node_name(sketch_path, i_atr_name)
            if qsm_mya_core.Node.is_exists(i_curve_node_name) is False:
                continue
            SketchCurve.appy_data(
                i_curve_node_name, i_atr_name, i_values, start_frame, translation_scale
            )

    @classmethod
    def apply_time_samples_for(cls, character, path, time_samples, start_frame, translation_scale=1.0):
        # key to character
        curve_map = dict()
        name = qsm_mya_core.DagNode.to_name(path)
        for i_key, i_v in time_samples.items():
            # sam_Skin__walk_test:Toes_L_rotateX
            # convert attribute to maya character
            i_atr_name = name+'_'+i_key
            i_curve_name = CharacterCurve.create(character, i_key, i_atr_name, i_v, start_frame, translation_scale)
            curve_map[i_key] = i_curve_name
        return curve_map

    def constraint_to_master(self, master_motion_layer):
        if isinstance(master_motion_layer, AbsAdvMotionLayer) is True:
            for i_sketch_key in self.ChrMasterSketches.Basic:
                i_sketch_src = self.get(i_sketch_key)
                i_sketch_dst = master_motion_layer.get(i_sketch_key)
                if i_sketch_key == self.ChrMasterSketches.Root_M:
                    _base.Sketch(i_sketch_src).create_point_constraint_to_master_layer(i_sketch_dst)
                _base.Sketch(i_sketch_src).create_orient_constraint_to_master_layer(i_sketch_dst)

    def get_constraint_weight_attributes(self):
        list_ = []
        for i_sketch_key in self.ChrMasterSketches.Basic:
            i_sketch_src = self.get(i_sketch_key)
            if i_sketch_key == self.ChrMasterSketches.Root_M:
                i_translate_connections = qsm_mya_core.NodeAttribute.get_all_target_connections(
                    i_sketch_src+'.translate'
                )
                if i_translate_connections:
                    i_atr = i_translate_connections[0][1]
                    i_atr_dst = '.'.join(i_atr.split('.')[:-1]+['targetWeight'])
                    list_.append(i_atr_dst)

            i_rotate_connections = qsm_mya_core.NodeAttribute.get_all_target_connections(
                i_sketch_src+'.rotate'
            )
            if i_rotate_connections:
                i_atr = i_rotate_connections[0][1]
                i_atr_dst = '.'.join(i_atr.split('.')[:-1]+['targetWeight'])
                list_.append(i_atr_dst)
        return list_

    def get_end_frame(self):
        return qsm_mya_core.NodeAttribute.get_value(
            self._location, 'clip_end'
        )

    def get_start_frame(self):
        return qsm_mya_core.NodeAttribute.get_value(
            self._location, 'clip_start'
        )

    def get_source_end_frame(self):
        return qsm_mya_core.NodeAttribute.get_value(
            self._location, 'source_end'
        )

    def get_source_start_frame(self):
        return qsm_mya_core.NodeAttribute.get_value(
            self._location, 'source_start'
        )

    def generate_end_root_sketch_transformations(self):
        end_frame = self.get_end_frame()
        root_scale = self.get_root_scale()
        transformations = cmds.xform(
            self.find_root_sketch(),
            translation=1, worldSpace=1, query=1
        )
        print transformations, root_scale

    def find_root_start(self):
        _ = cmds.ls('{}:{}'.format(self._namespace, 'ROOT_START'), long=1)
        if _:
            return _[0]

    def find_root_start_src(self):
        _ = cmds.ls('{}:{}'.format(self._namespace, 'ROOT_START_SRC'), long=1)
        if _:
            return _[0]

    def find_root_start_input(self):
        _ = cmds.ls('{}:{}'.format(self._namespace, 'ROOT_START_INPUT'), long=1)
        if _:
            return _[0]

    def find_root_start_constraint(self):
        _ = cmds.ls('{}:{}'.format(self._namespace, 'ROOT_START_PRC'), long=1)
        if _:
            return _[0]

    def find_root_end(self):
        _ = cmds.ls('{}:{}'.format(self._namespace, 'ROOT_END'), long=1)
        if _:
            return _[0]

    def set_layer_index(self, layer_index):
        qsm_mya_core.NodeAttribute.set_value(
            self._location, 'layer_index', layer_index
        )

    def update_main_weight(self, frame_range, is_start=False, is_end=False):
        curve_opt = self.get_main_weight_curve_opt()

        pre_blend, post_blend = 4, 4

        start_frame, end_frame = frame_range

        condition = [is_start, is_end]
        if condition == [True, True]:
            curve_opt.create_value_at_time(start_frame, 1)
            curve_opt.create_value_at_time(end_frame, 1)
        elif condition == [True, False]:
            curve_opt.create_value_at_time(start_frame, 1)
            curve_opt.create_value_at_time(end_frame, 1)
            curve_opt.create_value_at_time(end_frame+post_blend, 0)
        elif condition == [False, True]:
            curve_opt.create_value_at_time(start_frame-pre_blend, 0)
            curve_opt.create_value_at_time(start_frame, 1)
            curve_opt.create_value_at_time(end_frame, 1)
        else:
            if start_frame == end_frame:
                curve_opt.create_value_at_time(start_frame-pre_blend, 0)
                curve_opt.create_value_at_time(start_frame, 1)
                curve_opt.create_value_at_time(start_frame+post_blend, 0)
            else:
                curve_opt.create_value_at_time(start_frame-pre_blend, 0)
                curve_opt.create_value_at_time(start_frame, 1)
                curve_opt.create_value_at_time(end_frame, 1)
                curve_opt.create_value_at_time(end_frame+post_blend, 0)

    def update_main_weight_auto(self, is_start, is_end):
        clip_start, clip_end = self._node_opt.get('clip_start'), self._node_opt.get('clip_end')
        self.update_main_weight((clip_start, clip_end), is_start, is_end)

    def restore_main_weight_curve(self):
        curve_opt = self.get_main_weight_curve_opt()
        if curve_opt is not None:
            curve_opt.delete()

        curve_opt = qsm_mya_core.AnmCurveNodeOpt.create(self._location, 'main_weight', True)
        qsm_mya_core.NodeAttribute.set_as_message(
            self._location, 'main_weight_curve', curve_opt.path
        )

    def get_root_start_input_transformation_curves_kwargs(self):
        dict_ = {}
        for i_key, i_atr_src in [
            ('root_start_input_tx', 'translateX'),
            ('root_start_input_ty', 'translateY'),
            ('root_start_input_tz', 'translateZ'),
            ('root_start_input_rx', 'rotateX'),
            ('root_start_input_ry', 'rotateY'),
            ('root_start_input_rz', 'rotateZ')
        ]:
            i_curve = qsm_mya_core.NodeAttribute.get_as_message(
                self._location, i_key+'_curve'
            )
            if i_curve:
                i_curve_opt = qsm_mya_core.AnmCurveNodeOpt(i_curve)
            else:
                i_curve_opt = None
            dict_[i_key] = i_curve_opt, i_atr_src
        return dict_

    def restore_root_start_input_transformation_curves(self):
        curve_kwargs = self.get_root_start_input_transformation_curves_kwargs()
        for i_key, (i_curve_opt, i_atr_src) in curve_kwargs.items():
            if i_curve_opt is not None:
                i_curve_opt.delete()

            i_curve_typ = CharacterCurve.CURVE_TYPE_MAP[i_atr_src]
            i_curve_opt = qsm_mya_core.AnmCurveNodeOpt.create(
                self._location, i_key, keep_namespace=True, curve_type=i_curve_typ
            )

            qsm_mya_core.NodeAttribute.set_as_message(
                self._location, i_key+'_curve', i_curve_opt.path
            )

    def update_output_end(self, frame_range):
        curve_opt = self.get_output_end_curve_opt()

        start_frame, end_frame = frame_range
        curve_opt.create_value_at_time(end_frame+1, end_frame)

    def reset_root_start_input(self):
        curve_opt = self.get_output_end_curve_opt()
        if curve_opt is not None:
            curve_opt.delete()
        curve_opt = qsm_mya_core.AnmCurveNodeOpt.create(self._location, 'output_end', True)
        qsm_mya_core.NodeAttribute.set_as_message(
            self._location, 'output_end_curve', curve_opt.path
        )

    def get_output_end_curve_opt(self):
        _ = qsm_mya_core.NodeAttribute.get_as_message(
                self._location, 'output_end'
            )
        if _:
            return qsm_mya_core.AnmCurveNodeOpt(
                _
            )

    def get_main_weight_curve_opt(self):
        _ = self.get_message_from(
            'main_weight_curve'
        )
        if _:
            return qsm_mya_core.AnmCurveNodeOpt(
                _
            )

    def get_message_from(self, key):
        return qsm_mya_core.NodeAttribute.get_as_message(
            self._location, key
        )

    def generate_kwargs(self):
        kwargs = {}
        keys = bsc_model.TrackModel.MAIN_KEYS
        for j_key in keys:
            kwargs[j_key] = self._node_opt.get(j_key)
        return kwargs


class AdvChrMotionMasterLayerOpt(AbsAdvMotionLayer):
    @classmethod
    @qsm_mya_core.Undo.execute
    def create_for(cls, namespace):
        is_create, location = AdvMotionLayerBase.create_as_master_layer(namespace)
        return cls(location)

    def __init__(self, *args, **kwargs):
        super(AdvChrMotionMasterLayerOpt, self).__init__(*args, **kwargs)

    def export_motion_to(self, file_path):
        namespace = self.get_resource_namespace()
        start_frame, end_frame = self.get_frame_range()
        resource = _resource.AdvResource(namespace)
        main_control_keys = self.ChrMasterControlMap.Default.values()
        main_controls = [resource._control_set.get(x) for x in main_control_keys]
        main_controls = list(filter(None, main_controls))

        # fixme: face control is ignore?
        main_control_set = _control.AdvControlSet(main_controls)
        main_control_set.bake_all_keyframes(
            start_frame, end_frame,
            attributes=[
                'translateX', 'translateY', 'translateZ',
                'rotateX', 'rotateY', 'rotateZ',
            ]
        )
        resource._control_set.export_motion_to(file_path)
        cmds.undo()

    def connect_to_resource(self, adv_resource):
        qsm_mya_core.NodeAttribute.set_as_message(
            self._location, 'qsm_resource', adv_resource.get_root()
        )
        adv_resource.fit_master_layer_scale(self)
        adv_resource.fit_layer_sketches(self)
        adv_resource.constraint_from_master_layer(self)

    def get_next_layer_index(self):
        for i in range(100):
            if not cmds.listConnections(
                '{}.qsm_layers.layer_{}'.format(
                    self._location, i
                ), destination=0, source=1
            ):
                return i
        return 0

    def get_resource_namespace(self):
        resource_root = qsm_mya_core.NodeAttribute.get_as_message(
            self._location, 'qsm_resource'
        )
        return qsm_mya_core.DagNode.to_namespace(resource_root)

    @qsm_mya_core.Undo.execute
    def append_layer(self, file_path, pre_cycle=1, post_cycle=1, pre_blend=2, post_blend=2):
        if not bsc_storage.StgPath.get_is_file(file_path):
            raise OSError()

        resource_namespace = self.get_resource_namespace()

        layers_opt = AdvMotionLayersOpt(self.get_all_layers())

        stage_end_frame = layers_opt.get_end_frame()
        motion_layer_opt_last = layers_opt.get_end_layer()

        layer_index = self.get_next_layer_index()

        file_opt = bsc_storage.StgFileOpt(file_path)
        name = bsc_core.BscText.clear_up_to(file_opt.name_base)
        layer_namespace = '{}_{}_{}'.format(resource_namespace, name, layer_index)
        motion_layer_opt = AdvChrMotionLayer.create_for(layer_namespace)
        self.fit_layer_scale(motion_layer_opt)
        motion_layer_opt.constraint_to_master(self)
        data = bsc_storage.StgFileOpt(file_path).set_read()

        qsm_mya_core.NodeAttribute.set_as_message(
            self._location, 'qsm_layers.layer_{}'.format(layer_index), motion_layer_opt.get_root()
        )
        motion_layer_opt.set_layer_index(layer_index)
        clip_start, clip_end = motion_layer_opt.apply_data_for(
            motion_layer_opt,
            data,
            start_frame=stage_end_frame+1,
            post_cycle=post_cycle,
            pre_blend=pre_blend, post_blend=post_blend
        )

        motion_layer_opt.restore_main_weight_curve()
        motion_layer_opt.restore_root_start_input_transformation_curves()
        if motion_layer_opt_last is not None:
            motion_layer_opt.update_main_weight((clip_start, clip_end), is_start=False, is_end=True)
            self.update_root_start_opt(motion_layer_opt, motion_layer_opt_last, clip_start)
            # check exists layer count, when count is 1, last layer is start layer
            if layers_opt.get_layer_count() == 1:
                motion_layer_opt_last.update_main_weight_auto(is_start=True, is_end=False)
            else:
                motion_layer_opt_last.update_main_weight_auto(is_start=False, is_end=False)
        else:
            motion_layer_opt.update_main_weight((clip_start, clip_end), is_start=True, is_end=True)
            self.update_root_start_for_self(motion_layer_opt, clip_start)

        return motion_layer_opt

    def fit_layer_scale(self, layer_opt):
        scale = cmds.getAttr(self._location+'.scaleX')
        layer_opt.apply_root_scale(scale)

    def get_all_layers(self):
        list_ = []
        for i in range(100):
            _ = cmds.listConnections(
                '{}.qsm_layers.layer_{}'.format(
                    self._location, i
                ), destination=0, source=1
            )
            if _:
                list_.append(_[0].split('.')[0])
        return list_

    def get_all_layer_names(self):
        return [x.split(':')[0] for x in self.get_all_layers()]

    def get_frame_range(self):
        layers_opt = AdvMotionLayersOpt(self.get_all_layers())
        return layers_opt.get_frame_range()

    def generate_track_data(self):
        for i in self.get_all_layers():
            pass

    @classmethod
    def test(cls):
        """
import qsm_maya_lazy_tool
reload(qsm_maya_lazy_tool)
qsm_maya_lazy_tool.do_reload()

import qsm_maya_lazy.montage.core as c

c.AdvChrMotionMasterLayerOpt.test()
        """
        cls(
            cls.find_master_layer_path()
        ).export_motion_to(
            'Z:/temporaries/montage_test/test_1.jsz'
        )


class AdvMotionStage(object):

    @classmethod
    def find_master_layer_path(cls):
        _ = cmds.ls('*:MASTER_LAYER', long=1)
        if _:
            for i in _:
                if cmds.objExists('{}.qsm_type'.format(i)):
                    if cmds.getAttr('{}.qsm_type'.format(i)) == 'motion_master_layer':
                        return i

    def __init__(self):
        self._master_layer = self.find_master_layer_path()

    def generate_track_data(self):
        list_ = []
        if self._master_layer is None:
            return

        opt = AdvChrMotionMasterLayerOpt(self._master_layer)
        for i_path in opt.get_all_layers():
            i_kwargs = AdvChrMotionLayer(i_path).generate_kwargs()
            list_.append(i_kwargs)
        return list_
    
    def get_all_layers(self):
        if self._master_layer is None:
            return []

        opt = AdvChrMotionMasterLayerOpt(self._master_layer)
        return opt.get_all_layers()

    def get_all_layer_names(self):
        if self._master_layer is None:
            return []

        opt = AdvChrMotionMasterLayerOpt(self._master_layer)
        return opt.get_all_layer_names()


class AdvMotionLayersOpt(object):
    def __init__(self, locations):
        self._layers = [AdvChrMotionLayer(x) for x in locations]

    def get_end_layer(self):
        if self._layers:
            dict_ = {}
            for i in self._layers:
                i_end_frame = i.get_end_frame()
                dict_.setdefault(i_end_frame, []).append(i)
            end_frames = dict_.keys()
            return dict_[max(end_frames)][-1]
        return None

    def get_layer_count(self):
        return len(self._layers)

    def get_start_frame(self):
        _ = [x.get_start_frame() for x in self._layers]
        if _:
            return min(_)
        return 0

    def get_end_frame(self):
        _ = [x.get_end_frame() for x in self._layers]
        if _:
            return max(_)
        return 0

    def get_frame_range(self):
        return self.get_start_frame(), self.get_end_frame()
