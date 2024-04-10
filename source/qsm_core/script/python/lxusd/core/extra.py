# coding:utf-8
import six

import collections

import math

import fnmatch

import os

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxuniverse.core as unr_core
# usd
from .wrap import *

from . import configure as usd_cor_configure


class UsdBasic(object):
    @classmethod
    def _open_file_(cls, file_path):
        return Usd.Stage.Open(file_path, Usd.Stage.LoadAll)

    @classmethod
    def copy_with_references_fnc(cls, file_path_src, directory_tgt, replace=False):
        s = Usd.Stage.Open(file_path_src, Usd.Stage.LoadAll)
        layers = s.GetUsedLayers()
        directory_src = bsc_storage.StgFileOpt(file_path_src).get_directory_path()
        for i in layers:
            i_file_path_src = i.realPath
            if i_file_path_src:
                i_name = i_file_path_src[len(directory_src)+1:]
                i_file_path_tgt = '{}/{}'.format(directory_tgt, i_name)
                bsc_storage.StgFileOpt(i_file_path_src).copy_to_file(
                    i_file_path_tgt, replace=replace
                )


class UsdStageOpt(UsdBasic):
    KEY = 'usd stage'

    def __init__(self, *args):
        if not args:
            stage = Usd.Stage.CreateInMemory()
        else:
            if isinstance(args[0], Usd.Stage):
                stage = args[0]
            elif isinstance(args[0], six.string_types):
                file_path = args[0]
                if os.path.isfile(file_path) is True:
                    # bsc_log.Log.trace_method_result(
                    #     self.KEY, 'open file is started: "{}"'.format(
                    #         file_path
                    #     )
                    # )
                    stage = self._open_file_(file_path)
                    # bsc_log.Log.trace_method_result(
                    #     self.KEY, 'open file is completed: "{}"'.format(
                    #         file_path
                    #     )
                    # )
                else:
                    raise OSError()
            else:
                raise TypeError()
        #
        self._usd_stage = stage
        self._usd_stage.SetMetadata("metersPerUnit", 0.01)
        #
        UsdGeom.SetStageUpAxis(
            self._usd_stage, UsdGeom.Tokens.y
        )

    @property
    def usd_instance(self):
        return self._usd_stage

    def append_sublayer(self, file_path):
        root_layer = self._usd_stage.GetRootLayer()
        if os.path.isfile(file_path) is True:
            root_layer.subLayerPaths.append(file_path)
            bsc_log.Log.trace_method_result(
                'usd-layer-append',
                u'file="{}"'.format(file_path)
            )
        else:
            bsc_log.Log.trace_method_warning(
                'usd-layer-append',
                u'file="{}" is non-exist'.format(file_path)
            )

    def do_flatten(self):
        self._usd_stage.Flatten()

    def set_sublayer_prepend(self, file_path):
        root_layer = self._usd_stage.GetRootLayer()
        if os.path.isfile(file_path) is True:
            root_layer.subLayerPaths.insert(0, file_path)
            bsc_log.Log.trace_method_result(
                'usd-layer prepend',
                u'file="{}"'.format(file_path)
            )
        else:
            bsc_log.Log.trace_method_warning(
                'usd-layer prepend',
                u'file="{}" is non-exist'.format(file_path)
            )

    def set_default_prim(self, path_text):
        prim = self._usd_stage.GetPrimAtPath(path_text)
        self._usd_stage.SetDefaultPrim(prim)
        #
        bsc_log.Log.trace_method_result(
            'default-prim set',
            u'obj="{}"'.format(path_text)
        )

    def get_default_prim(self):
        return self._usd_stage.GetDefaultPrim()

    def export_to(self, file_path):
        self._usd_stage.Export(file_path)
        bsc_log.Log.trace_method_result(
            'usd-export',
            u'file="{}"'.format(file_path)
        )
        #
        # import os
        # base, ext = os.path.splitext(file_path)
        # self._usd_stage.Export(base + '.usda')
        # #
        # bsc_log.Log.trace_method_result(
        #     'usd-geometry-export',
        #     'file-path: "{}"'.format(file_path)
        # )

    def set_obj_create_as_override(self, path_text):
        bsc_log.Log.trace_method_result(
            'override-prim create',
            u'obj="{}"'.format(path_text)
        )
        return self._usd_stage.OverridePrim(path_text)

    def get_obj_is_exists(self, path_text):
        return self._usd_stage.GetPrimAtPath(path_text).IsValid()

    def get_obj(self, path_text):
        return self._usd_stage.GetPrimAtPath(path_text)

    def get_exists_obj(self, path_text):
        _ = self._usd_stage.GetPrimAtPath(path_text)
        if _.IsValid():
            return _

    def create_obj(self, path_text, type_name=''):
        path_opt = bsc_core.PthNodeOpt(path_text)
        paths = path_opt.get_component_paths()
        paths.reverse()
        for i_path in paths:
            if i_path != '/':
                if self._usd_stage.GetPrimAtPath(path_text).IsValid() is False:
                    self._usd_stage.DefinePrim(i_path, type_name)
        return self.get_obj(path_text)

    def create_one(self, path_text, type_name=''):
        return self._usd_stage.DefinePrim(
            path_text, type_name
        )

    def copy_dag_from(self, usd_prim):
        usd_stage = usd_prim.GetStage()
        path_text = usd_prim.GetPath().pathString
        path_opt = bsc_core.PthNodeOpt(path_text)
        paths = path_opt.get_component_paths()
        paths.reverse()
        for i_path in paths:
            if i_path != '/':
                if self._usd_stage.GetPrimAtPath(path_text).IsValid() is False:
                    i_prim = usd_stage.GetPrimAtPath(i_path)
                    i_type_name = i_prim.GetTypeName()
                    i_prim_new = self._usd_stage.DefinePrim(i_path, i_type_name)
                    self.copy_prim_attributes_fnc(i_prim, i_prim_new)
        return self.get_obj(path_text)

    @staticmethod
    def copy_prim_attributes_fnc(prim, prim_new):
        attributes = prim.GetAuthoredAttributes()
        for i_attribute in attributes:
            i_attribute_new = prim_new.CreateAttribute(
                i_attribute.GetName(), i_attribute.GetTypeName(), i_attribute.IsCustom(), i_attribute.GetVariability()
            )
            i_attribute_new.Set(i_attribute.Get())

    def copy_one_from(self, usd_prim, path_text=None, type_name=None):
        if path_text is None:
            path_text = usd_prim.GetPath().pathString
        if type_name is None:
            type_name = usd_prim.GetTypeName()
        return self._usd_stage.DefinePrim(
            path_text, type_name
        )

    def set_root_create(self, root, override=False):
        dag_path_comps = bsc_core.PthNodeMtd.get_dag_component_paths(
            root, pathsep=usd_cor_configure.UsdNodes.PATHSEP
        )
        if dag_path_comps:
            dag_path_comps.reverse()
        #
        for i_path in dag_path_comps:
            if i_path != usd_cor_configure.UsdNodes.PATHSEP:
                if override is True:
                    self.set_obj_create_as_override(i_path)
                else:
                    self._usd_stage.DefinePrim(i_path, usd_cor_configure.UsdNodeTypes.Xform)
        #
        default_prim_path = self._usd_stage.GetPrimAtPath(dag_path_comps[-1])
        self._usd_stage.SetDefaultPrim(default_prim_path)

    def get_objs(self, regex):
        list_ = []
        for i_usd_prim in self._usd_stage.TraverseAll():
            i_usd_prim_opt = UsdPrimOpt(i_usd_prim)
            list_.append(i_usd_prim_opt.get_path())
        #
        path_opt = bsc_core.PthNodeOpt(regex)
        #
        child_paths = bsc_core.PthNodeMtd.find_dag_child_paths(
            path_opt.get_parent_path(), list_
        )
        #
        return [
            self.get_obj(i) for i in fnmatch.filter(child_paths, regex)
        ]

    def get_obj_paths(self, regex):
        return [UsdPrimOpt(i).get_path() for i in self.get_objs(regex)]

    @classmethod
    def _set_metadata_copy_(cls, src_stage, tgt_stage):
        copy_list = [
            'metersPerUnit',
            'upAxis',
            #
            'startTimeCode',
            'endTimeCode',

        ]
        for i in copy_list:
            tgt_stage.SetMetadata(
                i, src_stage.GetMetadata(i)
            )

    def set_copy_to_new_stage(self, file_path):
        path_src = '/assets/chr/laohu_xiao'
        path_tgt = '/master/hi'
        #
        src_file_path = '/data/f/usd-cpy/test_src_1.usda'
        tgt_file_path = '/data/f/usd-cpy/test_tgt_3.usda'
        #
        src_stage_opt = self.__class__(src_file_path)
        src_stage = src_stage_opt.usd_instance
        src_layer = src_stage.GetRootLayer()
        src_obj = src_stage_opt.get_obj(path_src)
        #
        tgt_stage_opt = self.__class__()
        tgt_stage = tgt_stage_opt.usd_instance
        tgt_layer = tgt_stage.GetRootLayer()
        tgt_obj = tgt_stage_opt.create_obj(path_tgt)
        tgt_stage_opt.set_default_prim(
            '/master'
        )

        # Sdf.CopySpec(
        #     src_layer,
        #     src_obj.GetPath(),
        #     tgt_layer,
        #     tgt_obj.GetPath()
        # )

        self._set_metadata_copy_(src_stage, tgt_stage)

        tgt_stage_opt.export_to(
            tgt_file_path
        )

    def get_fps(self):
        return self._usd_stage.GetTimeCodesPerSecond()

    def set_frame(self, frame):
        self._usd_stage.Set()

    def set_frame_range(self, start_frame, end_frame):
        pass

    def get_frame_range(self):
        return (
            int(self._usd_stage.GetStartTimeCode()),
            int(self._usd_stage.GetEndTimeCode())
        )

    def get_all_objs(self):
        list_ = []
        for i_usd_prim in self._usd_stage.TraverseAll():
            list_.append(i_usd_prim)
        return list_

    def get_all_obj_paths(self):
        list_ = []
        for i_usd_prim in self._usd_stage.TraverseAll():
            if i_usd_prim.IsValid() is True:
                list_.append(i_usd_prim.GetPath().pathString)
        return list_

    def get_count(self):
        return len([i for i in self._usd_stage.TraverseAll()])

    def find_obj_paths(self, regex):
        def get_fnc_(path_, depth_):
            _depth = depth_+1
            if _depth <= depth_maximum:
                _prim = self._usd_stage.GetPrimAtPath(path_)
                _filter_name = filter_names[_depth]

                if path_ == '/':
                    _filter_path = '/*'
                else:
                    _filter_path = '{}/{}'.format(
                        path_, _filter_name
                    )
                _child_paths = UsdPrimOpt(_prim).get_child_paths()
                _filter_child_paths = fnmatch.filter(
                    _child_paths, _filter_path
                )
                if _filter_child_paths:
                    for _i_filter_child_path in _filter_child_paths:
                        if _depth == depth_maximum:
                            list_.append(_i_filter_child_path)
                        get_fnc_(_i_filter_child_path, _depth)

        #
        list_ = []
        #
        filter_names = regex.split('/')
        depth_maximum = len(filter_names)-1

        get_fnc_('/', 0)
        return list_

    def set_active_at(self, location, boolean):
        prim = self._usd_stage.GetPrimAtPath(location)
        if prim.IsValid():
            prim.SetActive(boolean)

    def get_bounding_box(self, location=None, active=False):
        b_box_cache = UsdGeom.BBoxCache(
            1,
            includedPurposes=[
                UsdGeom.Tokens.default_,
                UsdGeom.Tokens.render,
                UsdGeom.Tokens.proxy
            ],
            useExtentsHint=True,
            ignoreVisibility=True,
        )
        if location is not None:
            usd_prim = self._usd_stage.GetPrimAtPath(location)
        else:
            usd_prim = self._usd_stage.GetDefaultPrim()
        return b_box_cache.ComputeWorldBound(usd_prim)

    def compute_geometry_args(self, location=None, use_int_size=False):
        if self.get_obj_is_exists(location) is True:
            b_box = self.get_bounding_box(location)
            r = b_box.GetRange()
            return bsc_core.RawBBoxMtd.compute_geometry_args(
                r.GetMin(), r.GetMax(), use_int_size
            )

    def compute_bbox_args(self, location=None, use_int_size=False):
        if self.get_obj_is_exists(location) is True:
            b_box = self.get_bounding_box(location)
            r = b_box.GetRange()
            return r.GetMin(), r.GetMax()

    def compute_bbox(self):
        pass

    def get_radius(self, pivot):
        b_box_cache = UsdGeom.BBoxCache(
            1,
            includedPurposes=[
                UsdGeom.Tokens.default_,
                UsdGeom.Tokens.render,
                UsdGeom.Tokens.proxy
            ],
            useExtentsHint=True,
            ignoreVisibility=True,
        )
        dict_ = {}
        for i_usd_prim in self._usd_stage.TraverseAll():
            if i_usd_prim.IsValid():
                i_b_box = b_box_cache.ComputeWorldBound(i_usd_prim)
                if i_usd_prim.GetTypeName() in [
                    usd_cor_configure.UsdNodeTypes.Mesh
                ]:
                    i_range = i_b_box.GetRange()
                    i_radius = bsc_core.RawBBoxMtd.get_radius(
                        i_range.GetMin(), i_range.GetMax(), pivot
                    )
                    dict_.setdefault(
                        i_radius, []
                    ).append(
                        i_usd_prim
                    )
        if dict_:
            usd_prim = dict_[max(dict_.keys())][0]
            return UsdMeshOpt(
                UsdGeom.Mesh(usd_prim)
            ).get_radius(pivot)

    def load_by_locations_fnc(self, file_path, locations, active_locations=None):
        stage_tmp = Usd.Stage.Open(file_path, Usd.Stage.LoadAll)
        if isinstance(active_locations, (tuple, list)):
            for i in active_locations:
                i_p = stage_tmp.GetPrimAtPath(i)
                if i_p.IsValid():
                    i_p.SetActive(True)
        #
        for i_location_arg in locations:
            if isinstance(i_location_arg, (tuple, list)):
                i_location_source, i_location_target = i_location_arg
            elif isinstance(i_location_arg, six.string_types):
                i_location_source, i_location_target = i_location_arg, i_location_arg
            else:
                raise RuntimeError()
            # when target is exists, use target
            # etc. we have source location "/master/hi", need map to "/master/mod/hi", "/master/hi" is already exists, use "/master/hi"
            i_p_tgt = stage_tmp.GetPrimAtPath(i_location_target)
            if i_p_tgt.IsValid():
                self.load_by_location_fnc(file_path, i_location_target, i_location_target)
            # when target is non exists, use source and reference source to target
            else:
                i_p_src = stage_tmp.GetPrimAtPath(i_location_source)
                if i_p_src.IsValid():
                    self.load_by_location_fnc(file_path, i_location_source, i_location_target)
        #
        self._usd_stage.Flatten()

    def load_by_location_fnc(self, file_path, location_source, location_target):
        usd_location = self._usd_stage.GetPseudoRoot()
        #
        dag_path_comps = bsc_core.PthNodeMtd.get_dag_component_paths(
            location_target, pathsep=usd_cor_configure.UsdNodes.PATHSEP
        )
        if dag_path_comps:
            dag_path_comps.reverse()
        #
        for i in dag_path_comps:
            if i != usd_cor_configure.UsdNodes.PATHSEP:
                usd_location = self._usd_stage.DefinePrim(i, usd_cor_configure.UsdNodeTypes.Xform)
        #
        usd_location.GetReferences().AddReference(file_path, location_source)

    def get_all_mesh_objs(self):
        return [i for i in self._usd_stage.TraverseAll() if i.IsA(UsdGeom.Mesh)]

    def get_all_instance_objs(self):
        return [i for i in self._usd_stage.TraverseAll() if i.IsA(UsdGeom.PointInstancer)]

    def get_all_points_objs(self):
        return [i for i in self._usd_stage.TraverseAll() if i.IsA(UsdGeom.Points)]

    def get_reference_dict(self):
        dict_ = []
        _ = self._usd_stage.GetUsedLayers()
        for i in _:
            i_prims = i.rootPrims
            print i.pseudoRoot, 'AAA'
            if i_prims:
                print i_prims[0].path
                print i_prims[0].layer
                # print i.subLayerPaths
                # print i.realPath
            # dict_[i_prim.GetPath().pathString] = i_prim.realPath
        return dict_

    def delete_obj(self, *args):
        _ = args[0]
        if isinstance(_, Usd.Prim):
            self._usd_stage.RemovePrim(_.GetPath())
        if isinstance(_, Sdf.Path):
            self._usd_stage.RemovePrim(_)
        elif isinstance(_, six.string_types):
            self._usd_stage.RemovePrim(
                self._usd_stage.GetPrimAtPath(_).GetPath()
            )


