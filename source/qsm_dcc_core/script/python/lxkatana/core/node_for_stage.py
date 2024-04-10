# coding:utf-8
import six

import time

import lxcontent.core as ctt_core

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core
# katana
from .wrap import *

from . import node as ktn_cor_node


# katana scene graph operator
# noinspection PyUnusedLocal
class KtnSGNodeOpt(object):
    def __init__(self, stage_opt, obj_path):
        self._stage_opt = stage_opt
        self._obj_path = obj_path
        self._traversal = stage_opt._get_traversal_(obj_path)

    def get_path(self):
        return self._obj_path

    def get_port(self, port_path, use_global=False):
        """
        [
            'childList',
            'getBinary',
            'getChildByIndex',
            'getChildByName',
            'getChildName',
            'getGroupInherit',
            'getHash',
            'getHash64',
            'getNumberOfChildren',
            'getSize',
            'getXML',
            'parseBinary',
            'parseXML',
            'writePython']

        """
        tvl = self._traversal
        if tvl.valid():
            if use_global is True:
                attrs = tvl.getLocationData().getAttrs()
            else:
                attrs = tvl.getLocationData().getAttrs()
            if attrs:
                return attrs.getChildByName(port_path)

    def get_port_children(self, port_path):
        p = self.get_port(port_path)
        if p:
            return [i[1] for i in p.childList()]
        return []

    def get_port_child_names(self, port_path):
        p = self.get_port(port_path)
        if p:
            return [p.getChildName(i_idx) for i_idx, i in enumerate(p.childList())]
        return []

    def get_port_raw(self, port_path, use_global=False):
        port = self.get_port(port_path, use_global)
        if port is not None:
            return port.getValue()

    # noinspection PyUnusedLocal
    def get(self, key, use_global=False):
        p = self.get_port(key, use_global=False)
        if p is not None:
            c = p.getNumberOfValues()
            if c == 1:
                return p.getValue()

            _ = p.getData()
            t_c = p.getTupleSize()
            if t_c == 1:
                return list(_)
            return [tuple(_[i:i+t_c]) for i in range(0, c, t_c)]

    def get_properties(self, key):
        def rcs_fnc_(k_):
            _p = attrs.getChildByName(key)
            if hasattr(_p, 'getNumberOfChildren'):
                _c = _p.getNumberOfChildren()
                for _i in range(_c):
                    _i_p = _p.getChildByIndex(_i)
                    print _i_p
                    print dir(_i_p)

        ps = ctt_core.Properties(self)
        tvl = self._traversal
        if tvl.valid():
            attrs = tvl.getLocationData().getAttrs()
            rcs_fnc_(key)


class KtnSGMeshOpt(KtnSGNodeOpt):
    def __init__(self, *args, **kwargs):
        super(KtnSGMeshOpt, self).__init__(*args, **kwargs)

    def get_points(self):
        return self.get('geometry.point.P')

    def get_face_vertices(self):
        pass

    def compute_bbox_args(self):
        points = self.get_points()
        if points:
            xs, ys, zs = zip(*points)
            return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))
        return (0, 0, 0), (0, 0, 0)


