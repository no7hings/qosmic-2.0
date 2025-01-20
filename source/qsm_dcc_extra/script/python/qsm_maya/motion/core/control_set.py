# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

from ... import core as _mya_core

from . import base as _base

from . import control as _control


class ControlSetMotionOpt(
    _control.ControlNamespaceExtra,
    _base.AbsMotion
):
    LOG_KEY = 'control set motion'

    @classmethod
    def get_args_from_selection(cls):
        dict_ = {}
        _ = cmds.ls(selection=1, long=1)
        for i_path in _:
            dict_.setdefault(
                _mya_core.DagNode.extract_namespace(i_path), []
            ).append(i_path)
        return dict_

    @classmethod
    def get_args_from_selection_for_mirror(cls):
        dict_ = {}
        _ = cmds.ls(selection=1, long=1)
        for i_path in _:
            # ignore neither has "translate", "rotate"
            if cmds.objExists(i_path+'.translate') is False and cmds.objExists(i_path+'.rotate') is False:
                continue

            dict_.setdefault(
                _mya_core.DagNode.extract_namespace(i_path), []
            ).append(i_path)
        return dict_

    def __init__(self, namespace, paths):
        self._init_namespace_extra(namespace)
        self._path_set = set(paths)

    # motion
    def generate_motion_dict(self):
        dict_ = {}
        c = len(self._path_set)
        if c >= 500:
            with bsc_log.LogProcessContext.create(maximum=len(self._path_set)) as l_p:
                for i_path in self._path_set:
                    i_control_opt = _control.ControlMotionOpt(i_path)
                    dict_[i_control_opt.to_control_key(i_path)] = i_control_opt.generate_motion_properties()

                    l_p.do_update()
        else:
            for i_path in self._path_set:
                i_control_opt = _control.ControlMotionOpt(i_path)
                dict_[i_control_opt.to_control_key(i_path)] = i_control_opt.generate_motion_properties()

        return dict_

    def generate_pose_dict(self):
        dict_ = {}

        for i_path in self._path_set:
            i_control_opt = _control.ControlMotionOpt(i_path)
            dict_[i_control_opt.to_control_key(i_path)] = i_control_opt.generate_pose_properties()

        return dict_

    @_mya_core.Undo.execute
    def apply_motion_dict(self, data, **kwargs):
        bsc_log.Log.trace_method_result(
            self.LOG_KEY,
            'apply motion data: "{}"'.format(', '.join(['{}={}'.format(k, v) for k, v in kwargs.items()]))
        )

        key_excludes = kwargs.pop('control_key_excludes') if 'control_key_excludes' in kwargs else None

        for i_path in self._path_set:
            i_key = _control.ControlMotionOpt.to_control_key(i_path)
            if key_excludes:
                if i_key in key_excludes:
                    continue

            if i_key in data:
                _control.ControlMotionOpt(i_path).apply_motion_properties(data[i_key], **kwargs)

    @_mya_core.Undo.execute
    def apply_pose_dict(self, data, **kwargs):
        bsc_log.Log.trace_method_result(
            self.LOG_KEY,
            'apply pose data: "{}"'.format(', '.join(['{}={}'.format(k, v) for k, v in kwargs.items()]))
        )

        key_excludes = kwargs.pop('control_key_excludes') if 'control_key_excludes' in kwargs else None

        for i_path in self._path_set:
            i_key = _control.ControlMotionOpt.to_control_key(i_path)
            if key_excludes:
                if i_key in key_excludes:
                    continue

            if i_key in data:
                _control.ControlMotionOpt(i_path).apply_pose_properties(data[i_key], **kwargs)

    def export_motion_to(self, file_path):
        bsc_storage.StgFileOpt(file_path).set_write(self.generate_motion_dict())

    def export_pose_to(self, file_path):
        bsc_storage.StgFileOpt(file_path).set_write(self.generate_pose_dict())

    def load_motion_from(self, file_path, **kwargs):
        self.apply_motion_dict(
            bsc_storage.StgFileOpt(file_path).set_read(), **kwargs
        )

    def load_pose_from(self, file_path, **kwargs):
        self.apply_pose_dict(
            bsc_storage.StgFileOpt(file_path).set_read(), **kwargs
        )

    @_mya_core.Undo.execute
    def mirror_all_auto(self, **kwargs):
        for i_path in self._path_set:
            _control.ControlMotionOpt(i_path).do_mirror_auto(
                **kwargs
            )

    @_mya_core.Undo.execute
    def mirror_all_left_to_right(self, **kwargs):
        # mark axis vector first
        axis_vector_dict = self.generate_axis_vector_dict()
        for i_path in self._path_set:
            # ignore neither has "translate", "rotate"
            if cmds.objExists(i_path+'.translate') is False and cmds.objExists(i_path+'.rotate') is False:
                continue

            _control.ControlMotionOpt(i_path).do_mirror_side(
                self.MirrorSchemes.LeftToRight,
                axis_vector_dict=axis_vector_dict,
                **kwargs
            )

    @_mya_core.Undo.execute
    def mirror_all_middle(self, **kwargs):
        # mark axis vector first
        axis_vector_dict = self.generate_axis_vector_dict()
        for i_path in self._path_set:
            # ignore neither has "translate", "rotate"
            if cmds.objExists(i_path+'.translate') is False and cmds.objExists(i_path+'.rotate') is False:
                continue

            _control.ControlMotionOpt(i_path).do_mirror_middle(axis_vector_dict=axis_vector_dict, **kwargs)

    @_mya_core.Undo.execute
    def mirror_all_right_to_left(self, **kwargs):
        # mark axis vector first
        axis_vector_dict = self.generate_axis_vector_dict()
        for i_path in self._path_set:
            # ignore neither has "translate", "rotate"
            if cmds.objExists(i_path+'.translate') is False and cmds.objExists(i_path+'.rotate') is False:
                continue

            _control.ControlMotionOpt(i_path).do_mirror_side(
                self.MirrorSchemes.RightToLeft, axis_vector_dict=axis_vector_dict, **kwargs
            )

    @_mya_core.Undo.execute
    def flip_all(self, **kwargs):
        # mark data first
        data = self.generate_motion_dict()
        # mark axis vector
        axis_vector_dict = self.generate_axis_vector_dict()

        key_excludes = kwargs.pop('control_key_excludes') if 'control_key_excludes' in kwargs else None

        for i_key, i_data in data.items():
            if key_excludes:
                if i_key in key_excludes:
                    continue

            i_path = self.find_one_control(i_key)
            # ignore neither has "translate", "rotate"
            if cmds.objExists(i_path+'.translate') is False and cmds.objExists(i_path+'.rotate') is False:
                continue

            _control.ControlMotionOpt(i_path).do_mirror_auto(
                data_override=i_data, axis_vector_dict=axis_vector_dict, **kwargs
            )

    @_mya_core.Undo.execute
    def reset_transformation(self, translate=False, rotate=False, auto_keyframe=False):
        # mark auto key
        auto_key_mark = cmds.autoKeyframe(state=1, query=1)
        if auto_key_mark:
            cmds.autoKeyframe(state=False)

        if auto_keyframe is True:
            cmds.autoKeyframe(state=True)

        atr_names = []
        if translate is True:
            atr_names.extend(
                ['translateX', 'translateY', 'translateZ']
            )
        if rotate is True:
            atr_names.extend(
                ['rotateX', 'rotateY', 'rotateZ']
            )

        if not atr_names:
            return

        flag = False

        for i_path in self._path_set:
            for j_atr_name in atr_names:
                j_atr = '{}.{}'.format(i_path, j_atr_name)

                # ignore non exists
                if cmds.objExists(j_atr) is False:
                    continue

                # ignore non settable
                if _mya_core.NodeAttribute.is_settable(i_path, j_atr_name) is False:
                    continue

                j_value = round(cmds.getAttr(j_atr), 4)
                if j_value != 0:
                    flag = True
                    cmds.setAttr(j_atr, 0)

        if auto_keyframe is True:
            cmds.autoKeyframe(state=False)

        if auto_key_mark:
            cmds.autoKeyframe(state=True)

        return flag

    def generate_axis_vector_dict(self):
        # reset rotate
        flag = self.reset_transformation(rotate=True)
        # undo reset
        dict_ = {}
        # noinspection PyBroadException
        try:
            for i_path in self._path_set:
                dict_[i_path] = _mya_core.AxisVector.generate_for(i_path)
        except Exception:
            pass

        if flag is True:
            cmds.undo()
        return dict_