class UsdFileWriteOpt(object):
    def __init__(self, file_path):
        self._file_path = file_path
        self._usd_stage = Usd.Stage.CreateInMemory()

    def set_location_add(self, location):
        dag_path_comps = bsc_core.PthNodeMtd.get_dag_component_paths(
            location, pathsep=usd_cor_configure.UsdNodes.PATHSEP
        )
        if dag_path_comps:
            dag_path_comps.reverse()
        #
        for i in dag_path_comps:
            if i != usd_cor_configure.UsdNodes.PATHSEP:
                self.set_obj_add(i)
        #
        default_prim_path = self._usd_stage.GetPrimAtPath(dag_path_comps[1])
        self._usd_stage.SetDefaultPrim(default_prim_path)

    def set_obj_add(self, path):
        self._usd_stage.DefinePrim(path, usd_cor_configure.UsdNodeTypes.Xform)

    def set_save(self):
        file_opt = bsc_storage.StgFileOpt(self._file_path)
        file_opt.create_directory()
        self._usd_stage.Export(self._file_path)
        bsc_log.Log.trace_method_result(
            'usd-export',
            u'file="{}"'.format(self._file_path)
        )


class UsdFileOpt(object):
    def __init__(self, file_path, location=None):
        if location is not None:
            usd_stage_mask = Usd.StagePopulationMask()
            usd_stage_mask.Add(
                Sdf.Path(location)
            )
            self._usd_stage = Usd.Stage.OpenMasked(
                file_path, usd_stage_mask
            )
        else:
            self._usd_stage = Usd.Stage.OpenMasked(
                file_path, Usd.Stage.LoadAll
            )

    def get_usd_instance(self):
        return self._usd_stage

    usd_instance = property(get_usd_instance)


