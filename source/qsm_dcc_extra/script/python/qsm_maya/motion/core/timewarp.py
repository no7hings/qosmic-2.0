# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.log as bsc_log

from ... import core as _mya_core


class TimewarpOpt(object):
    LOG_KEY = 'timewrap'
    NODE_NAME = 'qsm_timewarp'

    @classmethod
    def create_auto(cls, frame_range_src):
        if _mya_core.Node.is_exists(cls.NODE_NAME) is False:
            curve_name = _mya_core.AnmCurve.create(cls.NODE_NAME, 'animCurveTT')
            cls(curve_name).setup(frame_range_src)

    @classmethod
    @_mya_core.Undo.execute
    def update_by_frame_range(cls, frame_range_src, frame_range_tgt):
        cls.create_auto(frame_range_src)
        opt = cls(cls.NODE_NAME)
        opt.frame_range_src = frame_range_src
        opt.frame_range_tgt = frame_range_tgt
        bsc_log.Log.trace_method_result(
            cls.LOG_KEY, 'warp by range, scale is {}, offset is {}'.format(
                opt.scale, opt.offset
            )
        )
        return True

    @classmethod
    @_mya_core.Undo.execute
    def update_by_scale_value(cls, frame_range_src, scale_value):
        cls.create_auto(frame_range_src)
        start_frame_src, end_frame_src = frame_range_src
        frame_count_src = end_frame_src-start_frame_src+1
        start_frame_tgt = start_frame_src
        end_frame_tgt = start_frame_tgt+int(frame_count_src*scale_value)-1
        opt = cls(cls.NODE_NAME)
        opt.frame_range_src = frame_range_src
        opt.frame_range_tgt = (start_frame_tgt, end_frame_tgt)
        return True

    @classmethod
    def remove(cls):
        if _mya_core.Node.is_exists(cls.NODE_NAME):
            _mya_core.Node.delete(cls.NODE_NAME)
            return True
        return False

    @classmethod
    @_mya_core.Undo.execute
    def apply(cls):
        if _mya_core.Node.is_exists(cls.NODE_NAME) is True:
            opt = cls(cls.NODE_NAME)
            curves = _mya_core.AnimCurves.get_all(reference=False, excludes=['timewarp', 'qsm_timewarp'])

            offset = opt.offset
            if offset != 0:
                _mya_core.AnimCurves.offset(
                    curves, offset
                )

                bsc_log.Log.trace_method_result(
                    cls.LOG_KEY, 'offset all curves, offset is {}'.format(offset)
                )

            scale = opt.scale
            if scale != 1.0:
                scale_pivot = opt.start_frame_tgt
                _mya_core.AnimCurves.scale_by_pivot(
                    curves, opt.scale, opt.start_frame_tgt
                )

                bsc_log.Log.trace_method_result(
                    cls.LOG_KEY, 'scale all curves, scale is {}, scale-pivot is {}'.format(
                        scale, scale_pivot
                    )
                )

            opt.remove()
            return True
        return False

    @classmethod
    def get_frame_range_args(cls):
        if _mya_core.Node.is_exists(cls.NODE_NAME) is True:
            opt = cls(cls.NODE_NAME)
            return opt.frame_range_src, opt.frame_range_tgt

        frame_range = _mya_core.Frame.get_frame_range()
        return frame_range, frame_range

    @classmethod
    def check_is_valid(cls):
        return _mya_core.Node.is_exists(cls.NODE_NAME)

    def __init__(self, curve_name):
        self._curve_name = curve_name
        self._curve_opt = _mya_core.AnmCurveOpt(self._curve_name)

    def setup(self, frame_range_src):
        start_frame_src, end_frame_src = frame_range_src
        # start
        self._curve_opt.create_value_at_time(start_frame_src, start_frame_src)
        self._curve_opt.set_tangent_types_at_time(start_frame_src, 'linear', 'linear')
        # end
        self._curve_opt.create_value_at_time(end_frame_src, end_frame_src)
        self._curve_opt.set_tangent_types_at_time(end_frame_src, 'linear', 'linear')
        self._curve_opt.set_infinities(4, 4)
        # connect to time1
        _mya_core.Connection.create(
            self.NODE_NAME+'.apply', 'time1.timewarpIn_Raw'
        )
        _mya_core.NodeAttribute.set_value(
            'time1', 'enableTimewarp', 1
        )

    @property
    def start_frame_src(self):
        return self._curve_opt.get_value_at(0)

    @property
    def frame_range_src(self):
        return self._curve_opt.get_value_at(0), self._curve_opt.get_value_at(1)

    @frame_range_src.setter
    def frame_range_src(self, frame_range):
        start_frame = min(frame_range)
        end_frame = max(frame_range)
        self._curve_opt.set_value_at(0, start_frame)
        self._curve_opt.set_value_at(1, end_frame)

    @property
    def start_frame_tgt(self):
        return self._curve_opt.get_time_at(0)

    @property
    def frame_range_tgt(self):
        return self._curve_opt.get_time_at(0), self._curve_opt.get_time_at(1)

    @frame_range_tgt.setter
    def frame_range_tgt(self, frame_range):
        start_frame = min(frame_range)
        end_frame = max(frame_range)
        # set end frame first
        self._curve_opt.update_time_range((0, 1), (start_frame, end_frame))

        _mya_core.Frame.set_frame_range(*frame_range)

    @property
    def frame_count_src(self):
        start_frame, end_frame = self.frame_range_src
        return end_frame-start_frame+1

    @property
    def frame_count_tgt(self):
        start_frame, end_frame = self.frame_range_tgt
        return end_frame-start_frame+1

    @property
    def scale(self):
        """
        scale not div by count
        (40-11)/float(20-11)
        """
        start_frame_src, end_frame_src = self.frame_range_src
        start_frame_tgt, end_frame_tgt = self.frame_range_tgt
        return float(end_frame_tgt-start_frame_tgt)/float(end_frame_src-start_frame_src)

    @property
    def scale_pivot(self):
        return self._curve_opt.get_value_at(0)

    @property
    def offset(self):
        return self._curve_opt.get_time_at(0)-self._curve_opt.get_value_at(0)

    @classmethod
    def test(cls):
        cls.create_auto((0, 32))

