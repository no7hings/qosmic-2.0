# coding:utf-8
import qsm_maya.core as qsm_mya_core


class AbsShapeOpt(object):
    SHAPE_TYPE = None

    def __init__(self, path_or_name):
        """
        use transform or shape
        """
        if qsm_mya_core.Node.is_exists(path_or_name) is False:
            raise RuntimeError()

        if qsm_mya_core.Node.is_transform_type(path_or_name):
            self._transform_path = qsm_mya_core.DagNode.to_path(path_or_name)
            _ = qsm_mya_core.Transform.get_shape(path_or_name)
            if qsm_mya_core.Node.type_is(_, self.SHAPE_TYPE) is True:
                self._shape_path = _
            else:
                raise RuntimeError()
        elif qsm_mya_core.Node.type_is(path_or_name, self.SHAPE_TYPE):
            self._shape_path = qsm_mya_core.DagNode.to_path(path_or_name)
            self._transform_path = qsm_mya_core.Shape.get_transform(path_or_name)
        else:
            raise RuntimeError()

        self._shape_opt = qsm_mya_core.EtrNodeOpt(self._shape_path)

    @property
    def transform_path(self):
        return self._transform_path

    @property
    def shape_path(self):
        return self._shape_path

    def apply_properties(self, properties):
        self._shape_opt.apply_properties(properties)

    def get_properties(self):
        return {}


class AbsMeshOpt(AbsShapeOpt):
    SHAPE_TYPE = 'mesh'

    def __init__(self, *args, **kwargs):
        super(AbsMeshOpt, self).__init__(*args, **kwargs)


class AbsGroupOpt(object):
    LOCATION = None

    def __init__(self, path_or_name, *args, **kwargs):
        if qsm_mya_core.Node.is_exists(path_or_name) is False:
            raise RuntimeError()

        self._location = qsm_mya_core.Shape.get_transform(path_or_name)
        self._group_opt = qsm_mya_core.GroupOpt(self._location)

    @property
    def location(self):
        return self._location
