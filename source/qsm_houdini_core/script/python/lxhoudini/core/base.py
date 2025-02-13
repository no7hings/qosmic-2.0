# coding:utf-8
import six

from .wrap import *


class HouBase(object):
    @classmethod
    def get_descendants(cls, path, include=None):
        def add_fnc(lis_, node_, include_arg_):
            if include_arg_ is not None:
                if node_.type().nameWithCategory() in include_arg_:
                    lis_.append(node_)
            else:
                lis_.append(node_)

        def rcs_fnc(lis_, node_, include_arg_):
            _child_nodes = node_.children()
            for _obj in _child_nodes:
                add_fnc(lis_, _obj, include_arg_)
                rcs_fnc(lis_, _obj, include_arg_)

        lis = []

        if isinstance(path, six.string_types):
            node = hou.node(path)
        else:
            node = path

        if isinstance(include, six.string_types):
            include_arg = [include]
        elif isinstance(include, (tuple, list)):
            include_arg = list(include)
        else:
            include_arg = None
        rcs_fnc(lis, node, include_arg)
        return lis

    @classmethod
    def get_all_inputs(cls, path, include=None):
        def add_fnc(lis_, node_, include_arg_):
            if include_arg_ is not None:
                if node_.type().nameWithCategory() in include_arg_:
                    lis_.append(node_)
            else:
                lis_.append(node_)

        def rcs_fnc(lis_, node_, include_arg_):
            _path = node_.path()
            if _path not in paths:
                paths.append(_path)
                add_fnc(lis_, node_, include_arg_)
                _input_nodes = node_.inputs()
                for _obj in _input_nodes:
                    if _obj is not None:
                        rcs_fnc(lis_, _obj, include_arg_)

        lis = []
        paths = []

        if isinstance(path, six.string_types):
            node = hou.node(path)
        else:
            node = path
        if isinstance(include, six.string_types):
            include_arg = [include]

        elif isinstance(include, (tuple, list)):
            include_arg = list(include)
        else:
            include_arg = None
        rcs_fnc(lis, node, include_arg)
        return lis

    @classmethod
    def get_ancestors(cls, path, include=None):
        def add_fnc(lis_, node_, include_arg_):
            if include_arg_ is not None:
                if node_.type().nameWithCategory() in include_arg_:
                    lis_.append(node_)
            else:
                lis_.append(node_)

        def rcs_fnc(lis_, node_, include_arg_):
            add_fnc(lis_, node_, include_arg_)
            _parent_node = node_.parent()
            if _parent_node is not None:
                rcs_fnc(lis_, _parent_node, include_arg_)

        lis = []

        if isinstance(path, six.string_types):
            node = hou.node(path)
        else:
            node = path

        if isinstance(include, six.string_types):
            include_arg = [include]
        elif isinstance(include, (tuple, list)):
            include_arg = list(include)
        else:
            include_arg = None
        rcs_fnc(lis, node, include_arg)
        return lis

    @classmethod
    def get_geo_is_visible(cls, path):
        if isinstance(path, six.string_types):
            node = hou.node(path)
        else:
            node = path
        if node.isObjectDisplayed() is False:
            return False
        #
        parent_nodes = cls.get_ancestors(node)
        parent_nodes.reverse()
        for i in parent_nodes:
            if isinstance(i, hou.ObjNode):
                if i.isObjectDisplayed() is False:
                    return False
        return True


class HouObj(object):
    def __init__(self):
        pass

    @classmethod
    def get_geos(cls):
        return hou.nodeType('Object/geo').instances()

    @classmethod
    def get_displayed_geos(cls):
        return [i for i in cls.get_geos() if HouBase.get_geo_is_visible(i) is True]

    @classmethod
    def get_render_nodes(cls):
        lis = []
        geos = cls.get_displayed_geos()
        for geo in geos:
            render_node = geo.renderNode()
            if render_node is not None:
                lis.append(render_node)
        return lis

    @classmethod
    def get_geometries(cls):
        lis = []
        for node in cls.get_render_nodes():
            lis.append(node.geometry())
        return lis

    @classmethod
    def get_shops(cls):
        def add_fnc_(node_):
            if isinstance(node_, (unicode, str)):
                _obj = hou.node(node_)
            else:
                _obj = node_
            if _obj is not None:
                _path = _obj.path()
                if _path not in paths:
                    paths.append(_path)
                    lis.append(_obj)

        lis = []
        paths = []

        geos = cls.get_displayed_geos()
        for geo in geos:
            render_node = geo.renderNode()
            if render_node is not None:
                geometry = render_node.geometry()
                attr = geometry.findPrimAttrib('shop_materialpath')
                if attr is not None:
                    materials = geometry.primStringAttribValues('shop_materialpath')
                    for material in materials:
                        add_fnc_(material)
                else:
                    material = hou.parm(geo.path()+'/shop_materialpath').evalAsNode()
                    add_fnc_(material)
        return lis

    @classmethod
    def get_instances(cls):
        return hou.nodeType('Object/instance').instances()

    @classmethod
    def get_displayed_instances(cls):
        return [i for i in cls.get_instances() if HouBase.get_geo_is_visible(i) is True]

    def _test(self):
        pass