class ControlSetBake(object):
    def __init__(self, paths):
        self._paths = paths

    @_mya_core.Undo.execute
    def execute(
        self,
        start_frame, end_frame,
        attributes, frame_extend=0,
        # todo: reduce_filter make detail lost, default use False?
        euler_filter=True, reduce_filter=False, **kwargs
    ):
        """
        bakeResults
            -simulation true
            -t "0:32"
            -sampleBy 1
            -oversamplingRate 1
            -disableImplicitControl true
            -preserveOutsideKeys true
            -sparseAnimCurveBake false
            -removeBakedAttributeFromLayer false
            -removeBakedAnimFromLayer false
            -bakeOnOverrideLayer false
            -minimizeRotation true
            -controlPoints false
            -shape true
            {
                "sam_Skin:Main"
            };
        """
        options = dict(
            time=(start_frame-frame_extend, end_frame+frame_extend),
            simulation=1,
            sampleBy=1,
            oversamplingRate=1,
            disableImplicitControl=1,
            preserveOutsideKeys=1,
            sparseAnimCurveBake=0,
            removeBakedAttributeFromLayer=0,
            removeBakedAnimFromLayer=0,
            bakeOnOverrideLayer=0,
            minimizeRotation=1,
            controlPoints=0,
            shape=0,
            attribute=attributes
        )

        options.update(kwargs)
        cmds.bakeResults(
            self._paths,
            **options
        )

        # remove non change frames
        self._simplify(start_frame, end_frame, attributes)

        # filter
        curves = _mya_core.AnmCurveNodes.get_all_from(self._paths)

        # euler filter
        if euler_filter is True:
            cmds.filterCurve(
                *curves
            )

        # reduce
        if reduce_filter is True:
            cmds.filterCurve(
                curves,
                filter='keyReducer',
                precisionMode=1,
                precision=2.5,
            )

    def _simplify(self, start_frame, end_frame, attributes):
        """
        simplify
            -timeTolerance 0.05
            -floatTolerance 0.05
            -valueTolerance 0.01
            {
                "nurbsCircle1.visibility",
                "nurbsCircle1.translateX",
                "nurbsCircle1.translateY",
                "nurbsCircle1.translateZ",
                "nurbsCircle1.rotateX",
                "nurbsCircle1.rotateY",
                "nurbsCircle1.rotateZ",
                "nurbsCircle1.scaleX",
                "nurbsCircle1.scaleY",
                "nurbsCircle1.scaleZ"
            };
        """
        options = dict(
            time=(start_frame, end_frame),
            timeTolerance=.05,
            floatTolerance=.05,
            valueTolerance=0.01,
            attribute=attributes
        )
        cmds.simplify(
            self._paths,
            **options
        )

    @classmethod
    def test(cls):
        cls(['nurbsCircle1']).execute(0, 32)
