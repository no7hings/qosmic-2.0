# coding:utf-8
import collections
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

import lxbasic.content as bsc_content

import lxbasic.resource as bsc_resource

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from . import base as _base

from . import component as _component


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
        atr_path_dst = '{}.{}'.format(path, atr_name)
        qsm_mya_core.Connection.create(atr_path_src, atr_path_dst)

        curve_opt = qsm_mya_core.AnmCurveOpt(curve_name_new)

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
            curve_opt.set_value_at_frame(i_frame, i_value*value_scale)

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
        atr_path_dst = '{}.{}'.format(sketch_path, atr_name)
        qsm_mya_core.Connection.create(atr_path_src, atr_path_dst)
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
        curve_opt = qsm_mya_core.AnmCurveOpt(curve_node)

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
            curve_opt.set_value_at_frame(i_frame, i_value*value_scale)


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
            blend_location = _component.MotionBlendGraph(namespace).create_all()
            location = _component.MotionLayerGraph(
                namespace, 'motion/motion_layer'
            ).create_all()
            qsm_mya_core.Container.add_dag_nodes(location, [clip_location, blend_location])
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
    def __init__(self, location):
        self._location = location
        self._namespace = qsm_mya_core.DagNode.to_namespace(self._location)

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
            layer = cls(location)
            cls.create_curves_for(layer)
            return layer
        return cls(location)

    @classmethod
    def create_curves_for(cls, layer):
        curve_nodes = []
        clip = layer.get_clip()
        for i_sketch_key in layer.ChrMasterSketches.Basic:
            i_sketch = layer.get(i_sketch_key)
            if i_sketch is None:
                continue

            if i_sketch_key == layer.ChrMasterSketches.Root_M:
                i_atr_names = layer.AtrKeys.Root
            else:
                i_atr_names = layer.AtrKeys.Default

            for j_atr_name in i_atr_names:
                j_curve_node = SketchCurve.create(
                    i_sketch, j_atr_name,
                )
                qsm_mya_core.Connection.create(
                    clip+'.output_time', j_curve_node+'.input'
                )
                curve_nodes.append(j_curve_node)

        qsm_mya_core.Container.add_nodes(clip, curve_nodes)

    @classmethod
    def apply_data_for(cls, layer, data, start_frame=1, post_cycle=1, pre_blend_frame=2, post_blend_frame=2):
        location = layer.get_root()
        sketch_data = data['sketches']
        frame_count = data['frame_count']
        root_height = data['root_height']
        master_root_height = cls.DEFAULT_MASTER_ROOT_HEIGHT
        translation_scale = master_root_height/root_height
        source_start_frame = 0
        source_end_frame = source_start_frame+frame_count-1
        end_frame = start_frame+frame_count*post_cycle-1
        pre_cycle = 0

        # curve_opt = qsm_mya_core.AnmCurveOpt.create(location, 'main_weight')
        # curve_opt.set_value_at_frame(start_frame-pre_blend_frame, 0)
        # curve_opt.set_value_at_frame(start_frame, 1)
        # curve_opt.set_value_at_frame(end_frame, 1)
        # curve_opt.set_value_at_frame(end_frame+post_blend_frame, 0)

        qsm_mya_core.NodeAttribute.set_value(
            location, 'blend_start_frame', start_frame
        )
        qsm_mya_core.NodeAttribute.set_value(
            location, 'blend_end_frame', end_frame
        )

        qsm_mya_core.NodeAttribute.set_value(
            location, 'start_frame', start_frame
        )
        qsm_mya_core.NodeAttribute.set_value(
            location, 'end_frame', end_frame
        )
        qsm_mya_core.NodeAttribute.set_value(
            location, 'pre_blend_frame', pre_blend_frame
        )
        qsm_mya_core.NodeAttribute.set_value(
            location, 'post_blend_frame', post_blend_frame
        )
        qsm_mya_core.NodeAttribute.set_value(
            location, 'source_start_frame', source_start_frame
        )
        qsm_mya_core.NodeAttribute.set_value(
            location, 'source_end_frame', source_end_frame
        )
        qsm_mya_core.NodeAttribute.set_value(
            location, 'pre_cycle', pre_cycle
        )
        qsm_mya_core.NodeAttribute.set_value(
            location, 'post_cycle', post_cycle
        )
        for i_sketch_key, i_v in sketch_data.items():
            i_sketch_path = layer.get(i_sketch_key)
            i_orients = i_v['orients']
            i_time_samples = i_v['time_samples']
            cls.apply_orient_for(i_sketch_path, i_orients)
            cls.apply_time_samples_for_(i_sketch_path, i_time_samples, source_start_frame, translation_scale)

        # connect main_weight to constraint
        weight_attributes = layer.get_constraint_weight_attributes()
        for i_weight_atr in weight_attributes:
            cmds.connectAttr(
                location+'.main_weight', i_weight_atr,
                force=1
            )

    @classmethod
    def test(cls):
        pass

    @classmethod
    def test_1(cls):
        motion_layer = cls.create_for(
            'test_1'
        )
        data = bsc_storage.StgFileOpt(
            'E:/myworkspace/qosmic-2.0/source/qsm_dcc_extra/resources/motion/sam_run_turn_left.json'
            # 'E:/myworkspace/qosmic-2.0/source/qsm_dcc_extra/resources/motion/mixamo_run_forward.json'
        ).set_read()
        cls.apply_data_for(motion_layer, data, post_cycle=1)

    def __init__(self, *args, **kwargs):
        super(AdvChrMotionLayer, self).__init__(*args, **kwargs)

    def get_clip(self):
        return qsm_mya_core.NodeAttribute.get_as_message(
            self._location, 'clip'
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
                    # i_atr_src = qsm_mya_core.NodeAttribute.get_source_(i_atr_dst)
                    list_.append(i_atr_dst)

            i_rotate_connections = qsm_mya_core.NodeAttribute.get_all_target_connections(
                i_sketch_src+'.rotate'
            )
            if i_rotate_connections:
                i_atr = i_rotate_connections[0][1]
                i_atr_dst = '.'.join(i_atr.split('.')[:-1]+['targetWeight'])
                # i_atr_src = qsm_mya_core.NodeAttribute.get_source_(i_atr_dst)
                list_.append(i_atr_dst)
        return list_

    def get_end_frame(self):
        return qsm_mya_core.NodeAttribute.get_value(
            self._location, 'end_frame'
        )

    def get_start_frame(self):
        return qsm_mya_core.NodeAttribute.get_value(
            self._location, 'start_frame'
        )

    def get_source_end_frame(self):
        return qsm_mya_core.NodeAttribute.get_value(
            self._location, 'source_end_frame'
        )

    def get_source_start_frame(self):
        return qsm_mya_core.NodeAttribute.get_value(
            self._location, 'source_start_frame'
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

    def find_root_start_constraint(self):
        _ = cmds.ls('{}:{}'.format(self._namespace, 'ROOT_START_PRC'), long=1)
        if _:
            return _[0]

    def find_root_end(self):
        _ = cmds.ls('{}:{}'.format(self._namespace, 'ROOT_END'), long=1)
        if _:
            return _[0]


class AdcChrMotionMasterLayer(AbsAdvMotionLayer):
    @classmethod
    @qsm_mya_core.Undo.execute
    def create_for(cls, namespace):
        is_create, location = AdvMotionLayerBase.create_as_master_layer(namespace)
        return cls(location)

    def __init__(self, *args, **kwargs):
        super(AdcChrMotionMasterLayer, self).__init__(*args, **kwargs)

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

    def append_layer(self, file_path, post_cycle=1, pre_blend_frame=2, post_blend_frame=2):
        if not bsc_storage.StgPath.get_is_file(file_path):
            raise OSError()

        resource_namespace = self.get_resource_namespace()

        layers_opt = AdvMotionLayersOpt(self.get_all_layers())
        end_frame = layers_opt.get_end_frame()
        pre_layer = layers_opt.get_end_layer()

        index = self.get_next_layer_index()
        file_opt = bsc_storage.StgFileOpt(file_path)
        name = file_opt.name_base
        layer_namespace = '{}_{}_{}'.format(resource_namespace, name, index)
        motion_layer = AdvChrMotionLayer.create_for(layer_namespace)
        self.fit_layer_scale(motion_layer)
        motion_layer.constraint_to_master(self)
        data = bsc_storage.StgFileOpt(file_path).set_read()

        qsm_mya_core.NodeAttribute.set_as_message(
            self._location, 'qsm_layers.layer_{}'.format(index), motion_layer.get_root()
        )
        motion_layer.apply_data_for(
            motion_layer,
            data,
            start_frame=end_frame, post_cycle=post_cycle,
            pre_blend_frame=pre_blend_frame, post_blend_frame=post_blend_frame
        )
        if pre_layer is not None:
            pre_root_end = pre_layer.find_root_end()
            root_start_constraint = motion_layer.find_root_start_constraint()
            qsm_mya_core.Connection.create(
                pre_root_end+'.translate', root_start_constraint+'.target[0].targetTranslate'
            )
            qsm_mya_core.Connection.create(
                pre_root_end+'.rotate', root_start_constraint+'.target[0].targetRotate'
            )

        return motion_layer

    def fit_layer_scale(self, layer):
        scale = cmds.getAttr(self._location+'.scaleX')
        layer.apply_root_scale(scale)

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

    def get_frame_range(self):
        layers_opt = AdvMotionLayersOpt(self.get_all_layers())
        return layers_opt.get_frame_range()


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
