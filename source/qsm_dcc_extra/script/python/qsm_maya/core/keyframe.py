# coding:utf-8
import copy

# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import attribute as _attribute

from . import reference as _reference

from . import connection as _connection


class AnimCurves(object):
    @classmethod
    def get_all_from_selection(cls):
        nodes = cmds.ls(sl=True) or []
        history_nodes = cmds.listHistory(nodes, pruneDagObjects=True, leaf=False) or []
        return cmds.ls(history_nodes, type='animCurve') or []

    @classmethod
    def get_range(cls, paths):
        if paths:
            return int(cmds.findKeyframe(paths, which='first')), int(cmds.findKeyframe(paths, which='last'))
        return 0, 0


class Control(object):
    @classmethod
    def find_anim_curves(cls, path):
        history_nodes = cmds.listHistory(path, pruneDagObjects=True, leaf=False) or []
        return cmds.ls(history_nodes, type='animCurve') or []


class NodePortAnmCurveOpt(object):
    DATA_KEYS = [
        'inAngle', 'outAngle',
        'inWeight', 'outWeight',
        'inTangentType', 'outTangentType',
    ]

    def __init__(self, path, atr_name):
        self._path = path
        self._atr_name = atr_name

    def find_node(self):
        _ = cmds.findKeyframe(
            self._path, curve=True, at=self._atr_name
        )
        if _:
            return _[0]

    def get_index_count(self):
        return cmds.keyframe(
            self._path,
            attribute=self._atr_name,
            query=True,
            keyframeCount=True
        ) or 0

    def get_time_at(self, index):
        _ = cmds.keyframe(
            self._path,
            query=1,
            attribute=self._atr_name,
            index=(index, index),
            timeChange=1
        )
        if _:
            return _[0]

    def set_value_at_frame(self, frame, value):
        cmds.setKeyframe(
            self._path,
            attribute=self._atr_name,
            time=(frame, frame),
            value=value
        )

    def get_value_at(self, index):
        _ = cmds.keyframe(
            self._path,
            query=1,
            attribute=self._atr_name,
            index=(index, index),
            valueChange=1
        )
        if _:
            return _[0]

    def get_tangents_at(self, index):
        list_ = []
        for i_key in self.DATA_KEYS:
            i_kwargs = dict(
                query=1,
                attribute=self._atr_name,
                index=(index, index),
            )
            i_kwargs[i_key] = 1
            _ = cmds.keyTangent(
                self._path, **i_kwargs
            )
            if _:
                list_.append(_[0])
            else:
                list_.append(None)
        return list_

    def set_tangents_at(self, frame, tangents):
        # fixme: set TangentType first? or weight first?
        tangents = copy.copy(tangents)
        tangents.reverse()
        keys = copy.copy(self.DATA_KEYS)
        keys.reverse()
        for i_seq, i_key in enumerate(keys):
            i_value = tangents[i_seq]

            i_kwargs = dict(
                attribute=self._atr_name,
                time=(frame, frame)
            )
            i_kwargs[i_key] = i_value
            cmds.keyTangent(
                self._path, **i_kwargs
            )

    def get_points(self):
        index_count = self.get_index_count()
        list_ = []
        for i_index in range(index_count):
            i_time = self.get_time_at(i_index)
            i_value = self.get_value_at(i_index)
            i_tangent = self.get_tangents_at(i_index)
            list_.append((i_time, i_value, i_tangent))
        return list_

    def set_points(self, points, frame_offset=0, value_factor=1):
        for i in points:
            i_time, i_value, i_tangents = i
            # fixme: time is None?
            if i_time is None:
                continue
            self.set_value_at_frame(i_time+frame_offset, i_value*value_factor)
            self.set_tangents_at(i_time+frame_offset, i_tangents)

        if points:
            # fix tangent bug
            first_points = points[0]
            f_time, f_value, f_tangents = first_points
            # fixme: time is None?
            if f_time is None:
                return
            self.set_value_at_frame(f_time+frame_offset, f_value*value_factor)
            self.set_tangents_at(f_time+frame_offset, f_tangents)

    def offset_all_values(self, offset_value):
        index_count = self.get_index_count()
        for i_index in range(index_count):
            i_time = self.get_time_at(i_index)
            i_value = self.get_value_at(i_index)
            i_value_new = i_value+offset_value
            self.set_value_at_frame(i_time, i_value_new)