class UsdStageDataOpt(object):
    def __init__(self, stage=None):
        self._usd_stage = stage

    @property
    def usd_instance(self):
        return self._usd_stage

    def set_create(self, type_, value):
        pass


class UsdPrimOpt(object):
    def __init__(self, usd_prim):
        self._usd_prim = usd_prim

    def get_stage(self):
        return self._usd_prim.GetStage()

    def get_type_name(self):
        return self._usd_prim.GetTypeName()

    def get_path(self):
        return self._usd_prim.GetPath().pathString

    def get_name(self):
        return self._usd_prim.GetName()

    def get_port(self, port_path):
        return self._usd_prim.GetAttribute(port_path)

    def get(self, key):
        p = self._usd_prim.GetAttribute(key)
        if p.GetNumTimeSamples():
            return p.Get(0)
        return p.Get()

    def get_customize_ports(self):
        return self._usd_prim.GetAuthoredAttributes() or []

    def get_customize_attributes(self, includes=None, use_full_path=False):
        dic = {}
        _ = self.get_customize_ports()
        for i in _:
            p = i.GetName().split(':')[-1]
            if isinstance(includes, (tuple, list)):
                if p not in includes:
                    continue
            dic[p] = i.Get()
        return dic

    def get_parent(self):
        return self._usd_prim.GetParent()

    def get_parent_path(self):
        return self.__class__(
            self._usd_prim.GetParent()
        ).get_path()

    def get_ancestors(self):
        list_ = []
        root = self.get_stage().GetPseudoRoot()
        p_cur = self._usd_prim
        while p_cur != root:
            p_cur = p_cur.GetParent()
            list_.append(p_cur)
        return list_

    def find_ancestors(self, includes):
        if not isinstance(includes, (tuple, list)):
            raise RuntimeError()

        list_ = []
        root = self.get_stage().GetPseudoRoot()
        p_cur = self._usd_prim
        while p_cur != root:
            p_cur = p_cur.GetParent()
            if p_cur.GetTypeName() in includes:
                list_.append(p_cur)
        return list_

    def get_children(self):
        return self._usd_prim.GetAllChildren()

    def create_child(self, name, type_name=''):
        return self.get_stage().DefinePrim(
            '{}/{}'.format(self.get_path(), name), type_name
        )

    def create_sibling(self, name, type_name=''):
        return self.get_stage().DefinePrim(
            '{}/{}'.format(self.get_parent_path(), name), type_name
        )

    def clear_children(self):
        state = self._usd_prim.GetStage()
        for i in self._usd_prim.GetAllChildren():
            state.RemovePrim(i.GetPath())

    def delete(self):
        self._usd_prim.GetStage().RemovePrim(self._usd_prim.GetPath())

    def get_descendants(self, type_includes=None):
        def rcs_fnc_(p_):
            _children = p_.GetChildren()
            for _i in _children:
                list_.append(_i)
                rcs_fnc_(_i)

        list_ = []
        rcs_fnc_(self._usd_prim)
        if isinstance(type_includes, list):
            return [i for i in list_ if i.GetTypeName() in type_includes]
        return list_

    def find_descendants(self, includes):
        return self.get_descendants(includes)

    def get_child_paths(self):
        return [i.GetPath().pathString for i in self._usd_prim.GetChildren()]

    def get_descendant_paths(self):
        def rcs_fnc_(list__, prim_):
            for _i_prim in prim_.GetChildren():
                list__.append(_i_prim.GetPath().pathString)
                rcs_fnc_(_i_prim)

        list_ = []
        rcs_fnc_(list_, self._usd_prim)
        return list_

    def get_variant_set(self, variant_set_name):
        return self._usd_prim.GetVariantSet(variant_set_name)

    def get_variant_sets(self):
        list_ = []
        usd_variant_sets = self._usd_prim.GetVariantSets()
        for i in usd_variant_sets.GetNames():
            i_variant_set = self._usd_prim.GetVariantSet(i)
            list_.append(
                i_variant_set
            )
        return list_

    def get_variant_names(self, variant_set_name):
        return UsdVariantSetOpt(self.get_variant_set(variant_set_name)).get_variant_names()

    def get_variant_dict(self):
        dic = collections.OrderedDict()
        for i in self.get_variant_sets():
            i_variant_set_opt = UsdVariantSetOpt(i)
            dic[i_variant_set_opt.get_name()] = (
                i_variant_set_opt.get_current_variant_name(),
                i_variant_set_opt.get_variant_names()
            )
        return dic

    @classmethod
    def _add_customize_attribute_(cls, usd_fnc, key, value):
        if isinstance(value, bool):
            dcc_type_name = unr_core.UnrType.CONSTANT_BOOLEAN
        elif isinstance(value, int):
            dcc_type_name = unr_core.UnrType.CONSTANT_INTEGER
        elif isinstance(value, float):
            dcc_type_name = unr_core.UnrType.CONSTANT_FLOAT
        elif isinstance(value, six.string_types):
            dcc_type_name = unr_core.UnrType.CONSTANT_STRING
        else:
            raise TypeError()
        #
        usd_type = usd_cor_configure.UsdTypes.MAPPER[dcc_type_name]
        p = usd_fnc.CreatePrimvar(
            key,
            usd_type
        )
        p.Set(value)

    def add_reference(self, file_path):
        self._usd_prim.GetReferences().AddReference(file_path)

    def add_payload(self, file_path):
        self._usd_prim.GetPayloads().AddPayload(file_path)

    def compute_world_b_box(self):
        b_box_cache = UsdGeom.BBoxCache(
            1,
            includedPurposes=[
                UsdGeom.Tokens.default_,
                UsdGeom.Tokens.render,
                UsdGeom.Tokens.proxy
            ],
            useExtentsHint=True,
            ignoreVisibility=True,
        )
        return b_box_cache.ComputeWorldBound(self._usd_prim)

    def compute_range_args(self):
        b_box = self.compute_world_b_box()
        r = b_box.GetRange()
        return r.GetMin(), r.GetMin()+r.GetSize()

    def compute_geometry_args(self):
        b_box = self.compute_world_b_box()
        r = b_box.GetRange()
        return r.GetMin(), r.GetMidpoint(), r.GetSize()

    def get_all_references(self):
        list_ = []
        _ = self._usd_prim.GetPrimStack()
        for i in _:
            list_.append(
                (
                    i.path.pathString, i.layer.realPath
                )
            )

        return list_

    def copy_form(self, usd_prim):
        pass

    def set_kind(self, kind):
        Usd.ModelAPI(self._usd_prim).SetKind(kind)

    def set_kind_as_subcomponent(self):
        self.set_kind(
            Kind.Tokens.subcomponent
        )

    def __str__(self):
        return '{}(path={})'.format(
            self.get_type_name(),
            self.get_path()
        )


