# coding:utf-8
import collections
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

import lxbasic.core as bsc_core

import lxbasic.content as bsc_content

import lxbasic.model as bsc_model

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

import qsm_maya.adv as qsm_mya_adv

from ..base import util as _bsc_util

from ..base import sketch as _bsc_sketch

from ..base import graph as _bas_graph

from ..base import keyframe as _bsc_keyframe

from ..adv import resource as _adv_resource

from ..adv import control_set as _adv_control_set

from ..mocap import resource as _mcp_resource

from ..base import abc as _bsc_abc


class AbsMtgLayer(_bsc_abc.AbsMontage):

    @classmethod
    def update_root_start_by_self_fnc(cls, mtg_layer, start_frame, end_frame):
        # update self output end
        mtg_layer._node_opt.set('output_end', end_frame)
        # user self root start
        pre_root_opt = qsm_mya_core.EtrNodeOpt(mtg_layer.find_root_start_src())
        mtg_layer._node_opt.set(
            'root_start_input_from', mtg_layer._node_opt.get('key')
        )

        for i_key, i_atr_src in [
            ('root_start_input_tx', 'translateX'),
            ('root_start_input_ty', 'translateY'),
            ('root_start_input_tz', 'translateZ'),
            ('root_start_input_rx', 'rotateX'),
            ('root_start_input_ry', 'rotateY'),
            ('root_start_input_rz', 'rotateZ')
        ]:
            i_curve_path = mtg_layer.get_message_from(i_key+'_curve')
            if i_curve_path is None:
                continue

            i_curve_opt = qsm_mya_core.AnmCurveNodeOpt(i_curve_path)
            i_curve_opt.create_value_at_time(start_frame, pre_root_opt.get(i_atr_src))
            i_curve_opt.set_tangent_types_at_time(start_frame, 'auto', 'step')

    @classmethod
    def update_root_start_fnc(cls, mtg_layer, pre_mtg_layer, start_frame):
        # update pre layer output end
        pre_mtg_layer._node_opt.set('output_end', start_frame-1)
        # use pre root end
        pre_root_end_opt = qsm_mya_core.EtrNodeOpt(pre_mtg_layer.find_root_end())
        mtg_layer._node_opt.set(
            'root_start_input_from', pre_mtg_layer._node_opt.get('key')
        )

        for i_key, i_atr_src in [
            ('root_start_input_tx', 'translateX'),
            ('root_start_input_ty', 'translateY'),
            ('root_start_input_tz', 'translateZ'),
            ('root_start_input_rx', 'rotateX'),
            ('root_start_input_ry', 'rotateY'),
            ('root_start_input_rz', 'rotateZ')
        ]:
            i_curve_path = mtg_layer.get_message_from(i_key+'_curve')
            if i_curve_path is None:
                continue

            i_curve_opt = qsm_mya_core.AnmCurveNodeOpt(i_curve_path)
            i_curve_opt.create_value_at_time(start_frame, pre_root_end_opt.get(i_atr_src))
            i_curve_opt.set_tangent_types_at_time(start_frame, 'auto', 'step')

    @classmethod
    def find_one_master_layer_location(cls, rig_namespace):
        rig_namespace = rig_namespace or '*'
        _ = cmds.ls(_bsc_util.MtgRigNamespace.to_master_layer_name(rig_namespace), long=1)
        if _:
            return _[0]

    @classmethod
    def find_one_master_layer(cls, rig_namespace):
        _ = cls.find_one_master_layer_location(rig_namespace)
        if _:
            return MtgMasterLayer(_)

    def __init__(self, location):
        super(AbsMtgLayer, self).__init__()

        self._location = location

        self._namespace = qsm_mya_core.DagNode.extract_namespace(self._location)

        self._node_opt = qsm_mya_core.EtrNodeOpt(self._location)

        self._sketches = cmds.ls(self._location, type='joint', long=1, dag=1) or []

        self._cache_dict = {}
        self._cache_all()
        
    @property
    def location(self):
        return self._location

    def find_offset_location(self):
        _ = cmds.ls('{}:OFFSET'.format(self._namespace), long=1)
        if _:
            return _[0]

    def find_layer_offset_location(self):
        _ = cmds.ls('{}:LAYER_OFFSET'.format(self._namespace), long=1)
        if _:
            return _[0]

    def find_sketch_root_location(self):
        _ = cmds.ls('{}:ROOT'.format(self._namespace), long=1)
        if _:
            return _[0]

    def find_root_sketch(self):
        root_sketch_key = self._configure.get_sketch_key('Root_M')
        _ = cmds.ls('{}:{}'.format(self._namespace, root_sketch_key), long=1)
        if _:
            return _[0]

    def _cache_all(self):
        self._cache_dict.clear()

        for i_path in self._sketches:
            i_sketch_key = qsm_mya_core.DagNode.to_name_without_namespace(i_path)
            self._cache_dict[i_sketch_key] = i_path

    def get(self, sketch_key):
        return self._cache_dict.get(sketch_key)

    def get_sketch(self, sketch_key):
        return self._cache_dict.get(sketch_key)

    def get_all(self):
        return self._cache_dict.values()

    def reset(self):
        basic_sketch_keys = self._configure.basic_sketch_keys
        root_sketch_key = self._configure.root_sketch_key
        for i_sketch_key in basic_sketch_keys:
            i_sketch = self.get(i_sketch_key)
            if i_sketch_key == root_sketch_key:
                _bsc_sketch.Sketch(i_sketch).reset_translations()
            _bsc_sketch.Sketch(i_sketch).reset_rotations()

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


