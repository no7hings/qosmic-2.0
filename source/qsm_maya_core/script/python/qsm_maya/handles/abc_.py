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

    def set_dict(self, properties):
        self._shape_opt.set_dict(properties)

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


class AbsSetBaseOpt(object):
    SET_ROOT = 'QSM_SET'

    SET_NAME = None

    @classmethod
    def create_root_set(cls):
        return qsm_mya_core.Set.create(cls.SET_ROOT)

    @classmethod
    def create_set(cls):
        set_root = cls.create_root_set()
        set_name = qsm_mya_core.Set.create(cls.SET_NAME)
        qsm_mya_core.Set.add_one(set_root, set_name)
        return set_name


# group
class AbsGroupOrg(AbsSetBaseOpt):
    LOCATION = None

    SET_NAME = 'QSM_GROUP_SET'

    def __init__(self):
        if qsm_mya_core.Node.is_exists(self.LOCATION) is False:
            qsm_mya_core.Group.create_dag(self.LOCATION)

    def add_one(self, path):
        if path.startswith('{}|'.format(self.LOCATION)):
            return path
        return qsm_mya_core.Group.add_one(self.LOCATION, path)

    def find_descendants(self, type_includes):
        return qsm_mya_core.Group.find_descendants(
            self.LOCATION, type_includes
        )


# layer
class AbsLayerOrg(AbsSetBaseOpt):
    NAME = None
    RGB = (0, 0, 0)
    VISIBLE = 0

    SET_NAME = 'QSM_LAYER_SET'

    def __init__(self):
        if qsm_mya_core.Node.is_exists(self.NAME) is False:
            layer_name = qsm_mya_core.DisplayLayer.create(self.NAME)
            qsm_mya_core.DisplayLayer.set_rgb(self.NAME, self.RGB)
            qsm_mya_core.DisplayLayer.set_visible(self.NAME, self.VISIBLE)
            set_name = self.create_set()
            qsm_mya_core.Set.add_one(set_name, layer_name)

    def add_one(self, path):
        qsm_mya_core.DisplayLayer.add_one(self.NAME, path)


class AbsMaterialOrg(AbsSetBaseOpt):
    NAME = None
    RGB = (0, 0, 0)

    SET_NAME = 'QSM_MATERIAL_SET'

    def __init__(self):
        if qsm_mya_core.Node.is_exists(self.NAME) is False:
            qsm_mya_core.Material.create_as_lambert(self.NAME, self.RGB)

    def assign_to(self, path):
        qsm_mya_core.Material.assign_to(self.NAME, path)