class UsdVariantSetOpt(object):
    def __init__(self, usd_usd_variant):
        self._usd_usd_variant = usd_usd_variant

    @property
    def usd_instance(self):
        return self._usd_usd_variant

    def get_name(self):
        return self._usd_usd_variant.GetName()

    def get_variant_names(self):
        return self._usd_usd_variant.GetVariantNames()

    def get_current_variant_name(self):
        return self._usd_usd_variant.GetVariantSelection()


class UsdDataMapper(object):
    def __init__(self, dcc_type, dcc_value):
        self._dcc_type = dcc_type
        self._dcc_value = dcc_value

    def to_usd_args(self):
        key = self._dcc_type.category.name, self._dcc_type.name
        if key in usd_cor_configure.UsdTypes.MAPPER:
            usd_type = usd_cor_configure.UsdTypes.MAPPER[key]
            return usd_type, None
        return None, None


class UsdTransformOpt(UsdPrimOpt):
    def __init__(self, usd_prim):
        self._usd_prim = usd_prim
        super(UsdTransformOpt, self).__init__(usd_prim)
        self._usd_fnc = UsdGeom.Imageable(self._usd_prim)

    def create_customize_attribute(self, key, value):
        self._add_customize_attribute_(
            self._usd_fnc, key, value
        )

    def get_customize_attribute(self, key):
        p = self._usd_fnc.GetPrimvar(key)
        if p:
            return p.Get()

    def set_visible(self, boolean):
        p = self._usd_fnc.GetVisibilityAttr()
        if p:
            pass
        else:
            p = self._usd_fnc.CreateVisibilityAttr(
                UsdGeom.Tokens.inherited,
                True
            )
        #
        p.Set(
            UsdGeom.Tokens.inherited if boolean is True else UsdGeom.Tokens.invisible
        )


class UsdBase(object):
    @classmethod
    def to_integer_array(cls, usd_integer_array):
        return map(int, usd_integer_array)

    @classmethod
    def to_point_array(cls, usd_point_array):
        return map(tuple, usd_point_array)

    @classmethod
    def to_coord_array(cls, usd_coord_array):
        return map(tuple, usd_coord_array)

    @classmethod
    def to_matrix(cls, usd_matrix):
        list_ = []
        for row in usd_matrix:
            for column in row:
                list_.append(column)
        return list_

    @classmethod
    def to_usd_matrix(cls, matrix):
        list_ = []
        for i in range(4):
            rows = []
            for j in range(4):
                rows.append(matrix[i*4+j])
            list_.append(rows)
        #
        return Gf.Matrix4d(list_)


class UsdGeometryOpt(UsdPrimOpt):
    def __init__(self, usd_instance):
        if isinstance(usd_instance, Usd.Prim):
            self._usd_fnc = UsdGeom.Gprim(usd_instance)
            self._usd_prim = usd_instance
        else:
            self._usd_fnc = usd_instance
            self._usd_prim = usd_instance.GetPrim()
        super(UsdGeometryOpt, self).__init__(self._usd_prim)

    def create_customize_port(self, port_path, dcc_type, dcc_value):
        usd_type, usd_value = UsdDataMapper(dcc_type, dcc_value).to_usd_args()
        if usd_type is not None:
            p = self._usd_fnc.CreatePrimvar(
                port_path,
                usd_type
            )
            p.Set(dcc_value)

    def create_customize_port_(self, port_path, type_path, dcc_value):
        category_name, type_name = type_path.split(unr_core.UnrType.PATHSEP)
        key = category_name, type_name
        if key in usd_cor_configure.UsdTypes.MAPPER:
            usd_type = usd_cor_configure.UsdTypes.MAPPER[key]
            p = self._usd_fnc.CreatePrimvar(
                port_path,
                usd_type
            )
            p.Set(dcc_value)

    def create_customize_port_as_face_color(self, port_path, type_path, usd_value):
        category_name, type_name = type_path.split(unr_core.UnrType.PATHSEP)
        key = category_name, type_name
        if key in usd_cor_configure.UsdTypes.MAPPER:
            usd_type = usd_cor_configure.UsdTypes.MAPPER[key]
            p = self._usd_fnc.CreatePrimvar(
                port_path,
                usd_type,
                UsdGeom.Tokens.uniform
            )
            p.Set(usd_value)

    def set_visible(self, boolean):
        p = self._usd_fnc.GetVisibilityAttr()
        if not p:
            p = self._usd_fnc.CreateVisibilityAttr(
                UsdGeom.Tokens.inherited,
                True
            )
        #
        p.Set(
            UsdGeom.Tokens.inherited if boolean is True else UsdGeom.Tokens.invisible
        )

    def create_primvar_as_point_as_uniform(self, port_path, values):
        p = self._usd_fnc.GetPrimvar(port_path)
        if not p:
            p = self._usd_fnc.CreatePrimvar(
                port_path,
                Sdf.ValueTypeNames.Point3dArray,
                UsdGeom.Tokens.uniform
            )

        p.Set(Vt.Vec3fArray(values))

    def create_primvar_as_float_as_uniform(self, port_path, values):
        p = self._usd_fnc.GetPrimvar(port_path)
        if not p:
            p = self._usd_fnc.CreatePrimvar(
                port_path,
                Sdf.ValueTypeNames.FloatArray,
                UsdGeom.Tokens.uniform
            )

        p.Set(Vt.FloatArray(values))

    def create_primvar_as_integer_as_uniform(self, port_path, values):
        p = self._usd_fnc.GetPrimvar(port_path)
        if not p:
            p = self._usd_fnc.CreatePrimvar(
                port_path,
                Sdf.ValueTypeNames.IntArray,
                UsdGeom.Tokens.uniform
            )

        p.Set(Vt.IntArray(values))

    def set_display_colors(self, colors):
        p = self._usd_fnc.GetDisplayColorPrimvar()
        if not p:
            p = self._usd_fnc.CreateDisplayColorPrimvar(
                UsdGeom.Tokens.constant
            )

        if not isinstance(colors, Vt.Vec3fArray):
            colors = Vt.Vec3fArray(colors)

        p.Set(colors)

    def get_display_colors(self):
        p = self._usd_fnc.GetDisplayColorPrimvar()
        if not p:
            p = self._usd_fnc.CreateDisplayColorPrimvar(
                UsdGeom.Tokens.constant
            )
        return p.Get()

    def fill_display_color(self, color):
        p = self._usd_fnc.GetDisplayColorPrimvar()
        if p is None:
            p = self._usd_fnc.CreateDisplayColorPrimvar(
                UsdGeom.Tokens.constant
            )
        r, g, b = color
        p.Set(
            Vt.Vec3fArray([(r, g, b)])
        )

    def set_purpose_as_proxy(self):
        p = self._usd_fnc.GetPurposeAttr()
        if not p:
            p = self._usd_fnc.CreatePurposeAttr()

        p.Set(UsdGeom.Tokens.proxy)

    def set_display_colors_as_uniform(self, values):
        usd_fnc = UsdGeom.Gprim(self._usd_prim)
        p = usd_fnc.GetDisplayColorPrimvar()
        if not p:
            p = usd_fnc.CreateDisplayColorPrimvar(
                UsdGeom.Tokens.uniform
            )
        else:
            p.SetInterpolation(
                UsdGeom.Tokens.uniform
            )

        p.Set(values)

    def set_normals_as_uniform(self, values):
        usd_fnc = UsdGeom.PointBased(self._usd_prim)
        p = usd_fnc.GetNormalsAttr()
        if not p:
            p = usd_fnc.CreateNormalsAttr(
                UsdGeom.Tokens.uniform
            )
        else:
            usd_fnc.SetNormalsInterpolation(
                UsdGeom.Tokens.uniform
            )

        p.Set(values)


