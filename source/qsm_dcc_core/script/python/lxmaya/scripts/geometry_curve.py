# coding:utf-8
from ..core.wrap import *


class CurveRebuild(object):
    def __init__(self, density=None, span_count=None, sample=10):
        curve_paths = cmds.ls(type='nurbsCurve', selection=1, dagObjects=1, long=1) or []
        self._om2_curves = []
        for crv_pth in curve_paths:
            om2_crv_obj = om2.MGlobal.getSelectionListByName(crv_pth).getDagPath(0)
            om2_crv = om2.MFnNurbsCurve(om2_crv_obj)
            self._om2_curves.append(om2_crv)
        #
        self._density = density
        self._span_count = span_count
        self._sample = sample

    @classmethod
    def _set_range_map_(cls, range_0, range_1, value_0):
        value_min_0, value_max_0 = range_0
        value_min_1, value_max_1 = range_1
        #
        percent = float(value_0-value_min_0)/(value_max_0-value_min_0)
        #
        value_1 = (value_max_1-value_min_1)*percent+value_min_1
        return value_1

    def set_rebuild(self):
        rebuild_dict = {}
        for om2_curve in self._om2_curves:
            path = om2_curve.fullPathName()
            if path in rebuild_dict:
                raw = rebuild_dict[path]
            else:
                raw = {}
                rebuild_dict[path] = raw
            #
            points, tangents = self._get_curve_derivatives_(om2_curve)
            raw['tangents'] = tangents
            raw['points'] = points
            span_count = self._get_curve_span_count_(om2_curve)
            raw['span_count'] = span_count

        first_point = None
        for k, v in rebuild_dict.items():
            points = v['points']
            point_0 = points[0]
            point_1 = points[-1]
            if first_point is None:
                first_point = point_0
            else:
                a = point_0.distanceTo(first_point)
                b = point_0.distanceTo(point_1)
                if a > b/2:
                    v['reverse'] = True

        if rebuild_dict:
            for k, v in rebuild_dict.items():
                span_count = v['span_count']
                if span_count is not None:
                    cmds.rebuildCurve(k, rebuildType=0, spans=span_count)
                reverse = v.get('reverse', False)
                if reverse is True:
                    print 'reverse curve: "{}"'.format(k)
                    cmds.reverseCurve(k, constructionHistory=0, replaceOriginal=1)

    def _get_curve_derivatives_(self, om2_curve):
        points = []
        tangents = []
        length = om2_curve.length()
        for i in range(self._sample+1):
            percent = 1/float(self._sample)*i
            value = self._set_range_map_((0, 1), (0, length), percent)
            param = om2_curve.findParamFromLength(value)
            point, tangent = om2_curve.getDerivativesAtParam(param, 4)
            points.append(point)
            tangent = tangent.normalize()
            tangents.append(tangent)
        return points, tangents

    def _get_curve_span_count_(self, om2_curve):
        length = om2_curve.length()
        if self._density is not None:
            return int(length*self._density)
        elif self._span_count is not None:
            return self._span_count


class MtdCurveRebuild(object):
    def __init__(self, density=None, span_count=None, sample=10):
        curve_paths = cmds.ls(type='nurbsCurve', selection=1, dagObjects=1, long=1) or []
        self._om2_curves = []
        for crv_pth in curve_paths:
            om2_crv_obj = om2.MGlobal.getSelectionListByName(crv_pth).getDagPath(0)
            om2_crv = om2.MFnNurbsCurve(om2_crv_obj)
            self._om2_curves.append(om2_crv)
        #
        self._density = density
        self._span_count = span_count
        self._sample = sample