class HouGeos(object):
    def __init__(self, *args):
        self._geo_hou_objs = []
        for i in args:
            if isinstance(i, six.string_types):
                geo = hou.node(i)
            else:
                geo = i
            if geo is not None:
                self._geo_hou_objs.append(geo)

    def get_render_nodes(self):
        lis = []
        geos = self._geo_hou_objs
        for geo in geos:
            render_node = geo.renderNode()
            if render_node is not None:
                lis.append(render_node)
        return lis

    def get_geometries(self):
        lis = []
        for render_node in self.get_render_nodes():
            geometry = render_node.geometry()
            lis.append(geometry)
        return lis

    def get_shops(self):
        def add_fnc_(node_):
            if isinstance(node_, (unicode, str)):
                _obj = hou.node(node_)
            else:
                _obj = node_
            if _obj is not None:
                _path = _obj.path()
                if _path not in paths:
                    paths.append(_path)
                    lis.append(_obj)

        lis = []
        paths = []

        geos = self._geo_hou_objs
        for geo in geos:
            render_node = geo.renderNode()
            if render_node is not None:
                geometry = render_node.geometry()
                attr = geometry.findPrimAttrib('shop_materialpath')
                if attr is not None:
                    materials = geometry.primStringAttribValues('shop_materialpath')
                    for material in materials:
                        add_fnc_(material)
                else:
                    material = hou.parm(geo.path()+'/shop_materialpath').evalAsNode()
                    add_fnc_(material)
        return lis

    def get_point_count(self):
        lis = []
        for geometry in self.get_geometries():
            lis.append(len(geometry.points()))
        if lis:
            return sum(lis)
        return 0

    def get_operators(self):
        lis = []
        for i in self._geo_hou_objs:
            parm = i.parm('ar_operator_graph')
            if parm:
                hou_obj = parm.evalAsNode()
                if hou_obj:
                    lis.append(hou_obj)
        return lis


class HouInstances(object):
    def __init__(self, *args):
        self._instance_hou_objs = []
        for i in args:
            if isinstance(i, six.string_types):
                geo = hou.node(i)
            else:
                geo = i
            if geo is not None:
                self._instance_hou_objs.append(geo)

    def get_geos(self):
        lis = []
        paths = []
        for i in self._instance_hou_objs:
            parm = i.parm('instancepath')
            if parm:
                hou_obj = parm.evalAsNode()
                if hou_obj:
                    path = hou_obj.path()
                    if path not in paths:
                        paths.append(path)
                        lis.append(hou_obj)
        return lis


class HoudiniShops(object):
    def __init__(self, *args):
        self._hou_shops = []
        for i in args:
            if isinstance(i, six.string_types):
                shop = hou.node(i)
            else:
                shop = i
            self._hou_shops.append(shop)

    def get_output_vops(self):
        lis = []
        for shop in self._hou_shops:
            output_vops = HouBase.get_descendants(shop, include='Vop/arnold_material')
            for i in output_vops:
                lis.append(i)
        return lis


class HoudiniVops(object):
    def __init__(self, *args):
        self._hou_vops = []
        for i in args:
            if isinstance(i, six.string_types):
                vop = hou.node(i)
            else:
                vop = i
            self._hou_vops.append(vop)

    def get_input_image_vops(self):
        lis = []
        for vop in self._hou_vops:
            image_vops = HouBase.get_all_inputs(vop, include='arnold::Vop/image')
            for i in image_vops:
                lis.append(i)
        return lis