class UsdInstancerOpt(UsdGeometryOpt):
    def __init__(self, usd_prim):
        super(UsdInstancerOpt, self).__init__(usd_prim)
        self._usd_fnc = UsdGeom.PointInstancer(self._usd_prim)

    def get_proto_prims(self):
        return map(
            lambda x: self._usd_prim.GetStage().GetPrimAtPath(x),
            self._usd_fnc.GetPrototypesRel().GetForwardedTargets()
        )

    def clear_proto(self):
        self._usd_fnc.GetPrototypesRel().BlockTargets()

    def set_proto_prims(self, prims):
        for i in prims:
            self._usd_fnc.GetPrototypesRel().AddTarget(i.GetPath())

    def get_positions(self):
        p = self._usd_fnc.GetPositionsAttr()
        if p:
            return p.Get()

    def set_positions(self, values):
        p = self._usd_fnc.GetPositionsAttr()
        if not p:
            p = self._usd_fnc.CreatePositionsAttr()
        p.Set(values)

    def get_orientations(self):
        p = self._usd_fnc.GetOrientationsAttr()
        if p:
            return p.Get()

    def set_orientations(self, values):
        p = self._usd_fnc.GetOrientationsAttr()
        if not p:
            p = self._usd_fnc.CreateOrientationsAttr()
        p.Set(values)

    def get_scales(self):
        p = self._usd_fnc.GetScalesAttr()
        if p:
            return p.Get()

    def set_scales(self, values):
        p = self._usd_fnc.GetScalesAttr()
        if not p:
            p = self._usd_fnc.CreateScalesAttr()
        p.Set(values)

    def get_proto_indices(self):
        p = self._usd_fnc.GetProtoIndicesAttr()
        if p:
            return p.Get()

    def set_proto_indices(self, values):
        p = self._usd_fnc.GetProtoIndicesAttr()
        if not p:
            p = self._usd_fnc.CreateProtoIndicesAttr()
        p.Set(values)


class UsdGeometryMeshOpt(UsdGeometryOpt):
    def __init__(self, usd_prim):
        super(UsdGeometryMeshOpt, self).__init__(usd_prim)
        self._usd_fnc = UsdGeom.Mesh(self._usd_prim)

    def get_points(self):
        p = self._usd_fnc.GetPointsAttr()
        if p.GetNumTimeSamples():
            return p.Get(0)
        return p.Get()

    def get_point_count(self):
        return len(self.get_points())

    def get_face_vertex_counts(self):
        usd_mesh = self._usd_fnc
        a = usd_mesh.GetFaceVertexCountsAttr()
        if a.GetNumTimeSamples():
            v = a.Get(0)
        else:
            v = a.Get()
        if v:
            return UsdBase.to_integer_array(v)
        return []

    def get_face_vertex_indices(self):
        a = self._usd_fnc.GetFaceVertexIndicesAttr()
        if a.GetNumTimeSamples():
            v = a.Get(0)
        else:
            v = a.Get()
        if v:
            return UsdBase.to_integer_array(v)
        return []

    def get_uv_map_names(self):
        list_ = []
        usd_mesh = self._usd_fnc
        usd_primvars = usd_mesh.GetAuthoredPrimvars()
        for i_p in usd_primvars:
            i_name = i_p.GetPrimvarName()
            i_a = self._usd_prim.GetAttribute('primvars:{}'.format(i_name))
            if i_a.GetNumTimeSamples():
                i_v = i_p.GetIndices(0)
            else:
                i_v = i_p.GetIndices()
            if i_v:
                list_.append(i_name)
        return list_

    def get_uv_map(self, uv_map_name):
        p = self._usd_fnc.GetPrimvar(uv_map_name)
        a = self._usd_prim.GetAttribute('primvars:{}'.format(uv_map_name))
        uv_face_vertex_counts = self.get_face_vertex_counts()
        if a.GetNumTimeSamples():
            uv_face_vertex_indices = p.GetIndices(0)
            uv_map_coords = p.Get(0)
        else:
            uv_face_vertex_indices = p.GetIndices()
            uv_map_coords = p.Get()
        return uv_face_vertex_counts, uv_face_vertex_indices, uv_map_coords

    def get_uv_map_coords(self, uv_map_name):
        p = self._usd_fnc.GetPrimvar(uv_map_name)
        a = self._usd_prim.GetAttribute('primvars:{}'.format(uv_map_name))
        if a.GetNumTimeSamples():
            return p.Get(0)
        return p.Get()

    def get_uv_map_face_vertex_indices(self, uv_map_name):
        p = self._usd_fnc.GetPrimvar(uv_map_name)
        a = self._usd_prim.GetAttribute('primvars:{}'.format(uv_map_name))
        if a.GetNumTimeSamples():
            return p.GetIndices(0)
        return p.GetIndices()

    def get_uv_maps(self):
        dic = {}
        uv_map_names = self.get_uv_map_names()
        for i_uv_map_name in uv_map_names:
            uv_map = self.get_uv_map(i_uv_map_name)
            dic[i_uv_map_name] = uv_map
        return dic


class AbsUsdMeshOptDef(UsdGeometryOpt):
    def __init__(self, *args):
        super(AbsUsdMeshOptDef, self).__init__(*args)
        self._usd_fnc = UsdGeom.Mesh(self._usd_prim)

    def get_path(self):
        return self._usd_prim.GetPath().pathString

    def get_face_count(self):
        usd_mesh = self._usd_fnc
        return usd_mesh.GetFaceCount()

    def get_face_vertices(self):
        return self.get_face_vertex_counts(), self.get_face_vertex_indices()

    def get_face_vertex_counts(self):
        a = self._usd_fnc.GetFaceVertexCountsAttr()
        if a.GetNumTimeSamples():
            return a.Get(0)
        return a.Get()

    def get_face_vertex_indices(self):
        usd_mesh = self._usd_fnc
        a = usd_mesh.GetFaceVertexIndicesAttr()
        if a.GetNumTimeSamples():
            return a.Get(0)
        return a.Get()

    def get_uv_map_names(self):
        list_ = []
        usd_primvars = self._usd_fnc.GetAuthoredPrimvars()
        for uv_primvar in usd_primvars:
            uv_map_name = uv_primvar.GetPrimvarName()
            if uv_primvar.GetIndices():
                list_.append(uv_map_name)
        return list_

    def get_uv_map(self, uv_map_name):
        uv_primvar = self._usd_fnc.GetPrimvar(uv_map_name)
        if uv_primvar:
            uv_face_vertex_indices = uv_primvar.GetIndices()
            uv_coords = uv_primvar.Get()
            return uv_face_vertex_indices, uv_coords


class ImageOpt(object):
    def __init__(self, file_path):
        from PIL import Image

        self.__is_udim = bsc_storage.StgTextureMtd.get_is_udim(file_path)

        unit_args = bsc_storage.StgTextureMtd.get_udim_region_args(file_path)
        if not unit_args:
            raise RuntimeError()

        self.__image_data = {}
        for i_path, i_region in unit_args:
            i_pil_image = Image.open(i_path)
            i_w, i_h = i_pil_image.size
            i_w_m, i_h_m = i_w-1, i_h-1
            self.__image_data[i_region] = i_pil_image, i_w_m, i_h_m

    @classmethod
    def get_uv_region(cls, u, v):
        if u > 9:
            raise RuntimeError()
        if v > 9:
            raise RuntimeError()
        return '10{}{}'.format(int(v), int(u)+1)

    @classmethod
    def get_rgb_at_pixel(cls, pil_image, x, y, maximum=255):
        r, g, b = pil_image.getpixel((x, y))
        if maximum == 255:
            return r, g, b
        return r/255.0, g/255.0, b/255.0

    def get_rgb_at_coord(self, u, v, maximum=255):
        if self.__is_udim is True:
            region = self.get_uv_region(u, v)
            _ = self.__image_data.get(region)
            if _:
                pil_image, w_m, h_m = _
                x, y = int((u-int(u))*w_m), int((v-int(v))*h_m)
                return self.get_rgb_at_pixel(pil_image, x, y, maximum)
            return 0, 0, 0

        pil_image, w_m, h_m = self.__image_data['1001']
        x, y = int(u*w_m), int(v*h_m)
        return self.get_rgb_at_pixel(pil_image, x, y, maximum)


class NpKDTree(object):
    def __init__(self, points):
        import numpy as np

        from scipy.spatial import KDTree

        l_s = len(points)/100
        l_s = max(10, l_s)

        self._kd_tree = KDTree(
            np.array(points),
            # leafsize=l_s
        )
        self._np_array_fnc = np.array

    def compute_closed_index(self, point):
        """
    print NpKDTree(
        [(0, 1, 0), (0, 2, 0), (0, 3, 0)]
    ).get_closed_point(
        (0, 2.15, 0)
    )
        """
        return self._kd_tree.query(self._np_array_fnc(list(point)))[1]

    def compute_closed_mapper(self, points):
        return self._kd_tree.query(self._np_array_fnc(points))

    def compute_closed_indexes(self, points, distance_tolerance=None):
        if isinstance(distance_tolerance, (int, float)):
            _ = self._kd_tree.query(
                self._np_array_fnc(points),
                eps=distance_tolerance,
                distance_upper_bound=distance_tolerance
            )
            return [i_index if i_distance <= distance_tolerance else None for i_distance, i_index in zip(*_)]
        _ = self._kd_tree.query(self._np_array_fnc(points))
        return _[1]

    @staticmethod
    def compute_fnc(data):
        points, check_points = data
        kd_tree = NpKDTree(points)
        return kd_tree.compute_closed_indexes(check_points)