class NodeKeyframe(object):

    @classmethod
    def apply_value(cls, path, data, force=False, mirror_keys=None):
        atr_name, value = data
        if _attribute.NodeAttribute.is_exists(path, atr_name) is False:
            return
        # try to unlock
        if _attribute.NodeAttribute.is_lock(path, atr_name) is True:
            # when node is from reference, ignore
            if _reference.Reference.is_from_reference(path) is True:
                return

            if force is True:
                _attribute.NodeAttribute.unlock(path, atr_name)
            else:
                return
        # try to break source
        if _attribute.NodeAttribute.has_source(path, atr_name) is True:
            if force is True:
                result = _attribute.NodeAttribute.break_source(path, atr_name)
                if result is False:
                    return
            else:
                return

        value_dst = _attribute.NodeAttribute.get_value(path, atr_name)
        if value != value_dst:
            _attribute.NodeAttribute.set_value(path, atr_name, value)

    @classmethod
    def apply_curve(cls, path, data, frame_offset=0, force=False, mirror_keys=None):
        atr_name, curve_type, infinities, curve_points = data
        if _attribute.NodeAttribute.is_exists(path, atr_name) is False:
            return

        if _attribute.NodeAttribute.is_lock(path, atr_name) is True:
            # when node is from reference, ignore
            if _reference.Reference.is_from_reference(path) is True:
                return
            if force is True:
                _attribute.NodeAttribute.unlock(path, atr_name)
            else:
                return

        if _attribute.NodeAttribute.has_source(path, atr_name) is True:
            if force is True:
                _attribute.NodeAttribute.break_source(path, atr_name)
            else:
                return

        curve_name = '{}_{}'.format(
            path.split('|')[-1].split(':')[-1],
            atr_name.replace('.', '_')
        )
        curve_name_new = cmds.createNode(curve_type, name=curve_name, skipSelect=1)

        i_atr_path_src = '{}.output'.format(curve_name_new)
        i_atr_path_dst = '{}.{}'.format(path, atr_name)
        _connection.Connection.create(i_atr_path_src, i_atr_path_dst)

        NodePortAnmCurveOpt(path, atr_name).set_points(curve_points, frame_offset=frame_offset)

        _attribute.NodeAttribute.set_value(
            curve_name_new, 'preInfinity', infinities[0]
        )
        _attribute.NodeAttribute.set_value(
            curve_name_new, 'postInfinity', infinities[1]
        )


class AnmCurve(object):
    NODE_TYPES = [
        'animCurveTL', 'animCurveTA', 'animCurveTT', 'animCurveTU',
        'animCurveUL', 'animCurveUA', 'animCurveUT', 'animCurveUU'
    ]

    @classmethod
    def offset_frame(cls, curve_name, offset):
        times = cmds.keyframe(curve_name, query=True, timeChange=True)
        for i_time in times:
            i_time_new = i_time+offset
            cmds.cutKey(curve_name, time=(i_time,))
            cmds.pasteKey(curve_name, time=(i_time_new,))

    @classmethod
    def check_is_valid(cls, any_node):
        return cmds.nodeType(any_node).startswith('animCurve')


class AnmCurveOpt(object):
    DATA_KEYS = [
        'inAngle', 'outAngle',
        'inWeight', 'outWeight',
        'inTangentType', 'outTangentType',
    ]

    @classmethod
    def create(cls, path, atr_name):
        curve_name = '{}_{}'.format(
            path.split('|')[-1].split(':')[-1],
            atr_name.replace('.', '_')
        )
        curve_type = 'animCurveTL'
        curve_name_new = cmds.createNode(curve_type, name=curve_name, skipSelect=1)

        atr_path_src = '{}.output'.format(curve_name_new)
        atr_path_dst = '{}.{}'.format(path, atr_name)
        _connection.Connection.create(atr_path_src, atr_path_dst)

        return cls(curve_name_new)

    def __init__(self, curve_name):
        self._curve_name = curve_name

    def get_index_count(self):
        return cmds.keyframe(
            self._curve_name,
            query=True,
            keyframeCount=True
        ) or 0

    def get_time_at(self, index):
        _ = cmds.keyframe(
            self._curve_name,
            query=1,
            index=(index, index),
            timeChange=1
        )
        if _:
            return _[0]

    def set_value_at_frame(self, frame, value):
        cmds.setKeyframe(
            self._curve_name,
            time=(frame, frame),
            value=value
        )

    def get_value_at(self, index):
        _ = cmds.keyframe(
            self._curve_name,
            query=1,
            index=(index, index),
            valueChange=1
        )
        if _:
            return _[0]

    def get_tangents_at(self, index):
        list_ = []
        for i_key in self.DATA_KEYS:
            i_kwargs = dict(
                query=1,
                index=(index, index),
            )
            i_kwargs[i_key] = 1
            _ = cmds.keyTangent(
                self._curve_name, **i_kwargs
            )
            if _:
                list_.append(_[0])
            else:
                list_.append(None)
        return list_

    def set_tangents_at(self, frame, tangents):
        for i_seq, i_key in enumerate(self.DATA_KEYS):
            i_value = tangents[i_seq]

            i_kwargs = dict(
                time=(frame, frame)
            )
            i_kwargs[i_key] = i_value
            cmds.keyTangent(
                self._curve_name, **i_kwargs
            )

    def get_points(self):
        index_count = self.get_index_count()
        list_ = []
        for i_index in range(index_count):
            i_time = self.get_time_at(i_index)
            i_value = self.get_value_at(i_index)
            i_tangent = self.get_tangents_at(i_index)
            list_.append((i_time, i_value, i_tangent))
        return list_

    def get_infinities(self):
        return (
            _attribute.NodeAttribute.get_value(self._curve_name, 'preInfinity'),
            _attribute.NodeAttribute.get_value(self._curve_name, 'postInfinity')
        )

    def set_points(self, points, frame_offset=0, value_factor=1):
        for i in points:
            i_time, i_value, i_tangents = i
            # fixme: time is None?
            if i_time is None:
                continue
            self.set_value_at_frame(i_time+frame_offset, i_value*value_factor)
            self.set_tangents_at(i_time+frame_offset, i_tangents)

        if points:
            # fix tangent bug
            first_points = points[0]
            f_time, f_value, f_tangents = first_points
            # fixme: time is None?
            if f_time is None:
                return
            self.set_value_at_frame(f_time+frame_offset, f_value*value_factor)
            self.set_tangents_at(f_time+frame_offset, f_tangents)