class MtgLayerBase(object):
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
    def create_master_layer(cls, layer_namespace):
        layer_name = _bsc_util.MtgLayerNamespace.to_master_later_name(layer_namespace)
        if qsm_mya_core.Node.is_exists(layer_name) is False:
            location = _bas_graph.MotionLayerGraph(
                layer_namespace, 'motion/motion_master_layer'
            ).create_all()
            # add layer attribute
            cmds.addAttr(
                location, longName='qsm_layers',
                numberOfChildren=250, attributeType='compound'
            )
            for i in range(250):
                cmds.addAttr(
                    location, longName='layer_{}'.format(i),
                    attributeType='message',
                    parent='qsm_layers'
                )

            root = MtgLayer.create_root()
            qsm_mya_core.Container.add_dag_nodes(root, [location])
            return True, layer_name
        return False, layer_name

    @classmethod
    def create_layer(cls, layer_namespace):
        layer_name = _bsc_util.MtgLayerNamespace.to_layer_name(layer_namespace)
        if qsm_mya_core.Node.is_exists(layer_name) is False:
            clip_location = _bas_graph.MotionTimeGraph(layer_namespace).create_all()
            location = _bas_graph.MotionLayerGraph(
                layer_namespace, 'motion/motion_layer'
            ).create_all()

            qsm_mya_core.Container.add_dag_nodes(
                location,
                [
                    clip_location,
                    # blend_location
                ]
            )

            root = MtgLayer.create_root()
            qsm_mya_core.Container.add_dag_nodes(root, [location])
            return True, layer_name
        return False, layer_name