class NpBBoxRange(object):
    def __init__(self, minimum, maximum):
        import numpy as np

        self._minimum = np.array(minimum)
        self._maximum = np.array(maximum)

        self._np_array_fnc = np.array
        self._np_all_fnc = np.all
        self._np_where_fnc = np.where

    def compute_contain_points(self, points):
        np_points = self._np_array_fnc(points)
        return np_points[
            self._np_all_fnc(
                (np_points >= self._minimum) & (np_points <= self._maximum), axis=1
            )
        ]

    def compute_contain_elements(self, points):
        element_dict = {_index: _point for _index, _point in enumerate(points)}
        return [element_dict[i] for i in self.compute_contain_indices(points)]

    def compute_contain_indices(self, points):
        np_points = self._np_array_fnc(points)
        return self._np_where_fnc(
            self._np_all_fnc(
                (np_points >= self._minimum) & (np_points <= self._maximum), axis=1
            )
        )[0]


class UsdMeshOpt(UsdGeometryOpt):

    def __init__(self, *args):
        super(UsdMeshOpt, self).__init__(*args)
        self._usd_fnc = UsdGeom.Mesh(self._usd_prim)
        #
        self.__cache = dict()

    def create(self, face_vertex_counts, face_vertex_indices, points):
        self.set_face_vertices(face_vertex_counts, face_vertex_indices)
        self.set_points(points)

    def get_path(self):
        return self._usd_prim.GetPath().pathString

    def get_face_count(self):
        usd_mesh = self._usd_fnc
        return usd_mesh.GetFaceCount()

    def get_face_vertices(self):
        return self.get_face_vertex_counts(), self.get_face_vertex_indices()

    def set_face_vertices(self, face_vertex_counts, face_vertex_indices):
        self.set_face_vertex_counts(face_vertex_counts)
        self.set_face_vertex_indices(face_vertex_indices)

    def get_face_vertex_counts(self):
        p = self._usd_fnc.GetFaceVertexCountsAttr()
        if p.GetNumTimeSamples():
            return p.Get(0)
        return p.Get()

    def set_face_vertex_counts(self, values):
        p = self._usd_fnc.GetFaceVertexCountsAttr()
        if not p:
            p.CreateFaceVertexCountsAttr()
        p.Set(values)

    def get_face_vertex_indices(self):
        usd_mesh = self._usd_fnc
        a = usd_mesh.GetFaceVertexIndicesAttr()
        if a.GetNumTimeSamples():
            return a.Get(0)
        return a.Get()

    def set_face_vertex_indices(self, values):
        p = self._usd_fnc.GetFaceVertexIndicesAttr()
        if not p:
            p.CreateFaceVertexIndicesAttr()
        p.Set(values)

    def get_uv_map_names(self):
        list_ = []
        usd_primvars = self._usd_fnc.GetAuthoredPrimvars()
        for uv_primvar in usd_primvars:
            uv_map_name = uv_primvar.GetPrimvarName()
            if uv_primvar.GetIndices():
                list_.append(uv_map_name)
        return list_

    def get_uv_map(self, uv_map_name):
        uv_primvar = self._usd_fnc.GetPrimvar(uv_map_name)
        if uv_primvar:
            uv_face_vertex_indices = uv_primvar.GetIndices()
            uv_coords = uv_primvar.Get()
            return uv_face_vertex_indices, uv_coords

    def _create_uv_map_name_(self, uv_map_name):
        if self._usd_fnc.HasPrimvar(uv_map_name) is True:
            return self._usd_fnc.GetPrimvar(uv_map_name)
        return self._usd_fnc.CreatePrimvar(
            uv_map_name,
            Sdf.ValueTypeNames.TexCoord2fArray,
            UsdGeom.Tokens.faceVarying
        )

    def _get_primvar_(self, primvar_name):
        if self._usd_fnc.HasPrimvar(primvar_name) is True:
            return self._usd_fnc.GetPrimvar(primvar_name)
        return self._usd_fnc.CreatePrimvar(
            primvar_name,
            Sdf.ValueTypeNames.TexCoord2fArray,
            UsdGeom.Tokens.faceVarying
        )

    def create_uv_map(self, uv_map_name, uv_map):
        if uv_map_name == 'map1':
            uv_map_name = 'st'
        primvar = self._create_uv_map_name_(uv_map_name)
        uv_face_vertex_indices, uv_coords = uv_map
        primvar.Set(uv_coords)
        primvar.SetIndices(Vt.IntArray(uv_face_vertex_indices))

    def assign_uv_map(self, uv_map_name, uv_map):
        primvar = self._usd_fnc.GetPrimvar(uv_map_name)
        indices, values = uv_map
        primvar.Set(values)
        primvar.SetIndices(Vt.IntArray(indices))

    def set_display_colors_as_vertex(self, color_map):
        p = self._usd_fnc.GetDisplayColorPrimvar()
        if not p:
            p = self._usd_fnc.CreateDisplayColorPrimvar(
                UsdGeom.Tokens.faceVarying
            )
        else:
            p.SetInterpolation(UsdGeom.Tokens.faceVarying)

        indices, values = color_map
        p.Set(values)
        p.SetIndices(
            Vt.IntArray(indices)
        )

    def get_colors_fom_shell(self, offset=0, seed=0):
        vertex_counts, vertex_indices = self.get_face_vertices()
        face_to_shell_dict = bsc_core.DccMeshFaceShellOpt(vertex_counts, vertex_indices).generate()
        max_shell_index = max(face_to_shell_dict.values())
        choice_colors = bsc_core.RawColorMtd.get_choice_colors(
            count=max_shell_index+1, maximum=1.0, offset=offset, seed=seed
        )
        colors = []
        c = len(vertex_counts)
        for i in range(c):
            i_shell_index = face_to_shell_dict[i]
            i_rgb = choice_colors[i_shell_index]
            colors.append(i_rgb)
        return Vt.Vec3fArray(colors)

    def get_points(self):
        p = self._usd_fnc.GetPointsAttr()
        if p.GetNumTimeSamples():
            return p.Get(0)
        return p.Get()

    def set_points(self, values):
        p = self._usd_fnc.GetPointsAttr()
        if not p:
            p.CreatePointsAttr()
        p.Set(values)

    def get_point_count(self):
        return len(self.get_points())

    def get_radius(self, pivot):
        o_x, o_y, o_z = pivot
        points = self.get_points()
        set_ = set()
        for i_point in points:
            i_x, i_y, i_z = i_point
            i_r = abs(math.sqrt((i_x+o_x)**2+(i_z+o_z)**2))
            set_.add(i_r)
        return max(set_)

    def compute_vertex_color_map_from_uv_coord(self, uv_map_name):
        uv_map = self.get_uv_map(uv_map_name)
        if uv_map:
            colors = []
            uv_vertex_indices, uv_coords = uv_map
            c = len(uv_coords)
            for i in range(c):
                if i <= c:
                    i_x, i_y = uv_coords[i]
                    i_rgb = (i_x-int(i_x)%1, i_y-int(i_y)%1, 0)
                else:
                    i_rgb = (0, 0, 1)
                #
                colors.append(i_rgb)
            return uv_vertex_indices, Vt.Vec3fArray(colors)

    def compute_vertex_color_map_from_image(self, file_path, uv_map_name):
        uv_map = self.get_uv_map(uv_map_name)
        if uv_map:
            colors = []
            uv_face_vertex_indices, uv_coords = uv_map
            image_opt = ImageOpt(file_path)
            c = len(uv_coords)
            for i in range(c):
                i_u, i_v = uv_coords[i]
                i_rgb = image_opt.get_rgb_at_coord(i_u, i_v, maximum=1.0)
                colors.append(i_rgb)
            return uv_face_vertex_indices, Vt.Vec3fArray(colors)

    def compute_face_points(self):
        key = 'face_points'
        if key in self.__cache:
            return self.__cache[key]

        face_vertex_counts = self.get_face_vertex_counts()
        face_vertex_indices = self.get_face_vertex_indices()
        points = self.get_points()

        list_ = []
        index_cur = 0
        for i_count in face_vertex_counts:
            i_indices = face_vertex_indices[index_cur:index_cur+i_count]
            i_points = [points[i] for i in i_indices]
            # i_c = Gf.Vec3f(0, 0, 0)

            i_point_center = sum(i_points, Gf.Vec3f()) / i_count
            list_.append(i_point_center)

            index_cur += i_count

        face_points = Vt.Vec3fArray(list_)
        self.__cache[key] = face_points
        return face_points

    def compute_face_colors_from_image(self, file_path, uv_map_name):
        image_opt = ImageOpt(file_path)
        face_extra = self.generate_face_extra(uv_map_name)
        face_points = self.compute_face_points()
        colors = []
        for i_face_index, i_point in enumerate(face_points):
            i_coord = face_extra.compute_uv_coord_at(i_face_index, i_point)
            if i_coord:
                i_u, i_v = i_coord
                i_rgb = image_opt.get_rgb_at_coord(i_u, i_v, maximum=1.0)
                colors.append(i_rgb)
            else:
                colors.append((0, 0, 0))
        return Vt.Vec3fArray(colors)

    def generate_face_points_kd_tree(self):
        key = 'face_points_kd_tree'
        if key in self.__cache:
            return self.__cache[key]

        face_points = self.compute_face_points()
        kd_tree = NpKDTree(face_points)
        bsc_log.Log.debug('generator KDTree: "{}"'.format(self.get_path()))
        self.__cache[key] = kd_tree
        return kd_tree

    def generate_b_box_range(self):
        key = 'b_box_range'
        if key in self.__cache:
            return self.__cache[key]

        b_box = self.compute_world_b_box()
        r = b_box.GetRange()
        minimum, maximum = r.GetMin(), r.GetMax()
        b_box_range = NpBBoxRange(minimum, maximum)
        self.__cache[key] = b_box_range
        return b_box_range

    def compute_face_normals(self):
        key = 'face_normals'
        if key in self.__cache:
            return self.__cache[key]

        face_vertex_counts = self.get_face_vertex_counts()
        face_vertex_indices = self.get_face_vertex_indices()
        points = self.get_points()

        list_ = []
        index_cur = 0
        for i_count in face_vertex_counts:
            i_indices = face_vertex_indices[index_cur:index_cur+i_count]
            i_v_0, i_v_1, i_v_2 = [points[i] for i in i_indices[:3]]

            i_v_n_0 = i_v_1-i_v_0
            i_v_n_1 = i_v_2-i_v_0

            i_normal = i_v_n_0 ^ i_v_n_1
            i_normal.Normalize()
            list_.append(i_normal)

            index_cur += i_count

        face_normals = Vt.Vec3fArray(list_)
        self.__cache[key] = face_normals
        return face_normals

    def generate_face_query(self):
        key = 'face_query'
        if key in self.__cache:
            return self.__cache[key]
        face_query = MeshFaceQuery(self)
        self.__cache[key] = face_query
        return face_query

    def generate_face_uv_query(self, uv_map_name):
        return MeshFaceUvQuery(self, uv_map_name)

    def generate_face_extra(self, uv_map_name):
        key = 'face_extra.{}'.format(uv_map_name)
        if key in self.__cache:
            return self.__cache[key]
        face_extra = MeshFaceExtra(self, uv_map_name)
        self.__cache[key] = face_extra
        return face_extra