class NodePortAnmLayerOpt(object):
    ANM_LAYER_KEYS = [
        'mute',
        'solo',
        'lock',
        'override',
        'passthrough',
        'rotationAccumulationMode',
        'scaleAccumulationMode',
        #
        'childsoloed',
        'outMute',
        'preferred',
        'collapse'
    ]

    @classmethod
    def _next_layer_fnc(cls, anm_blend, atr_name):
        _ = cmds.listConnections(
            _attribute.NodeAttribute.to_atr_path(anm_blend, atr_name),
            destination=0, source=1, type='animLayer', skipConversionNodes=1
        ) or []
        if _:
            return _[0]
        return None

    @classmethod
    def _next_curve_fnc(cls, curve_args, anm_blend, atr_name):
        _ = cmds.listConnections(
            _attribute.NodeAttribute.to_atr_path(anm_blend, atr_name),
            destination=0, source=1, type='animCurve', skipConversionNodes=1
        ) or []
        if _:
            curve_name = _[0]
            curve_args.append(
                (curve_name, cls._next_layer_fnc(anm_blend, 'weightB'))
            )

    @classmethod
    def _next_blend_fnc(cls, curve_args, anm_blend, atr_name):
        _ = cmds.listConnections(
            _attribute.NodeAttribute.to_atr_path(anm_blend, atr_name),
            destination=0, source=1, skipConversionNodes=1
        ) or []
        if _:
            node = _[0]
            node_type = cmds.nodeType(node)
            if node_type.startswith('animBlendNode'):
                anm_blend = node
                cls._next_curve_fnc(curve_args, anm_blend, 'inputB')
                cls._next_blend_fnc(curve_args, anm_blend, 'inputA')

    def __init__(self, path, atr_name):
        self._path = path
        self._atr_name = atr_name
        self._atr_path = _attribute.NodeAttribute.to_atr_path(self._path, self._atr_name)

    def generate_curve_args(self):
        curve_args = []
        _ = cmds.listConnections(self._atr_path, destination=0, source=1, skipConversionNodes=1) or []
        if _:
            node = _[0]
            node_type = cmds.nodeType(node)
            if node_type.startswith('animBlendNode'):
                anm_blend = node
                self._next_curve_fnc(curve_args, anm_blend, 'inputB')
                self._next_blend_fnc(curve_args, anm_blend, 'inputA')
            elif node_type.startswith('animCurve'):
                curve_args.append((node, None))
        return curve_args

    def get_data(self):
        layer_data = {}
        for i_anm_curve, i_anm_layer in self.generate_curve_args():
            i_anm_curve_opt = AnmCurveOpt(i_anm_curve)
            # if i_anm_layer is not None:
            #     i_anm_data = []
            #     for j in self.ANM_LAYER_KEYS:
            #         # noinspection PyUnresolvedReferences
            #         i_anm_data.append(
            #             cmds.getAttr(i_anm_layer+'.'+j)
            #         )
            #     layer_data[i_anm_layer] = i_anm_data

        return layer_data


class NodeAnmCurvesOpt(object):
    def __init__(self, path):
        self._path = path

    def get_data(self):
        atr_names = _attribute.NodeAttributes.get_all_keyable_names(self._path)
        for i_atr_name in atr_names:
            print i_atr_name