class MtgLayer(AbsMtgLayer):
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
    def generate_fnc(cls, rig_namespace, key):
        layer_namespace = _bsc_util.MtgRigNamespace.to_layer_namespace(rig_namespace, key)
        is_create, layer_name = MtgLayerBase.create_layer(
            layer_namespace
        )
        if is_create is True:
            layer = cls(layer_name)
            # track key
            layer.set('key', key)
            cls.create_curves_for(layer)
            cmds.select(clear=1)
            return layer
        return cls(layer_name)

    @classmethod
    def create_curves_for(cls, mtg_layer):
        curve_nodes = []
        time_container = mtg_layer.get_time_container()
        basic_sketch_keys = mtg_layer._configure.basic_sketch_keys
        root_sketch_key = mtg_layer._configure.root_sketch_key
        for i_sketch_key in basic_sketch_keys:
            i_sketch = mtg_layer.get(i_sketch_key)
            if i_sketch is None:
                continue

            if i_sketch_key == root_sketch_key:
                i_atr_names = mtg_layer.AtrKeys.Root
            else:
                i_atr_names = mtg_layer.AtrKeys.Default

            for j_atr_name in i_atr_names:
                j_curve_node = _bsc_keyframe.SketchCurve.create(
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
        mtg_layer, data,
        start_frame=1,
        pre_cycle=0, post_cycle=1,
        pre_blend=4, post_blend=4, blend_type='flat',
        **kwargs
    ):
        location = mtg_layer.location
        sketch_data = data['sketches']

        frame_count = data['frame_count']
        root_height = data['root_height']

        master_lower_height = cls.DEFAULT_MASTER_LOWER_HEIGHT
        translation_scale = master_lower_height/root_height

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
        #
        for i_sketch_key, i_v in sketch_data.items():
            i_sketch_path = mtg_layer.get(i_sketch_key)
            i_orients = i_v['orients']
            i_time_samples = i_v['time_samples']
            cls.apply_orient_for(i_sketch_path, i_orients)
            cls.apply_time_samples_for_(i_sketch_path, i_time_samples, source_start, translation_scale)

        # connect main_weight to constraint
        weight_attributes = mtg_layer.get_constraint_weight_attributes()
        for i_weight_atr in weight_attributes:
            cmds.connectAttr(
                location+'.main_weight_output', i_weight_atr,
                force=1
            )
        return clip_start, clip_end

    def __init__(self, *args, **kwargs):
        super(MtgLayer, self).__init__(*args, **kwargs)

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
            i_curve_node_name = _bsc_keyframe.SketchCurve.to_curve_node_name(sketch_path, i_atr_name)
            if qsm_mya_core.Node.is_exists(i_curve_node_name) is False:
                continue

            _bsc_keyframe.SketchCurve.appy_data(
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
            i_curve_name = _bsc_keyframe.ControlCurve.create(character, i_key, i_atr_name, i_v, start_frame, translation_scale)
            curve_map[i_key] = i_curve_name
        return curve_map

    def connect_to_master_layer(self, master_motion_layer):
        if isinstance(master_motion_layer, AbsMtgLayer) is True:
            basic_sketch_keys = self._configure.basic_sketch_keys
            root_sketch_key = self._configure.root_sketch_key
            for i_sketch_key in basic_sketch_keys:
                i_sketch_src = self.get(i_sketch_key)

                i_sketch_dst = master_motion_layer.get(i_sketch_key)
                if i_sketch_key == root_sketch_key:
                    _bsc_sketch.Sketch(i_sketch_src).create_point_constraint_to_master(
                        i_sketch_dst,
                        break_parent_inverse=True
                    )
                    _bsc_sketch.Sketch(i_sketch_src).create_orient_constraint_to_master(
                        i_sketch_dst,
                        break_parent_inverse=True,
                        interp_type=1
                    )
                else:
                    _bsc_sketch.Sketch(i_sketch_src).create_orient_constraint_to_master(
                        i_sketch_dst,
                        # do not break parent inverse
                        # break_parent_inverse=True,
                        interp_type=1
                    )

    def get_constraint_weight_attributes(self):
        list_ = []
        basic_sketch_keys = self._configure.basic_sketch_keys
        root_sketch_key = self._configure.root_sketch_key
        for i_sketch_key in basic_sketch_keys:
            i_sketch_src = self.get(i_sketch_key)
            if i_sketch_key == root_sketch_key:
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

    def find_root_end(self):
        _ = cmds.ls('{}:{}'.format(self._namespace, 'ROOT_END'), long=1)
        if _:
            return _[0]

    def set_layer_index(self, layer_index):
        qsm_mya_core.NodeAttribute.set_value(
            self._location, 'layer_index', layer_index
        )

    def set_rgb(self, rgb):
        qsm_mya_core.NodeAttribute.set_as_tuple(
            self._location, 'rgb', rgb
        )

    def update_main_weight(
        self,
        frame_range,
        is_start=False, is_end=False,
        pre_blend=4, post_blend=4, blend_type='flat',
        **kwargs
    ):
        curve_opt = self.get_main_weight_curve_opt()

        end_offset = 0

        min_weight, max_weight = 0.0, 0.5

        start_frame, end_frame = frame_range

        condition = [is_start, is_end]
        if condition == [True, True]:
            # start
            curve_opt.create_value_at_time(start_frame, max_weight)
            # end
            curve_opt.create_value_at_time(end_frame+end_offset, max_weight)
        elif condition == [True, False]:
            # start
            curve_opt.create_value_at_time(start_frame, max_weight)
            # end
            curve_opt.create_value_at_time(end_frame+end_offset, max_weight)
            curve_opt.create_value_at_time(end_frame+post_blend+end_offset, min_weight)
        elif condition == [False, True]:
            # start
            curve_opt.create_value_at_time(start_frame-pre_blend, min_weight)
            curve_opt.create_value_at_time(start_frame, max_weight)
            # end
            curve_opt.create_value_at_time(end_frame+end_offset, max_weight)
        else:
            if start_frame == end_frame:
                # start
                curve_opt.create_value_at_time(start_frame-pre_blend, min_weight)
                curve_opt.create_value_at_time(start_frame, max_weight)
                # end
                curve_opt.create_value_at_time(end_frame+post_blend, min_weight)
            else:
                # start
                curve_opt.create_value_at_time(start_frame-pre_blend, min_weight)
                curve_opt.create_value_at_time(start_frame, max_weight)
                # end
                curve_opt.create_value_at_time(end_frame+end_offset, max_weight)
                curve_opt.create_value_at_time(end_frame+post_blend+end_offset, min_weight)

    def update_main_weight_auto(self, is_start, is_end):
        clip_start, clip_end = self._node_opt.get('clip_start'), self._node_opt.get('clip_end')
        pre_blend, post_blend = self._node_opt.get('pre_blend'), self._node_opt.get('post_blend')
        self.update_main_weight((clip_start, clip_end), is_start, is_end, pre_blend, post_blend)

    def restore_main_weight_curve(self):
        curve_opt = self.get_main_weight_curve_opt()
        if curve_opt is not None:
            curve_opt.delete()

        curve_opt = qsm_mya_core.AnmCurveNodeOpt.create(self._location, 'main_weight', True)
        qsm_mya_core.NodeAttribute.set_as_message(
            self._location, 'main_weight_curve', curve_opt.path
        )

    def generate_root_start_input_transformation_curves_kwargs(self):
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
        curve_kwargs = self.generate_root_start_input_transformation_curves_kwargs()
        for i_key, (i_curve_opt, i_atr_src) in curve_kwargs.items():
            if i_curve_opt is not None:
                i_curve_opt.delete()

            i_curve_typ = _bsc_keyframe.ControlCurve.CURVE_TYPE_MAP[i_atr_src]
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

    def generate_track_kwargs(self):
        kwargs = {}
        for j_key in bsc_model.TrackModel.MAIN_KEYS:
            kwargs[j_key] = self._node_opt.get(j_key)
        # for j_key in bsc_model.TrackModel.SUB_KEYS:
        #     kwargs[j_key] = self._node_opt.get(j_key)
        return kwargs


class MtgMasterLayer(AbsMtgLayer):
    @classmethod
    @qsm_mya_core.Undo.execute
    def generate_fnc(cls, rig_namespace):
        master_layer_namespace = _bsc_util.MtgRigNamespace.to_master_layer_namespace(rig_namespace)
        is_create, layer_name = MtgLayerBase.create_master_layer(master_layer_namespace)
        if is_create is True:
            mtg_master_layer = cls(layer_name)
            mtg_master_layer.look_from_persp_cam()
            cmds.select(clear=1)
            return mtg_master_layer
        return cls(layer_name)

    def __init__(self, *args, **kwargs):
        super(MtgMasterLayer, self).__init__(*args, **kwargs)
        
    def do_delete(self):
        layers = self.get_all_layer_locations()
        
        qsm_mya_core.Node.delete(self._location)
        
        for i in layers:
            qsm_mya_core.Node.delete(i)

    def restore(self):
        layers = self.get_all_layer_locations()
        for i in layers:
            qsm_mya_core.Node.delete(i)

    def do_bake(self):
        rig_namespace = self.get_rig_namespace()

        control_key_query = self._configure.control_key_query
        if qsm_mya_adv.AdvOpt.check_is_valid(rig_namespace) is True:
            start_frame, end_frame = self.get_frame_range()
            adv_resource = _adv_resource.AdvResource(rig_namespace)
            main_control_keys = control_key_query.values()

            main_controls = [adv_resource._control_set.get(x) for x in main_control_keys]
            main_controls = list(filter(None, main_controls))

            # fixme: face control is ignore?
            main_control_set = _adv_control_set.AdvControlSet(main_controls)
            main_control_set.bake_all_keyframes(
                start_frame, end_frame,
                attributes=[
                    'translateX', 'translateY', 'translateZ',
                    'rotateX', 'rotateY', 'rotateZ',
                ]
            )

            self.do_delete()
        elif _mcp_resource.MocapResource.check_is_valid(rig_namespace) is True:
            start_frame, end_frame = self.get_frame_range()

            mocap_resource = _mcp_resource.MocapResource(namespace=rig_namespace)

            mocap_resource.sketch_set.bake_all_keyframes(
                start_frame, end_frame,
                attributes=[
                    'translateX', 'translateY', 'translateZ',
                    'rotateX', 'rotateY', 'rotateZ',
                ]
            )
            self.do_delete()
        else:
            pass

    def find_root_loc(self):
        _ = cmds.ls('{}:{}'.format(self._namespace, 'root_loc'), long=1)
        if _:
            return _[0]

    def generate_root_loc_curves_kwargs(self):
        dict_ = {}
        root_loc = self.find_root_loc()
        if root_loc:
            for i_key, i_atr_src in [
                ('root_loc_tx', 'translateX'),
                ('root_loc_ty', 'translateY'),
                ('root_loc_tz', 'translateZ'),
                ('root_loc_rx', 'rotateX'),
                ('root_loc_ry', 'rotateY'),
                ('root_loc_rz', 'rotateZ'),
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

    def restore_root_loc_curves(self):
        root_loc = self.find_root_loc()
        if root_loc:
            curve_kwargs = self.generate_root_loc_curves_kwargs()
            for i_key, (i_curve_opt, i_atr_src) in curve_kwargs.items():
                if i_curve_opt is not None:
                    i_curve_opt.delete()

                i_curve_typ = _bsc_keyframe.ControlCurve.CURVE_TYPE_MAP[i_atr_src]
                i_curve_opt = qsm_mya_core.AnmCurveNodeOpt.create(
                    root_loc, i_atr_src, keep_namespace=True, curve_type=i_curve_typ
                )

                qsm_mya_core.NodeAttribute.set_as_message(
                    self._location, i_key+'_curve', i_curve_opt.path
                )

    def find_persp_cam(self):
        _ = cmds.ls('{}:{}'.format(self._namespace, 'persp_camShape'), long=1)
        if _:
            return _[0]

    def look_from_persp_cam(self):
        persp_cam = self.find_persp_cam()
        if persp_cam:
            qsm_mya_core.Camera.over_persp_look(persp_cam)

    def export_motion_to(self, file_path):
        control_key_query = self._configure.control_key_query
        rig_namespace = self.get_rig_namespace()
        start_frame, end_frame = self.get_frame_range()
        adv_resource = _adv_resource.AdvResource(rig_namespace)
        main_control_keys = control_key_query.values()
        main_controls = [adv_resource._control_set.get(x) for x in main_control_keys]
        main_controls = list(filter(None, main_controls))

        # fixme: face control is ignore?
        main_control_set = _adv_control_set.AdvControlSet(main_controls)
        main_control_set.bake_all_keyframes(
            start_frame, end_frame,
            attributes=[
                'translateX', 'translateY', 'translateZ',
                'rotateX', 'rotateY', 'rotateZ',
            ]
        )
        adv_resource._control_set.export_motion_to(file_path)
        cmds.undo()

    def connect_to_adv_resource(self, adv_resource):
        qsm_mya_core.NodeAttribute.set_as_message(
            self._location, 'qsm_resource', adv_resource.find_root_location()
        )
        adv_resource.connect_from_master_layer(self)

    def connect_to_mocap(self, mocap_resource):
        qsm_mya_core.NodeAttribute.set_as_message(
            self._location, 'qsm_resource', mocap_resource.find_root_location()
        )
        mocap_resource.connect_from_master_layer(self)

    def get_next_layer_index(self):
        for i in range(250):
            if not cmds.listConnections(
                '{}.qsm_layers.layer_{}'.format(
                    self._location, i
                ), destination=0, source=1
            ):
                return i
        return 0

    def get_rig_namespace(self):
        resource_root = qsm_mya_core.NodeAttribute.get_as_message(
            self._location, 'qsm_resource'
        )
        if resource_root:
            return qsm_mya_core.DagNode.extract_namespace(resource_root)
        return 'test'

    @qsm_mya_core.Undo.execute
    def append_layer(
        self,
        motion_json,
        pre_cycle=1, post_cycle=1,
        pre_blend=4, post_blend=4, blend_type='flat',
        **kwargs
    ):
        if not bsc_storage.StgPath.get_is_file(motion_json):
            raise OSError()

        rig_namespace = self.get_rig_namespace()

        layers_opt = MtgLayersOpt(self.get_all_layer_locations())

        stage_end_frame = layers_opt.get_end_frame()
        pre_mtg_layer = layers_opt.get_end_layer()

        layer_index = self.get_next_layer_index()

        file_opt = bsc_storage.StgFileOpt(motion_json)
        dcc_name = bsc_core.BscText.clear_up_to(file_opt.name_base)
        key = '{}_{}'.format(dcc_name, layer_index)
        mtg_layer = MtgLayer.generate_fnc(rig_namespace, key)

        self.fit_layer_scale(mtg_layer)
        mtg_layer.connect_to_master_layer(self)
        data = bsc_storage.StgFileOpt(motion_json).set_read()

        qsm_mya_core.NodeAttribute.set_as_message(
            self._location, 'qsm_layers.layer_{}'.format(layer_index), mtg_layer.location
        )
        mtg_layer.set_layer_index(layer_index)
        rgb = bsc_core.BscTextOpt(key).to_hash_rgb(maximum=1.0, s_p=(15, 35), v_p=(75, 95))
        mtg_layer.set_rgb(rgb)
        qsm_mya_core.NodeAttribute.set_as_string(
            mtg_layer.location, 'motion_json', motion_json
        )
        clip_start, clip_end = mtg_layer.apply_data_for(
            mtg_layer,
            data,
            start_frame=stage_end_frame+1,
            pre_cycle=pre_cycle, post_cycle=post_cycle,
            pre_blend=pre_blend, post_blend=post_blend, blend_type='flat',
            **kwargs
        )
        # create main weight curve for self
        mtg_layer.restore_main_weight_curve()
        mtg_layer.restore_root_start_input_transformation_curves()

        is_start = pre_mtg_layer is None
        if is_start:
            mtg_layer.update_main_weight(
                (clip_start, clip_end),
                is_start=True, is_end=True,
                pre_blend=pre_blend, post_blend=post_blend, blend_type='flat'
            )
            self.update_root_start_by_self_fnc(mtg_layer, clip_start, clip_end)

            self.restore_root_loc_curves()
            # todo: do not execute here
        else:
            mtg_layer.update_main_weight(
                (clip_start, clip_end),
                is_start=False, is_end=True,
                pre_blend=pre_blend, post_blend=post_blend, blend_type='flat'
            )
            self.update_root_start_fnc(mtg_layer, pre_mtg_layer, clip_start)
            pre_mtg_layer.update_main_weight_auto(is_start=False, is_end=False)

        # update for follow camera
        self.update_root_loc_for(mtg_layer, is_start, clip_start, clip_end)

        return mtg_layer

    def create_layer(self, motion_json, **kwargs):
        if not bsc_storage.StgPath.get_is_file(motion_json):
            raise OSError()

        layer_index = self.get_next_layer_index()

        rig_namespace = self.get_rig_namespace()

        key = kwargs['key']
        mtg_layer = MtgLayer.generate_fnc(rig_namespace, key)

        self.fit_layer_scale(mtg_layer)
        mtg_layer.connect_to_master_layer(self)
        data = bsc_storage.StgFileOpt(motion_json).set_read()

        qsm_mya_core.NodeAttribute.set_as_message(
            self._location, 'qsm_layers.layer_{}'.format(layer_index), mtg_layer.location
        )
        mtg_layer.set_layer_index(layer_index)
        qsm_mya_core.NodeAttribute.set_as_string(
            mtg_layer.location, 'motion_json', motion_json
        )
        mtg_layer.apply_data_for(
            mtg_layer,
            data,
        )

    def update_root_loc_for(self, mtg_layer, is_start, start_frame, end_frame):
        root_start = mtg_layer.find_root_start()
        root_end = mtg_layer.find_root_end()

        curve_names = []
        root_loc_curves_kwargs = self.generate_root_loc_curves_kwargs()
        for i_key, (i_curve_opt, i_atr_src) in root_loc_curves_kwargs.items():
            if i_curve_opt is None:
                continue

            curve_names.append(i_curve_opt.path)
            # first layer, update start
            if is_start is True:
                i_value_start = cmds.getAttr(root_start+'.'+i_atr_src)
                # todo: do not offset Y?
                if i_atr_src == 'translateY':
                    i_value_start = 0

                i_curve_opt.create_value_at_time(start_frame, i_value_start)
                i_curve_opt.set_tangent_types_at_time(start_frame, 'clamped', 'clamped')

            i_value_end = cmds.getAttr(root_end+'.'+i_atr_src)
            if i_atr_src == 'translateY':
                i_value_end = 0

            i_curve_opt.create_value_at_time(end_frame, i_value_end)
            i_curve_opt.set_tangent_types_at_time(start_frame, 'clamped', 'clamped')

        # filter root track curve later
        if curve_names:
            qsm_mya_core.AnmCurveNodes.euler_filter(curve_names)

    def update_root_loc_end_for(self, mtg_layer, start_frame, end_frame):
        root_end = mtg_layer.find_root_end()

        curve_names = []
        root_loc_curves_kwargs = self.generate_root_loc_curves_kwargs()
        for i_key, (i_curve_opt, i_atr_src) in root_loc_curves_kwargs.items():
            if i_curve_opt is None:
                continue

            curve_names.append(i_curve_opt.path)

            i_value_end = cmds.getAttr(root_end+'.'+i_atr_src)
            if i_atr_src == 'translateY':
                i_value_end = 0

            i_curve_opt.create_value_at_time(end_frame, i_value_end)
            i_curve_opt.set_tangent_types_at_time(start_frame, 'clamped', 'clamped')

        # filter root track curve later
        if curve_names:
            qsm_mya_core.AnmCurveNodes.euler_filter(curve_names)

    def fit_layer_scale(self, mtg_layer):
        scale = cmds.getAttr(self._location+'.scaleX')
        mtg_layer.apply_root_scale(scale)

    def get_all_layer_locations(self):
        list_ = []
        for i in range(250):
            _ = cmds.listConnections(
                '{}.qsm_layers.layer_{}'.format(
                    self._location, i
                ), destination=0, source=1
            )
            if _:
                list_.append(_[0].split('.')[0])
        return list_

    def get_all_layer_names(self):
        return [':'.join(x.split(':')[:-1]) for x in self.get_all_layer_locations()]

    def get_frame_range(self):
        layers_opt = MtgLayersOpt(self.get_all_layer_locations())
        return layers_opt.get_frame_range()


class MtgLayersOpt(object):
    def __init__(self, locations):
        self._layers = [MtgLayer(x) for x in locations]

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


class MtgRoot(_bsc_abc.AbsMontage):
    @classmethod
    def set_current_rig_namespace(cls, rig_namespace):
        root = cls.create_root()
        qsm_mya_core.NodeAttribute.create_as_string(
            root, 'rig_namespace', rig_namespace
        )

    @classmethod
    def get_current_rig_namespace(cls):
        root = cls.create_root()
        if qsm_mya_core.NodeAttribute.is_exists(root, 'rig_namespace'):
            return qsm_mya_core.NodeAttribute.get_as_string(
                root, 'rig_namespace'
            )
