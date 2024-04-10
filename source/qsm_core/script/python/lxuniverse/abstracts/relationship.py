# coding:utf-8


# <obj-connection>
class AbsObjConnection(object):
    OBJ_TOKEN = None
    OBJ_PATHSEP = None

    def __init__(self, universe, source_obj_path, source_port_path, target_obj_path, target_port_path):
        self._universe = universe

        self._source_obj_path = source_obj_path
        self._source_port_path = source_port_path

        self._target_obj_path = target_obj_path
        self._target_port_path = target_port_path

    @property
    def universe(self):
        return self._universe

    # obj
    @property
    def source_obj(self):
        return self.universe.get_obj(self._source_obj_path)

    @property
    def target_obj(self):
        return self.universe.get_obj(self._target_obj_path)

    def get_source_obj(self):
        return self.universe.get_obj(self._source_obj_path)

    def get_target_obj(self):
        return self.universe.get_obj(self._target_obj_path)

    # port
    @property
    def source(self):
        port_token = self.OBJ_TOKEN._get_port_source_token_(self._source_port_path)
        return self.source_obj.get_port(port_token)

    @property
    def target(self):
        port_token = self.OBJ_TOKEN._get_port_target_token_(self._target_port_path)
        return self.target_obj.get_port(port_token)

    def _get_stack_key_(self):
        return self.OBJ_TOKEN._get_obj_connection_token_(
            self._source_obj_path, self._source_port_path,
            self._target_obj_path, self._target_port_path
        )

    def __str__(self):
        return '{}(source="{}", target="{}")'.format(
            self.__class__.__name__,
            self.OBJ_TOKEN._get_obj_source_token_(self._source_obj_path, self._source_port_path),
            self.OBJ_TOKEN._get_obj_target_token_(self._target_obj_path, self._target_port_path),
        )

    def __repr__(self):
        return self.__str__()


# <obj-bind>
class AbsObjBind(object):
    def __init__(self, universe, obj):
        self._universe = universe
        self._obj = obj

    @property
    def universe(self):
        return self._universe

    @property
    def obj(self):
        return self._obj

    def _get_stack_key_(self):
        pass

    def __str__(self):
        return '{}(obj="{}")'.format(
            self.__class__.__name__,
            self.obj.path
        )