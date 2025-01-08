# coding:utf-8
from contextlib import contextmanager
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import attribute as _attribute

from . import connection as _connection

from . import node_for_dag as _node_for_dag


@contextmanager
def auto_keyframe_context(auto_keyframe=False):
    auto_key_mark = cmds.autoKeyframe(state=1, query=1)
    if auto_key_mark:
        cmds.autoKeyframe(state=False)

    if auto_keyframe is True:
        cmds.autoKeyframe(state=True)

    yield

    if auto_keyframe is True:
        cmds.autoKeyframe(state=False)

    if auto_key_mark:
        cmds.autoKeyframe(state=True)


class AnimCurveNodes(object):
    @classmethod
    def get_all_from_selection(cls):
        nodes = cmds.ls(sl=True) or []
        history_nodes = cmds.listHistory(nodes, pruneDagObjects=True, leaf=False) or []
        return cmds.ls(history_nodes, type='animCurve') or []

    @classmethod
    def get_range(cls, curve_names):
        if curve_names:
            return int(cmds.findKeyframe(curve_names, which='first')), int(cmds.findKeyframe(curve_names, which='last'))
        return 0, 0

    @classmethod
    def get_all(cls, reference=False, excludes=None):
        _ = cmds.ls(type='animCurve') or []
        if reference is True:
            curve_names = _
        else:
            curve_names = [x for x in _ if not cmds.referenceQuery(x, isNodeReferenced=1)]

        if isinstance(excludes, (tuple, list)):
            for i in excludes:
                if i in curve_names:
                    curve_names.remove(i)
        return curve_names

    @classmethod
    def get_all_from(cls, controls):
        history_nodes = cmds.listHistory(controls, pruneDagObjects=True, leaf=False) or []
        return cmds.ls(history_nodes, type='animCurve') or []

    @classmethod
    def scale_by_pivot(cls, curve_names, scale, scale_pivot):
        """
        scaleKey -iub false -t "33:66" -ts 2.030302 -tp 33 -fs 2.030302 -fp 33 -vs 1 -vp 0 -an objects Main_translateX
        """
        cmds.scaleKey(
            *curve_names, timeScale=scale, timePivot=scale_pivot
        )

    @classmethod
    def wrap_to_range(cls, curve_names, frame_range):
        pass

    @classmethod
    def offset(cls, curve_names, offset):
        """
        keyframe -e -iub false -an objects -t "1:121" -r -o over -tc 14 -fc 0.583333 pCube1_visibility
        """
        cmds.keyframe(
            *curve_names, animation='objects', relative=1, option='over', timeChange=offset
        )

    @classmethod
    def euler_filter(cls, curve_names):
        cmds.filterCurve(*curve_names)


class AnmCurveNode(object):
    NODE_TYPES = [
        'animCurveTL', 'animCurveTA', 'animCurveTT', 'animCurveTU',
        'animCurveUL', 'animCurveUA', 'animCurveUT', 'animCurveUU'
    ]

    @classmethod
    def create(cls, name, type_name):
        if cmds.objExists(name) is True:
            return name
        return cmds.createNode(
            type_name, name=name, skipSelect=1
        )

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

    @classmethod
    def clear_keyframes(cls, curve_name):
        if cmds.objExists(curve_name):
            key_times = cmds.keyframe(curve_name, query=True, timeChange=True)
            if key_times:
                cmds.cutKey(curve_name, time=(min(key_times), max(key_times)))