# noinspection PyUnusedLocal
class KtnStageOpt(object):
    OBJ_PATHSEP = '/'
    PORT_PATHSEP = '.'
    #
    GEOMETRY_ROOT = '/root/world/geo'
    OBJ_OPT_CLS = KtnSGNodeOpt

    def __init__(self, ktn_obj=None):
        if ktn_obj is not None:
            if isinstance(ktn_obj, six.string_types):
                self._ktn_obj = NodegraphAPI.GetNode(ktn_obj)
            else:
                self._ktn_obj = ktn_obj
        else:
            self._ktn_obj = NodegraphAPI.GetViewNode()
        #
        self._runtime = FnGeolib.GetRegisteredRuntimeInstance()
        self._transaction = self._runtime.createTransaction()
        self._client = self._transaction.createClient()
        #
        self._transaction.setClientOp(self._client, Nodes3DAPI.GetOp(self._transaction, self._ktn_obj))
        self._runtime.commit(self._transaction)
        #
        self.__bbox_cache = dict()

    def _get_traversal_(self, location):
        return FnGeolib.Util.Traversal(
            self._client, location
        )

    def _test_(self, location):
        pass

    def get_obj_exists(self, obj_path):
        t = self._get_traversal_(obj_path)
        return t.valid()

    def get_obj(self, obj_path):
        return self._get_traversal_(obj_path)

    def generate_obj_opt(self, obj_path):
        return KtnSGNodeOpt(self, obj_path)

    def generate_mesh_opt(self, obj_path):
        return KtnSGMeshOpt(self, obj_path)

    def get_descendant_paths_at(self, location):
        list_ = []
        tvl = self._get_traversal_(location)
        while tvl.valid():
            i_obj_path = tvl.getLocationPath()
            if not i_obj_path == location:
                list_.append(i_obj_path)
            tvl.next()
        return list_

    def get_port(self, atr_path):
        _ = atr_path.split(self.PORT_PATHSEP)
        obj_path = _[0]
        port_path = self.PORT_PATHSEP.join(_[1:])
        tvl = self._get_traversal_(obj_path)
        if tvl.valid():
            atrs = tvl.getLocationData().getAttrs()
            return tvl.getLocationData().getAttrs().getChildByName(port_path)

    def get_port_raw(self, atr_path):
        p = self.get_port(atr_path)
        if p is not None:
            c = p.getTupleSize()
            if c == 1:
                return p.getValue()
            return p.getData()

    def get(self, key):
        return self.get_port_raw(key)

    def get_all_paths_at(self, location, type_includes=None, type_excludes=None):
        list_ = []
        tvl = self._get_traversal_(
            location
        )
        # timeout for kill block
        timeout = 60
        start_time = int(time.time())
        while True:
            if (int(time.time())-start_time) > timeout:
                raise RuntimeError(
                    bsc_log.Log.trace_method_error(
                        'location traversal is timeout'
                    )
                )
            #
            if tvl.valid() is False:
                break
            #
            i_path = tvl.getLocationPath()
            i_attrs = tvl.getLocationData().getAttrs()
            # call next in here
            tvl.next()
            # include filter
            if isinstance(type_includes, (tuple, list)):
                i_type_name = i_attrs.getChildByName('type').getValue()
                if i_type_name not in type_includes:
                    continue
            # exclude filter
            if isinstance(type_excludes, (tuple, list)):
                i_attrs = tvl.getLocationData().getAttrs()
                i_type_name = i_attrs.getChildByName('type').getValue()
                if i_type_name in type_excludes:
                    continue
            #
            list_.append(i_path)
        return list_

    def get_all_port_raws_at(self, location, port_path, type_includes=None, type_excludes=None):
        list_ = []
        tvl = self._get_traversal_(
            location
        )
        # timeout for kill block
        timeout = 60
        start_time = int(time.time())
        while True:
            if (int(time.time())-start_time) > timeout:
                raise RuntimeError(
                    bsc_log.Log.trace_method_error(
                        'location traversal is timeout'
                    )
                )
            #
            if tvl.valid() is False:
                break
            #
            i_attrs = tvl.getLocationData().getAttrs()
            # call next in here
            tvl.next()
            # include filter
            if isinstance(type_includes, (tuple, list)):
                i_type_name = i_attrs.getChildByName('type').getValue()
                if i_type_name not in type_includes:
                    continue
            # exclude filter
            if isinstance(type_excludes, (tuple, list)):
                i_attrs = tvl.getLocationData().getAttrs()
                i_type_name = i_attrs.getChildByName('type').getValue()
                if i_type_name in type_excludes:
                    continue
            #
            i_attr = i_attrs.getChildByName(port_path)
            if i_attr is not None:
                i_ = i_attr.getValue()
                list_.append(i_)
        #
        list__ = list(set(list_))
        list__.sort(key=list_.index)
        return list__

    def get_all_paths_at_as_dynamic(self, frame_range, location, type_includes=None, type_excludes=None):
        start_frame, end_frame = frame_range
        if start_frame == end_frame:
            ktn_cor_node.NGNodeOpt(
                NodegraphAPI.GetRootNode()
            ).set('currentTime', start_frame)
            return self.get_all_paths_at(
                location, type_includes, type_excludes
            )
        else:
            list_ = []
            for i_frame in range(start_frame, end_frame+1):
                ktn_cor_node.NGNodeOpt(
                    NodegraphAPI.GetRootNode()
                ).set('currentTime', i_frame)
                #
                i_paths = self.get_all_paths_at(
                    location, type_includes, type_excludes
                )
                list_.extend(i_paths)
            #
            list__ = list(set(list_))
            list__.sort(key=list_.index)
            return list__

    def compute_bbox_args(self, location):
        # cache compute result
        if location in self.__bbox_cache:
            return self.__bbox_cache[location]

        mesh_paths = self.get_all_paths_at(location, type_includes=['subdmesh', 'polymesh'])
        if mesh_paths:
            points = []
            for i_path in mesh_paths:
                i_bbox_args = KtnSGMeshOpt(self, i_path).compute_bbox_args()
                points.extend(i_bbox_args)

            if points:
                xs, ys, zs = zip(*points)
                b = (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))
                self.__bbox_cache[location] = b
                return b
        b = (0, 0, 0), (0, 0, 0)
        self.__bbox_cache[location] = b
        return b

    def compute_geometry_args(self, location, use_int_size=False):
        bbox_args = self.compute_bbox_args(location)
        return bsc_core.RawBBoxMtd.compute_geometry_args(
            bbox_args[0], bbox_args[1], use_int_size
        )

    def __str__(self):
        return '{}(node="{}")'.format(
            self.__class__.__name__,
            self._ktn_obj.getName()
        )


class KtnSGSelectionOpt(object):
    def __init__(self, *args):
        self._paths = args[0]
        self._scene_graph = ScenegraphManager.getActiveScenegraph()

    def select_all(self):
        paths = self._paths
        list_ = []
        for path in paths:
            ps = bsc_core.PthNodeOpt(path).get_ancestor_paths()
            for p in ps:
                if p not in list_:
                    if p != '/':
                        list_.append(p)
        #
        self._scene_graph.addOpenLocations(list_, replace=True)
        self._scene_graph.addSelectedLocations(paths, replace=True)

    @classmethod
    def set_clear(cls):
        ScenegraphManager.getActiveScenegraph().clearOpenLocations()
        ScenegraphManager.getActiveScenegraph().addSelectedLocations([], replace=True)