class MeshFaceQuery(object):
    def __init__(self, mesh_opt):
        if not isinstance(mesh_opt, UsdMeshOpt):
            raise TypeError()

        self._mesh_opt = mesh_opt
        (
            self._count_mapper, self._indices_mapper, self._points_mapper,
        ) = self.__generate_mapper()

    def __generate_mapper(self):
        count_mapper = {}
        indices_mapper = {}
        points_mapper = {}
        face_vertex_counts = self._mesh_opt.get_face_vertex_counts()
        face_vertex_indices = self._mesh_opt.get_face_vertex_indices()
        points = self._mesh_opt.get_points()
        index_cur = 0
        for i_face_index, i_face_count in enumerate(face_vertex_counts):
            count_mapper[i_face_index] = i_face_count
            i_vertex_indices = face_vertex_indices[index_cur:index_cur+i_face_count]
            indices_mapper[i_face_index] = i_vertex_indices
            points_mapper[i_face_index] = [points[i] for i in i_vertex_indices]

            index_cur += i_face_count
        return count_mapper, indices_mapper, points_mapper

    def get_count_at(self, face_index):
        return self._count_mapper[face_index]

    def get_indices_at(self, face_index):
        return self._indices_mapper[face_index]

    def get_points_at(self, face_index):
        return self._points_mapper[face_index]


class MeshFaceUvQuery(object):
    def __init__(self, mesh_opt, uv_map_name):
        if not isinstance(mesh_opt, UsdMeshOpt):
            raise TypeError()

        self._mesh_opt = mesh_opt
        (
            self._face_uv_indices_mapper, self._face_uv_coords_mapper,
            self._vertex_uv_index_mapper, self._vertex_uv_coord_mapper
        ) = self.__generate_mapper(
            uv_map_name
        )

    def __generate_mapper(self, uv_map_name):
        face_uv_indices_mapper = {}
        face_uv_coords_mapper = {}
        vertex_uv_index_mapper = {}
        vertex_uv_coord_mapper = {}
        uv_map = self._mesh_opt.get_uv_map(uv_map_name)
        if uv_map:
            face_vertex_counts = self._mesh_opt.get_face_vertex_counts()
            face_vertex_indices = self._mesh_opt.get_face_vertex_indices()
            uv_face_vertex_indices, uv_coords = uv_map
            index_cur = 0
            for i_face_index, i_face_count in enumerate(face_vertex_counts):
                i_vertex_indices = face_vertex_indices[index_cur:index_cur+i_face_count]
                i_uv_indices = uv_face_vertex_indices[index_cur:index_cur+i_face_count]
                face_uv_indices_mapper[i_face_index] = i_uv_indices
                # ignore when uv indices is not found
                if i_uv_indices is not None:
                    # ignore when uv indices count is less than face count
                    if len(i_uv_indices) == i_face_count:
                        i_uv_coords = []
                        for j_seq, j_uv_index in enumerate(i_vertex_indices):
                            j_uv_index = i_uv_indices[j_seq]
                            vertex_uv_index_mapper[j_uv_index] = j_uv_index
                            j_coord = uv_coords[j_uv_index]
                            vertex_uv_coord_mapper[j_uv_index] = j_coord
                            i_uv_coords.append(j_coord)
                        face_uv_coords_mapper[i_face_index] = i_uv_coords

                index_cur += i_face_count
        return face_uv_indices_mapper, face_uv_coords_mapper, vertex_uv_index_mapper, vertex_uv_coord_mapper

    def get_index_at(self, vertex_index):
        if vertex_index in self._vertex_uv_index_mapper:
            return self._vertex_uv_index_mapper.get(vertex_index)

    def get_coord_at(self, vertex_index):
        if vertex_index in self._vertex_uv_coord_mapper:
            return self._vertex_uv_coord_mapper.get(vertex_index)

    def get_indices_at(self, face_index):
        if face_index in self._face_uv_indices_mapper:
            return self._face_uv_indices_mapper[face_index]

    def get_coords_at(self, face_index):
        if face_index in self._face_uv_coords_mapper:
            return self._face_uv_coords_mapper[face_index]


class MeshFaceExtra(object):
    def __init__(self, mesh_opt, uv_map_name):
        if not isinstance(mesh_opt, UsdMeshOpt):
            raise TypeError()

        self._mesh_opt = mesh_opt

        self._mesh_face_query = self._mesh_opt.generate_face_query()
        self._mesh_face_uv_query = self._mesh_opt.generate_face_uv_query(uv_map_name)

        face_points, face_normals = self.__generate_mapper()
        self._face_point_dict = {_index: _point for _index, _point in enumerate(face_points)}
        self._face_normal_dict = {_index: _point for _index, _point in enumerate(face_normals)}

    def __generate_mapper(self):
        return self._mesh_opt.compute_face_points(), self._mesh_opt.compute_face_normals()

    def compute_project_point_at(self, face_index, point):
        face_point = self._face_point_dict[face_index]
        face_normal = self._face_normal_dict[face_index]
        plane = Gf.Plane(
            Gf.Vec3d(face_normal),
            Gf.Vec3d(face_point)
        )

        project_point = plane.Project(Gf.Vec3d(point))
        return Gf.Vec3f(project_point)

    def compute_uv_coord_at(self, face_index, point):
        face_point = self._face_point_dict[face_index]
        face_normal = self._face_normal_dict[face_index]
        plane = Gf.Plane(
            Gf.Vec3d(face_normal),
            Gf.Vec3d(face_point)
        )

        project_point = plane.Project(Gf.Vec3d(point))
        project_point = Gf.Vec3f(project_point)

        points = self._mesh_face_query.get_points_at(face_index)
        uv_coords = self._mesh_face_uv_query.get_coords_at(face_index)
        if uv_coords:
            lengths = map(lambda _x: (project_point-_x).GetLength(), points)
            lengths_ = map(lambda _x: 1/_x if _x != 0 else 1, lengths)
            lengths_all_ = sum(lengths_)
            percents = map(lambda _x: _x/lengths_all_, lengths_)
            return (
                sum(map(lambda _x: _x[0][0]*_x[1], zip(uv_coords, percents))),
                sum(map(lambda _x: _x[0][1]*_x[1], zip(uv_coords, percents)))
            )