class AnmCurveNodeOpt(object):
    DATA_KEYS = [
        'inAngle', 'outAngle',
        'inWeight', 'outWeight',
        'inTangentType', 'outTangentType',
    ]

    @classmethod
    def create(cls, path, atr_name, keep_namespace=False, curve_type=None):
        if keep_namespace is True:
            curve_name = '{}_{}'.format(
                path.split('|')[-1],
                atr_name.replace('.', '_')
            )
        else:
            curve_name = '{}_{}'.format(
                path.split('|')[-1].split(':')[-1],
                atr_name.replace('.', '_')
            )

        curve_type = curve_type or 'animCurveTL'
        curve_name_ = cmds.createNode(curve_type, name=curve_name, skipSelect=1)

        atr_path_src = '{}.output'.format(curve_name_)
        atr_path_tgt = '{}.{}'.format(path, atr_name)
        _connection.Connection.create(atr_path_src, atr_path_tgt)

        return cls(curve_name_)

    @classmethod
    def create_as_translate(cls, path, atr_name, keep_namespace=False):
        return cls.create(path, atr_name, keep_namespace=keep_namespace, curve_type='animCurveTL')

    @classmethod
    def create_as_rotate(cls, path, atr_name, keep_namespace=False):
        return cls.create(path, atr_name, keep_namespace=keep_namespace, curve_type='animCurveTA')

    @classmethod
    def create_as_scale(cls, path, atr_name, keep_namespace=False):
        return cls.create(path, atr_name, keep_namespace=keep_namespace, curve_type='animCurveTU')

    def __init__(self, curve_name):
        self._path = curve_name

    @property
    def path(self):
        return self._path

    def clear(self):
        AnmCurveNode.clear_keyframes(self._path)

    def delete(self):
        _node_for_dag.DagNode.delete(self._path)

    def get_index_count(self):
        return cmds.keyframe(
            self._path,
            query=True,
            keyframeCount=True
        ) or 0

    def get_time_at(self, index):
        _ = cmds.keyframe(
            self._path,
            query=1,
            index=(index, index),
            timeChange=1
        )
        if _:
            return _[0]

    def set_time_at(self, index, frame):
        cmds.keyframe(
            self._path,
            index=(index, index),
            timeChange=frame
        )

    def update_time_range(self, index_range, frame_range):
        start_index, end_index = index_range
        start_frame, end_frame = frame_range
        start_frame_pre, end_frame_pre = self.get_time_at(start_index), self.get_time_at(end_index)
        if start_frame > end_frame_pre:
            self.set_time_at(end_index, end_frame)
            self.set_time_at(start_index, start_frame)
        else:
            self.set_time_at(start_index, start_frame)
            self.set_time_at(end_index, end_frame)

    def get_value_at(self, index):
        _ = cmds.keyframe(
            self._path,
            query=1,
            index=(index, index),
            valueChange=1
        )
        if _:
            return _[0]

    def set_value_at(self, index, value):
        cmds.keyframe(
            self._path,
            index=(index, index),
            valueChange=value
        )

    def set_value_at_time(self, frame, value):
        cmds.keyframe(
            self._path,
            time=(frame, frame),
            valueChange=value
        )

    def create_value_at_time(self, frame, value):
        cmds.setKeyframe(
            self._path,
            time=(frame, frame),
            value=value
        )

    def get_tangents_at(self, index):
        list_ = []
        for i_key in self.DATA_KEYS:
            i_kwargs = dict(
                query=1,
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

    def get_tangent_types_at(self, index):
        return (
            cmds.keyTangent(
                self._path, query=1, index=(index, index), inTangentType=1
            )[0],
            cmds.keyTangent(
                self._path, query=1, index=(index, index), outTangentType=1
            )[0]
        )

    def set_tangent_types_at_time(self, frame, in_tangent_type, out_tangent_type):
        """
        Valid values are
        "spline"
        "linear"
        "fast"
        "slow"
        "flat"
        "step"
        "stepnext"
        "fixed"
        "clamped"
        "plateau"
        "auto"
        """
        cmds.keyTangent(
            self._path, time=(frame, frame), inTangentType=in_tangent_type
        )
        cmds.keyTangent(
            self._path, time=(frame, frame), outTangentType=out_tangent_type
        )

    def set_tangents_at_time(self, frame, tangents):
        for i_seq, i_key in enumerate(self.DATA_KEYS):
            i_value = tangents[i_seq]

            i_kwargs = dict(
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

    def get_infinities(self):
        return (
            _attribute.NodeAttribute.get_value(self._path, 'preInfinity'),
            _attribute.NodeAttribute.get_value(self._path, 'postInfinity')
        )

    def set_infinities(self, pre_infinity, post_infinity):
        _attribute.NodeAttribute.set_value(self._path, 'preInfinity', pre_infinity)
        _attribute.NodeAttribute.set_value(self._path, 'postInfinity', post_infinity)

    def set_points(self, points, frame_offset=0, value_factor=1):
        for i in points:
            i_time, i_value, i_tangents = i
            # fixme: time is None?
            if i_time is None:
                continue

            self.create_value_at_time(i_time+frame_offset, i_value*value_factor)
            self.set_tangents_at_time(i_time+frame_offset, i_tangents)

        if points:
            # fix tangent bug
            first_points = points[0]
            f_time, f_value, f_tangents = first_points
            # fixme: time is None?
            if f_time is None:
                return

            self.create_value_at_time(f_time+frame_offset, f_value*value_factor)
            self.set_tangents_at_time(f_time+frame_offset, f_tangents)

    def offset_all_values(self, offset_value):
        index_count = self.get_index_count()
        for i_index in range(index_count):
            i_time = self.get_time_at(i_index)
            i_value = self.get_value_at(i_index)
            i_value_new = i_value+offset_value

            self.create_value_at_time(i_time, i_value_new)

    def do_euler_filter(self):
        cmds.filterCurve(self._path)


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
            i_anm_curve_opt = AnmCurveNodeOpt(i_anm_curve)
            # if i_anm_layer is not None:
            #     i_anm_data = []
            #     for j in self.ANM_LAYER_KEYS:
            #         # noinspection PyUnresolvedReferences
            #         i_anm_data.append(
            #             cmds.getAttr(i_anm_layer+'.'+j)
            #         )
            #     layer_data[i_anm_layer] = i_anm_data

        return layer_data
