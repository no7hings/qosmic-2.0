# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.dcc.abstracts as bsc_dcc_abstracts

import lxuniverse.core as unr_core
# maya
from ...core.wrap import *

from ... import core as mya_core


class XgenDescriptionOpt(bsc_dcc_abstracts.AbsNodeOpt):
    def __init__(self, *args, **kwargs):
        super(XgenDescriptionOpt, self).__init__(*args, **kwargs)

    def get_name(self):
        # use transform name
        return mya_core.MyaUtil.get_name_with_namespace_clear(
            self._obj.get_transform().get_name()
        )

    def get_path(self, lstrip=None):
        # remove namespace, use transform path
        raw = mya_core.MyaUtil.get_path_with_namespace_clear(
            self._obj.get_transform().get_name()
        )
        # replace pathsep
        raw = raw.replace(self._obj.PATHSEP, unr_core.UnrObj.PATHSEP)
        # strip path
        if lstrip is not None:
            if raw.startswith(lstrip):
                raw = raw[len(lstrip):]
        return raw

    def get_path_as_uuid(self, lstrip=None):
        return bsc_core.HashMtd.get_hash_value(self.get_path(lstrip), as_unique_id=True)

    def get_name_as_uuid(self):
        return bsc_core.HashMtd.get_hash_value(self.get_name(), as_unique_id=True)

    def get_usd_basis_curve_data(self):
        guides = cmds.ls(
            self._obj.transform.path, type='xgmSplineGuide', dagObjects=1, noIntermediate=1, long=1
        )

        counts = []
        points = []
        # widths = [0.003]
        widths = []
        for i in guides:
            i_points = mya_core.CmdXgenSplineGuideOpt(
                i
            ).get_control_points()
            counts.append(len(i_points))
            points.extend(i_points)
            widths.append(0.003)
        return counts, points, widths


class XgenSplineGuideOpt(bsc_dcc_abstracts.AbsNodeOpt):
    def __init__(self, *args, **kwargs):
        super(XgenSplineGuideOpt, self).__init__(*args, **kwargs)

    def get_control_points(self):
        return mya_core.CmdXgenSplineGuideOpt(
            self._obj.path
        ).get_control_points()

    def get_curve_data(self):
        points = self.get_control_points()
        degree = 2
        form = 1
        count = len(points)
        knots = mya_core.Om2Base._get_curve_knots_(count, degree)
        span = count - 3
        return points, knots, degree, form, span

    def get_usd_curve_data(self):
        points = self.get_control_points()
        degree = 2
        form = 1
        count = len(points)
        knots = mya_core.Om2Base._get_curve_knots_(count, degree)
        span = count - 3
        ranges = [(0, 1)]
        widths = [.1]
        order = [degree]
        return points, knots, ranges, widths, order

    def get_usd_basis_curve_data(self):
        points = self.get_control_points()
        counts = [len(points)]
        widths = [0.003]
        return counts, points, widths
