# coding:utf-8
from .. import core as _mya_core


class AbsMeshOpt(object):
    def __init__(self, path_or_name):
        """
        use transform or shape
        """
        if _mya_core.Node.is_exists(path_or_name) is False:
            raise RuntimeError()

        if _mya_core.Node.is_transform_type(path_or_name):
            self._transform_path = _mya_core.DagNode.to_path(path_or_name)
            _ = _mya_core.Transform.get_shape(path_or_name)
            if _mya_core.Node.is_mesh(_) is True:
                self._shape_path = _
            else:
                raise RuntimeError()
        elif _mya_core.Node.is_mesh(path_or_name):
            self._shape_path = _mya_core.DagNode.to_path(path_or_name)
            self._transform_path = _mya_core.Shape.get_transform(path_or_name)
        else:
            raise RuntimeError()
