# coding:utf-8
import qsm_maya.core as qsm_mya_core


class Node(object):
    DEFORM_NODE_TYPES = [
        'deformBend',
        'deformFlare',
        'deformSine',
        'deformSquash',
        'deformTwist',
        'deformWave',
    ]

    DEFORM_NODE = 'nonLinear'

    def __init__(self, path):
        self._path = path
        self._node_opt = qsm_mya_core.BscNodeOpt(path)

    def get_data(self):
        dct = {}
        for i_port in self._node_opt.get_all_ports():
            dct[i_port.port_path] = i_port.get()
        return dct

    def get_deform_data(self):
        dct = {}
        for i_port in self._node_opt.get_all_ports(includes=self._node_opt.get_all_keyable_port_paths()):
            dct[i_port.port_path] = i_port.get()
        return dct

    def apply_data(self, data):
        for k, v in data.items():
            i_port = self._node_opt.get_port(k)
            if i_port.is_locked():
                continue
            # noinspection PyBroadException
            try:
                i_port.set(v)
            except Exception:
                print self._path, k, v
                import traceback
                traceback.print_exc()

    @classmethod
    def guess_scheme(cls, path):
        if qsm_mya_core.Transform.check_is_transform(path) is True:
            shape_path = qsm_mya_core.Transform.get_shape_path(path)
            shape_type = qsm_mya_core.Node.get_type(shape_path)
        elif qsm_mya_core.Shape.check_is_shape(path) is True:
            shape_type = qsm_mya_core.Node.get_type(path)
        else:
            return

        if shape_type in cls.DEFORM_NODE_TYPES:
            return DeformShape(path)
        else:
            return CustomShape(path)

    def test(self):
        print self.get_data()


class _AbsShape(object):
    pass


class CustomShape(_AbsShape):
    def __init__(self, path):
        self._path = path

    def find_transform(self):
        return qsm_mya_core.Shape.get_transform(self._path)


class DeformShape(_AbsShape):
    AttributeMapper = dict(

    )

    def __init__(self, path):
        self._path = path

    def find_transform(self):
        return qsm_mya_core.Shape.get_transform(self._path)

    def find_non_linear(self):
        _ = qsm_mya_core.NodeAttribute.get_target_nodes(
            self._path, 'deformerData', 'nonLinear'
        )
        if _:
            return _[0]
        return

    def get_transform_data(self):
        _ = self.find_transform()
        if _:
            return Node(_).get_data()

    def get_non_linear_data(self):
        _ = self.find_non_linear()
        if _:
            return Node(_).get_data()

    def get_data(self):
        return dict(
            transform=self.get_transform_data() or {},
            shape={},
            nonLinear=self.get_non_linear_data() or {}
        )

    def apply_transform_data(self, data):
        _ = self.find_transform()
        if _:
            Node(_).apply_data(data)

    def apply_non_linear_data(self, data):
        _ = self.find_non_linear()
        if _:
            Node(self.find_non_linear()).apply_data(data)

    def apply_data(self, data, key_includes=None):
        self.apply_transform_data(data['transform'])
        self.apply_non_linear_data(data['nonLinear'])


class FxShape(_AbsShape):
    nucleus = 'nucleus'
    pass