class UsdNurbsCurvesOpt(object):
    def __init__(self, usd_fnc):
        pass


class UsdPointsOpt(UsdGeometryOpt):
    def __init__(self, *args):
        super(UsdPointsOpt, self).__init__(*args)
        self._usd_fnc = UsdGeom.Points(self._usd_prim)

    def set_points(self, values):
        usd_fnc = self._usd_fnc
        p = usd_fnc.GetPointsAttr()
        if p is None:
            p = usd_fnc.CreatePointsAttr()
        p.Set(values)

    def set_widths(self, values):
        usd_fnc = self._usd_fnc
        p = usd_fnc.GetWidthsAttr()
        if p is None:
            p = usd_fnc.CreateWidthsAttr()
        p.Set(values)

    def set_width_as_vertex(self, values):
        usd_fnc = self._usd_fnc
        p = usd_fnc.GetWidthsAttr()
        if p is None:
            p = usd_fnc.CreateWidthsAttr(UsdGeom.Tokens.varying)
        else:
            usd_fnc.SetWidthsInterpolation(UsdGeom.Tokens.varying)
        p.Set(values)

    def set_display_colors_as_vertex(self, values):
        usd_fnc = UsdGeom.Gprim(self._usd_prim)
        p = usd_fnc.GetDisplayColorPrimvar()
        if not p:
            p = usd_fnc.CreateDisplayColorPrimvar(
                UsdGeom.Tokens.varying
            )
        else:
            p.SetInterpolation(
                UsdGeom.Tokens.varying
            )

        p.Set(values)


class UsdBasisCurvesOpt(UsdGeometryOpt):
    def __init__(self, usd_prim):
        super(UsdBasisCurvesOpt, self).__init__(usd_prim)
        self._usd_fnc = UsdGeom.BasisCurves(self._usd_prim)

    def create(self, counts, points, widths):
        self.set_curve_basis(
            UsdGeom.Tokens.catmullRom
        )
        self.set_curve_type(
            UsdGeom.Tokens.cubic
        )
        self.set_curve_vertex_counts(counts)
        self.set_points(points)
        self.set_widths(widths)

    def create_by_points_and_normals(self, points, normals):
        c_counts = []
        c_points = []
        c_widths = []
        c_colors = []
        for i_p, i_n in zip(points, normals):
            i_p_1 = i_p + i_n
            i_points = [i_p, i_p, i_p_1, i_p_1]
            c_counts.append(len(i_points))
            c_points.extend(i_points)
            c_widths.append(0.003)
            c_colors.append(i_n)

        self.create(c_counts, c_points, c_widths)
        self.set_display_colors_as_uniform(c_colors)

    def set_curve_type(self, value):
        usd_fnc = self._usd_fnc
        p = usd_fnc.GetTypeAttr()
        if p is not None:
            p = usd_fnc.CreateTypeAttr()
        p.Set(value)

    def set_curve_basis(self, value):
        usd_fnc = self._usd_fnc
        p = usd_fnc.GetBasisAttr()
        if p is not None:
            p = usd_fnc.CreateBasisAttr()
        p.Set(value)

    def set_curve_vertex_counts(self, values):
        usd_fnc = self._usd_fnc
        p = usd_fnc.GetCurveVertexCountsAttr()
        if p is None:
            p = usd_fnc.CreateCurveVertexCountsAttr()
        p.Set(values)

    def set_points(self, values):
        usd_fnc = self._usd_fnc
        p = usd_fnc.GetPointsAttr()
        if p is None:
            p = usd_fnc.CreatePointsAttr()
        p.Set(values)

    def get_points(self):
        usd_fnc = self._usd_fnc
        p = usd_fnc.GetPointsAttr()
        if p.GetNumTimeSamples():
            return p.Get(0)
        return p.Get()

    def set_widths(self, values):
        usd_fnc = self._usd_fnc
        p = usd_fnc.GetWidthsAttr()
        if p is None:
            p = usd_fnc.CreateWidthsAttr()
        p.Set(values)


class UsdMatrix(object):
    def __init__(self, usd_matrix):
        self._usd_fnc = usd_matrix

    @staticmethod
    def __to_angle(usd_matrix):
        x, y, z = usd_matrix.ExtractRotation().GetQuat().GetImaginary()
        return Gf.Vec3d(x*360.0/math.pi, y*360.0/math.pi, z*360.0/math.pi)

    def to_transformation(self):
        """
if __name__ == '__main__':
    print UsdMatrix(
        Gf.Matrix4d(
            [
                (4.92403876506104, 0.0, -0.8682408883346516, 0.0),
                (0.0, 5.0, 0.0, 0.0),
                (0.8682408883346516, 0.0, 4.92403876506104, 0.0),
                (0.0, 10.0, 0.0, 1.0)
            ]
        )
    ).to_transformation()

    print UsdMatrix(
        Gf.Matrix4d(
            [
                (4.990105983120342, 0.2615203729623543, -0.1744974835125049, 0.0),
                (-0.2585986987282574, 4.992546577171016, 0.08720887451415081, 0.0),
                (0.178798742284776, -0.07801134086531315, 4.996193074777413, 0.0),
                (0.0, 10.0, 0.0, 1.0)
            ]

        )
    ).to_transformation()

        """
        _, r, s, u, t, p = self._usd_fnc.Factor()
        transform = t
        rotate = self.__to_angle(u)
        scale = s
        return transform, rotate, scale


class UsdRotation(object):
    def __init__(self, *args):
        self._usd_fnc = args[0]

    def to_axis(self):
        return self._usd_fnc.GetAngle()

    def to_angle(self):
        return self._usd_fnc.GetAxis()


class UsdQuaternion(object):
    def __init__(self, *args):
        _ = args[0]
        if isinstance(_, Gf.Quath):
            self._usd_fnc = _
        elif isinstance(_, (tuple, list)):
            # w, (x, y, z)
            self._usd_fnc = Gf.Quath(_[0], _[1:])
        else:
            raise RuntimeError()

    def to_axis(self):
        return Gf.Rotation(self._usd_fnc).GetAxis()

    def to_angle(self):
        return Gf.Rotation(self._usd_fnc).GetAngle()

    def to_rotate(self):
        """
if __name__ == '__main__':
    print UsdQuaternion(
        (0.731934, 0.0433655, -0.679688, 0.00678253)
    ).to_rotate()
        """
        x, y, z = self._usd_fnc.GetImaginary()
        return Gf.Vec3d(x*360.0/math.pi, y*360.0/math.pi, z*360.0/math.pi)


class UsdBBox(object):
    def __init__(self, *args):
        self._usd_fnc = args[0]

    def to_size(self):
        return self._usd_fnc.GetSize()


class UsdTransformation(object):
    def __init__(self, translate, orientation, scale):
        self._translate = Gf.Vec3d(translate)
        self._orientation = orientation
        self._scale = Gf.Vec3d(scale)

    def to_matrix(self):
        m_t = Gf.Matrix4d()
        m_t.SetTranslate(self._translate)
        m_r = Gf.Matrix4d()
        m_r.SetRotate(self._orientation)
        m_s = Gf.Matrix4d()
        m_s.SetScale(self._scale)
        m_t_0 = Gf.Matrix4d()
        m_t_0.SetTranslate(self._translate*-1)
        return m_t_0*m_r*m_s*m_t


if __name__ == '__main__':
    print NpBBoxRange(
        (-10, -10, -10), (10, 10, 10)
    ).compute_contain_points([(1, 0, 0), (12, 12, 0)])
