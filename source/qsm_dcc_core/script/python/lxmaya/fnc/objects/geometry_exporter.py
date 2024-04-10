# coding:utf-8
import six

import os

import copy

import lxresource as bsc_resource

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.dcc.objects as bsc_dcc_objects

import lxbasic.fnc.abstracts as bsc_fnc_abstracts

import lxusd.core as usd_core

import lxusd.fnc.objects as usd_fnc_objects
# maya
from ...core.wrap import *

from ... import core as mya_core

from ...dcc import objects as mya_dcc_objects

from ...dcc import operators as mya_dcc_operators


class FncExporterForGeometryAbc(object):
    FILE = 'file'
    FRAME_RANGE = 'frameRange'
    FRAME_RELATIVE_SAMPLE = 'frameRelativeSample'
    STEP = 'step'
    ROOT = 'root'
    ATTR = 'attr'
    #
    DATA_FORMAT = 'dataFormat'
    #
    NO_NORMAL = 'noNormals'
    RENDER_ONLY = 'ro'
    STRIP_NAMESPACE = 'stripNamespaces'
    UV_WRITE = 'uvWrite'
    WRITE_FACE_SETS = 'writeFaceSets'
    WHOLE_FRAME_GEO = 'wholeFrameGeo'
    WORLD_SPACE = 'worldSpace'
    WRITE_VISIBILITY = 'writeVisibility'
    EULER_FILTER = 'eulerFilter'
    WRITE_CREASES = 'writeCreases'
    WRITE_UV_SETS = 'writeUVSets'
    #
    ATTR_PREFIX = 'attrPrefix'
    #
    OPTION = {
        NO_NORMAL: False,
        RENDER_ONLY: False,
        STRIP_NAMESPACE: True,
        UV_WRITE: True,
        WRITE_FACE_SETS: False,
        WHOLE_FRAME_GEO: False,
        WORLD_SPACE: True,
        WRITE_VISIBILITY: True,
        EULER_FILTER: False,
        WRITE_CREASES: False,
        WRITE_UV_SETS: True,
    }
    #
    OGAWA = 'ogawa'
    HDF = 'hdf'
    #
    DATA_FROAMTS = [
        OGAWA,
        HDF
    ]
    PLUG_NAME = 'AbcExport'

    def __init__(
            self,
            file_path,
            root=None,
            frame=None,
            step=None,
            attribute=None,
            attribute_prefix=None,
            option=None,
            data_format=None
        ):
        self._file_path = file_path
        #
        self._root = self._get_location_(root)
        self._star_frame, self._end_frame = mya_dcc_objects.Scene.get_frame_range(frame)
        self._step = step
        self._attribute = attribute
        self._attribute_prefix = attribute_prefix
        self._option = copy.copy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                if k in self.OPTION:
                    self._option[k] = v
                else:
                    raise KeyError()
        self._data_format = data_format
        #
        self._results = []

    @classmethod
    def _get_location_(cls, raw):
        if raw is not None:
            if isinstance(raw, six.string_types):
                _ = [raw]
            elif isinstance(raw, (tuple, list)):
                _ = list(raw)
            else:
                raise TypeError()
            return map(lambda x: bsc_core.PthNodeOpt(x).translate_to('|').to_string(), _)
        return []

    @classmethod
    def _get_file_(cls, file_path):
        return '-{0} {1}'.format(cls.FILE, file_path.replace('\\', '/'))

    @classmethod
    def _get_option_(cls, option):
        if isinstance(option, dict):
            lis = ['-{0}'.format(k) for k, v in option.items() if v is True]
            if lis:
                return ' '.join(lis)

    @classmethod
    def _get_data_format_(cls, data_format):
        if isinstance(data_format, six.string_types):
            if data_format in cls.DATA_FROAMTS:
                return '-{0} {1}'.format(cls.DATA_FORMAT, data_format)
            return '-{0} {1}'.format(cls.DATA_FORMAT, cls.OGAWA)
        return '-{0} {1}'.format(cls.DATA_FORMAT, cls.OGAWA)

    @classmethod
    def _get_frame_(cls, star_frame, end_frame):
        return '-{0} {1} {2}'.format(cls.FRAME_RANGE, star_frame, end_frame)

    @classmethod
    def _get_step_(cls, step):
        if isinstance(step, (int, float)):
            return '-{0} {1}'.format(cls.STEP, step)

    @classmethod
    def _get_root_(cls, root):
        lis = cls._get_exists_dcc_paths_(root)
        if lis:
            return ' '.join(['-{0} {1}'.format(cls.ROOT, i) for i in lis])

    @classmethod
    def _get_exists_dcc_paths_(cls, obj_path_args):
        if isinstance(obj_path_args, six.string_types):
            if cmds.objExists(obj_path_args):
                return [cmds.ls(obj_path_args, long=1)[0]]
        elif isinstance(obj_path_args, (tuple, list)):
            return [cmds.ls(i, long=1)[0] for i in obj_path_args if cmds.objExists(i)]

    @classmethod
    def _get_strs_(cls, string, includes=None):
        lis = []
        if isinstance(string, six.string_types):
            if includes:
                if string in includes:
                    lis = [string]
            else:
                lis = [string]
        elif isinstance(string, (tuple, list)):
            for i in string:
                if includes:
                    if i in includes:
                        lis.append(i)
                else:
                    lis.append(i)
        return lis

    @classmethod
    def _get_attribute_(cls, attr_name):
        lis = cls._get_strs_(attr_name)
        #
        if lis:
            _ = ' '.join(['-{0} {1}'.format(cls.ATTR, i) for i in lis])
        else:
            _ = None
        return _

    @classmethod
    def _get_attribute_prefix_(cls, attr_name):
        lis = cls._get_strs_(attr_name)
        #
        if lis:
            _ = ' '.join(['-{0} {1}'.format(cls.ATTR_PREFIX, i) for i in lis])
        else:
            _ = None
        return _

    @staticmethod
    def _get_j_(js):
        _ = [i for i in js if i is not None]
        if _:
            return ' '.join(_)

    @classmethod
    def _set_cmd_run_(cls, j):
        """
        :param j: str
        :return: None
        """
        cmds.loadPlugin(cls.PLUG_NAME, quiet=1)
        return cmds.AbcExport(j=j)

    #
    def set_run(self):
        js = [
            self._get_frame_(self._star_frame, self._end_frame),
            self._get_step_(self._step),
            self._get_attribute_(self._attribute),
            self._get_attribute_prefix_(self._attribute_prefix),
            self._get_option_(self._option),
            self._get_data_format_(self._data_format),
            self._get_root_(self._root),
            self._get_file_(self._file_path)
        ]
        #
        file_ = bsc_dcc_objects.StgFile(self._file_path)
        directory_ = file_.directory
        if directory_.get_is_exists() is False:
            directory_.set_create()
        #
        j = self._get_j_(js)
        if j:
            self._results = self._set_cmd_run_(j)
            bsc_log.Log.trace_method_result(
                'alembic export',
                'file="{}"'.format(file_.path)
            )
            if self._results:
                for i in self._results:
                    bsc_log.Log.trace_result(
                        'export ".abc": "{}"'.format(i)
                    )
        return self._results

    def get_outputs(self):
        return self._results


class FncExporterForGeometryUsdOld(object):
    OPTION = dict(
        exportUVs=1,
        exportColorSets=1,
        defaultMeshScheme='catmullClark',
        defaultUSDFormat='usdc',
        animation=0,
        eulerFilter=0,
        staticSingleSample=0,
        startTime=1,
        endTime=1,
        frameStride=1,
        frameSample=0.0,
        parentScope='',
        exportDisplayColor=0,
        shadingMode='displayColor',
        convertMaterialsTo='UsdPreviewSurface',
        exportInstances=1,
        exportVisibility=1,
        mergeTransformAndShape=0,
        stripNamespaces=1
    )
    PLUG_NAME = 'mayaUsdPlugin'

    def __init__(self, file_path, root=None, option=None):
        self._file_path = file_path
        self._root = root

        self._option = copy.copy(self.OPTION)
        self._option['defaultUSDFormat'] = self._get_usd_format_(self._file_path)
        if isinstance(option, dict):
            for k, v in option.items():
                self._option[k] = v

        self._results = []

    @classmethod
    def _get_usd_format_(cls, file_path):
        ext = os.path.splitext(file_path)[-1]
        if ext == '.usd':
            return 'usdc'
        elif ext == '.usda':
            return 'usda'
        raise TypeError()

    @classmethod
    def _get_usd_option_(cls, option):
        lis = []
        for k, v in option.items():
            if isinstance(v, bool):
                v = int(v)
            lis.append(';{}={}'.format(k, v))
        return ''.join(lis)

    @classmethod
    def _set_cmd_run_(cls, file_path, **kwargs):
        cmds.loadPlugin(cls.PLUG_NAME, quiet=1)
        return cmds.file(file_path, **kwargs)

    def set_run(self):
        os_file = bsc_dcc_objects.StgFile(self._file_path)
        os_file.create_directory()
        #
        usd_option = self._get_usd_option_(self._option)
        kwargs = dict(
            type='USD Export',
            options=usd_option,
            force=1,
            preserveReferences=1,
        )
        _selected_paths = []
        if self._root is not None:
            _selected_paths = cmds.ls(selection=1, long=1) or []
            cmds.select(self._root)
            kwargs['exportSelected'] = True
        else:
            kwargs['exportAll'] = True
        #
        _ = self._set_cmd_run_(self._file_path, **kwargs)
        if _:
            self._results = [self._file_path]
        #
        if self._results:
            for i in self._results:
                bsc_log.Log.trace_method_result(
                    'maya-usd-exporter',
                    u'file="{}"'.format(i)
                )

        if 'exportSelected' in kwargs:
            if _selected_paths:
                cmds.select(_selected_paths)
            else:
                cmds.select(clear=1)

        return self._results

    def get_outputs(self):
        return self._results


class FncExporterForGeometryUsdOld1(object):
    OPTION = {}

    def __init__(self, file_path, root=None, option=None):
        self._file_path = file_path
        self._root = root

        self._option = copy.deepcopy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                self._option[k] = v

        self._results = []

    def set_run(self):
        # noinspection PyUnresolvedReferences
        from papyUsd.maya import MayaUsdExport

        root = bsc_core.PthNodeMtd.get_dag_pathsep_replace(
            self._root, pathsep_tgt=mya_core.MyaUtil.OBJ_PATHSEP
        )
        s_r = root
        r = '|'.join(s_r.split('|')[:-1])
        MayaUsdExport.MayaUsdExport().subTree(r, s_r, self._file_path)
        #
        self._results = [self._file_path]
        if self._results:
            for i in self._results:
                bsc_log.Log.trace_method_result(
                    'maya-usd-exporter',
                    u'file="{}"'.format(i)
                )


class FncExporterForDatabaseGeometry(object):
    OPTION = dict(
        force=False
    )

    def __init__(self, option=None):
        self._results = []
        self._errors = []
        self._warnings = []
        #
        self._option = copy.copy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                self._option[k] = v
        #
        self._selected_path = mya_dcc_objects.Selection.get_selected_paths(include=['mesh'])

    def _set_uv_map_export_run_(self):
        if self._selected_path:
            with bsc_log.LogProcessContext.create(maximum=len(self._selected_path)) as gp:
                for path in self._selected_path:
                    gp.do_update()
                    mesh = mya_dcc_objects.Mesh(path)
                    mesh_opt = mya_dcc_operators.MeshOpt(mesh)
                    if mesh_opt.get_shell_count() == 1:
                        uv_maps = mesh_opt.get_uv_maps()
                        key = mesh_opt.get_face_vertices_as_uuid()
                        if bsc_storage.DccTempCacheMtdForGeometryUv.set_value(
                                key=key,
                                value=uv_maps,
                                force=self._option['force']
                        ) is True:
                            bsc_log.Log.trace_method_result(
                                '{}'.format(self.__class__.__name__),
                                'obj="{}"'.format(mesh.path)
                            )
                    else:
                        bsc_log.Log.trace_method_warning(
                            '{}'.format(self.__class__.__name__),
                            'obj="{}" shell is more than "one"'.format(mesh.path)
                        )

    def set_run(self):
        self._set_uv_map_export_run_()


class FncExporterForCameraAbc(bsc_fnc_abstracts.AbsFncOptionBase):
    OPTION = dict(
        file='',
        location='',
        frame=(1, 1),
    )

    def __init__(self, option):
        super(FncExporterForCameraAbc, self).__init__(option)
        option = self.get_option()
        location = option.get('location')
        g = mya_dcc_objects.Group(bsc_core.PthNodeOpt(location).translate_to('|').to_string())
        self._camera_shape_paths = g.get_all_shape_paths(include_obj_type='camera')
        self._camera_transform_paths = map(lambda x: mya_dcc_objects.Shape(x).transform.path, self._camera_shape_paths)

    def pre_run_fnc(self):
        for i in self._camera_shape_paths:
            i_camera_shape = mya_dcc_objects.Shape(i)
            i_camera_shape.get_port('overscan').set(1)
            #
            i_camera_shape.get_port('lx_film_fit').set_create('long')
            i_camera_shape.get_port('lx_film_fit').set(
                i_camera_shape.get_port('filmFit').get()
            )
            i_camera_shape.get_port('lx_camera_tag').set_create('string')
            i_camera_shape.get_port('lx_camera_tag').set(
                'main'
            )

    def set_run(self):
        self.pre_run_fnc()
        option = self.get_option()
        FncExporterForGeometryAbc(
            file_path=option.get('file'),
            root=self._camera_transform_paths,
            frame=option.get('frame'),
            attribute=['lx_film_fit', 'lx_camera_tag']
        ).set_run()


class FncExporterForGeometryUsd(bsc_fnc_abstracts.AbsFncOptionBase):
    OPTION = dict(
        file='',
        location='',
        #
        default_prim_path=None,
        #
        with_mesh=True,
        with_mesh_uv=True,
        with_curve=True,
        #
        path_lstrip=None,
        use_override=False,
        export_selected=False,
        # auto clear namespace
        namespace_clear=True,
        #
        with_visible=True,
        #
        with_display_color=True,
        display_color=(0.25, 0.75, 0.5),
        #
        auto_display_color=False,
        auto_plant_display_color=False,
        #
        with_mesh_subset=False,
        with_material_assign=False,
        #
        port_match_patterns=[]
    )

    def __init__(self, option=None):
        super(FncExporterForGeometryUsd, self).__init__(option)

    def execute(self):
        file_path = self.get('file')
        location = self.get('location')
        #
        default_prim_path = self.get('default_prim_path')
        use_override = self.get('use_override')
        usd_root_lstrip = self.get('path_lstrip')
        with_visible = self.get('with_visible')
        with_display_color = self.get('with_display_color')
        display_color = self.get('display_color')
        auto_display_color = self.get('auto_display_color')
        auto_plant_display_color = self.get('auto_plant_display_color')
        with_mesh_subset = self.get('with_mesh_subset')
        with_material_assign = self.get('with_material_assign')
        port_match_patterns = self.get('port_match_patterns')
        #
        if location.startswith('|'):
            location = location.replace('|', '/')
        #
        root_dag_path = bsc_core.PthNodeOpt(location)
        root_mya_dag_path = root_dag_path.translate_to(
            pathsep=mya_core.MyaUtil.OBJ_PATHSEP
        )
        mya_root = root_mya_dag_path.path
        #
        root_mya_obj = mya_dcc_objects.Group(mya_root)
        if root_mya_obj.get_is_exists() is True:
            mya_objs = root_mya_obj.get_descendants()
            if mya_objs:
                usd_geometry_exporter = usd_fnc_objects.FncGeometryExporter(
                    option=dict(
                        file=file_path,
                        location=location,
                        #
                        default_prim_path=default_prim_path
                    )
                )
                c = len(mya_objs)
                with bsc_log.LogProcessContext.create(maximum=c, label='geometry-usd export') as g_p:
                    for i_mya_obj in mya_objs:
                        i_mya_type_name = i_mya_obj.get_type_name()
                        i_mya_api_type_name = i_mya_obj.get_api_type()
                        i_mya_obj_path = i_mya_obj.get_path()
                        #
                        i_usd_obj_path = bsc_core.PthNodeMtd.get_dag_pathsep_replace(
                            i_mya_obj_path, pathsep_src=mya_core.MyaUtil.OBJ_PATHSEP
                        )
                        i_usd_obj_path = bsc_core.PthNodeMtd.get_dag_path_lstrip(i_usd_obj_path, usd_root_lstrip)

                        i_rgb = None
                        if auto_plant_display_color is True:
                            i_rgb = bsc_core.PthNodeOpt(i_usd_obj_path).get_plant_rgb(maximum=1.0)
                        elif auto_display_color is True:
                            i_rgb = bsc_core.PthNodeOpt(i_usd_obj_path).get_rgb(maximum=1.0)
                        elif with_display_color is True:
                            i_rgb = display_color
                        # clean namespace
                        if ':' in i_usd_obj_path:
                            bsc_log.Log.trace_method_warning(
                                'usd-mesh export',
                                'obj="{}" has namespace'.format(i_usd_obj_path)
                            )
                        #
                        i_usd_obj_path = bsc_core.PthNodeMtd.get_dag_path_with_namespace_clear(
                            i_usd_obj_path
                        )
                        i_usd_obj_path = bsc_core.PthNodeMtd.cleanup_dag_path(
                            i_usd_obj_path
                        )
                        if i_mya_api_type_name in mya_core.MyaNodeApiTypes.Transforms:
                            transform_mya_obj = mya_dcc_objects.Transform(i_mya_obj_path)
                            transform_mya_obj_opt = mya_dcc_operators.TransformOpt(transform_mya_obj)
                            transform_usd_obj_opt = usd_geometry_exporter.create_transform_opt(
                                i_usd_obj_path, use_override=use_override
                            )
                            matrix = transform_mya_obj_opt.get_matrix()
                            transform_usd_obj_opt.set_matrix(matrix)
                            #
                            if with_visible is True:
                                transform_usd_obj_opt.set_visible(
                                    transform_mya_obj.get_visible()
                                )
                        #
                        elif i_mya_type_name == mya_core.MyaNodeTypes.Mesh:
                            i_mya_mesh = mya_dcc_objects.Mesh(i_mya_obj_path)
                            if i_mya_mesh.get_port('intermediateObject').get() is False:
                                i_mya_mesh_opt = mya_dcc_operators.MeshOpt(i_mya_mesh)
                                i_mya_mesh_look_opt = mya_dcc_operators.MeshLookOpt(i_mya_mesh)
                                if i_mya_mesh_opt.get_is_invalid() is False:
                                    i_usd_mesh_opt = usd_geometry_exporter.create_mesh_opt(
                                        i_usd_obj_path, use_override=use_override
                                    )
                                    i_usd_mesh_opt.set_create(
                                        face_vertices=i_mya_mesh_opt.get_face_vertices(),
                                        points=i_mya_mesh_opt.get_points(),
                                        uv_maps=i_mya_mesh_opt.get_uv_maps()
                                    )
                                    if with_mesh_subset is True:
                                        subsets = i_mya_mesh_look_opt.get_subsets_by_material_assign()
                                        if subsets:
                                            i_usd_mesh_opt.create_subsets(
                                                subsets
                                            )
                                    if with_material_assign is True:
                                        material_assigns = i_mya_mesh_look_opt.get_material_assigns()
                                        i_usd_mesh_opt.assign_materials(
                                            material_assigns
                                        )
                                    # export visibility
                                    if with_visible is True:
                                        i_usd_mesh_opt.set_visible(
                                            i_mya_mesh.get_visible()
                                        )
                                    # export color use name
                                    if i_rgb is not None:
                                        i_usd_mesh_opt.fill_display_color(i_rgb)
                                else:
                                    bsc_log.Log.trace_method_error(
                                        'usd-mesh export',
                                        'obj="{}" is invalid'.format(i_mya_obj.path)
                                    )
                        # nurbs curve
                        elif i_mya_type_name == mya_core.MyaNodeTypes.Curve:
                            i_mya_curve = mya_dcc_objects.Curve(i_mya_obj_path)
                            if i_mya_curve.get_port('intermediateObject').get() is False:
                                i_mya_curve_opt = mya_dcc_operators.NurbsCurveOpt(i_mya_curve)
                                if i_mya_curve_opt.get_is_invalid() is False:
                                    i_usd_curve_opt = usd_geometry_exporter.create_basis_curves_opt(
                                        i_usd_obj_path, use_override=use_override
                                    )
                                    counts, points, widths = i_mya_curve_opt.get_usd_basis_curve_data()
                                    i_usd_curve_opt.set_create(
                                        counts, points, widths
                                    )
                                    if i_rgb is not None:
                                        i_usd_curve_opt.fill_display_color(i_rgb)
                        # xgen description
                        elif i_mya_type_name == mya_core.MyaNodeTypes.XgenDescription:
                            i_mya_xgen_description = mya_dcc_objects.Shape(i_mya_obj_path)
                            i_mya_xgen_description_guide_opt = mya_dcc_operators.XgenDescriptionOpt(
                                i_mya_xgen_description
                            )
                            if i_mya_xgen_description_guide_opt.get_is_exists() is True:
                                i_usd_curve_opt = usd_geometry_exporter.create_basis_curves_opt(
                                    i_usd_obj_path, use_override=use_override
                                )
                                counts, points, widths = i_mya_xgen_description_guide_opt.get_usd_basis_curve_data()
                                i_usd_curve_opt.set_create(
                                    counts, points, widths
                                )
                                if i_rgb is not None:
                                    i_usd_curve_opt.fill_display_color(i_rgb)
                        #
                        if port_match_patterns:
                            i_geometry_usd_fnc = usd_geometry_exporter._get_geometry_fnc_(i_usd_obj_path)
                            if i_geometry_usd_fnc is not None:
                                i_customize_ports = mya_core.CmdObjOpt(i_mya_obj_path).get_customize_ports()
                                for j_port in i_customize_ports:
                                    if j_port.get_is_naming_matches(port_match_patterns) is True:
                                        j_key = j_port.port_path
                                        j_value = j_port.get()
                                        if j_value is None:
                                            j_value = ''
                                        #
                                        usd_core.UsdPrimOpt._add_customize_attribute_(
                                            i_geometry_usd_fnc, j_key, j_value
                                        )
                        #
                        g_p.do_update()
                #
                usd_geometry_exporter.execute()
        else:
            bsc_log.Log.trace_method_warning(
                'maya-usd-export',
                'obj="{}" is non-exists'.format(location)
            )


class FncExporterForGeometryUvMapUsd(bsc_fnc_abstracts.AbsFncOptionBase):
    OPTION = dict(
        file='',
        location='',
        root='',
        #
        display_color=(0.75, .75, 0.5),
        subdiv_dict={}
    )

    def __init__(self, option):
        super(FncExporterForGeometryUvMapUsd, self).__init__(option)

    @classmethod
    def _set_subdiv_(cls, obj_path, subdiv_count):
        _ = cmds.listConnections(obj_path, destination=0, source=1, type='polySmoothFace')
        if _:
            mya_core.CmdObjOpt(_[0]).set('divisions', subdiv_count)
            mya_core.CmdObjOpt(_[0]).set('smoothUVs', 0)
            return _
        return cmds.polySmooth(
            obj_path,
            dv=subdiv_count,
            mth=0,
            sdt=0,
            ovb=1,
            ofb=3,
            ofc=0,
            ost=0,
            ocr=0,
            bnr=1,
            c=1,
            kb=1,
            ksb=1,
            khe=0,
            kt=1,
            kmb=1,
            suv=0,
            peh=0,
            sl=1,
            dpe=1,
            ps=0.1,
            ro=1,
            ch=1
        )

    @classmethod
    def _get_tmp_usd_file_(cls):
        user_directory_path = bsc_storage.StgTmpBaseMtd.get_user_directory('usd-export')
        return '{}/{}.usd'.format(
            user_directory_path,
            bsc_core.TimestampOpt(
                bsc_core.SysBaseMtd.get_timestamp()
            ).get_as_tag_36()
        )

    @classmethod
    def _set_tmp_usd_export_(cls, file_path, location, root):
        FncExporterForGeometryUsd(
            option=dict(
                file=file_path,
                location=location,
                #
                default_prim_path=root,
                with_mesh_uv=True,
                with_mesh=True,
                #
                use_override=False
            )
        ).execute()

    def set_run(self):
        subdiv_dict = self.get('subdiv_dict')
        post_deletes = []
        if subdiv_dict:
            for k, v in subdiv_dict.items():
                i_obj_path = bsc_core.PthNodeOpt(
                    k
                ).translate_to('|')
                # i_results = self._set_subdiv_(
                #     i_obj_path, v
                # )
                # post_deletes.extend(i_results)
        #
        file_path = self.get('file')
        temp_usd_file_path = self._get_tmp_usd_file_()
        location = self.get('location')
        root = self.get('root')

        self._set_tmp_usd_export_(
            temp_usd_file_path, location, root
        )

        # print temp_usd_file_path
        # temp_usd_file_path = '/l/temp/temporary/usd-export/2022_0913-dongchangbao/RI58SQ.usd'

        usd_fnc_objects.GeometryUvMapExporter(
            file_path=file_path,
            root=root,
            option=dict(
                file_0=temp_usd_file_path,
                file_1=temp_usd_file_path,
                display_color=self.get('display_color')
            )
        ).set_run()


class FncExporterForGeometryUsdNew(bsc_fnc_abstracts.AbsFncOptionBase):
    KEY = 'geometry usd export'
    OPTION = dict(
        file='',
        # locations
        renderable_locations=[
            # '/master/mod/hi',
            # '/master/mod/lo',
            # '/master/hair',
            # '/master/plant',
            # '/master/light'
        ],
        auxiliary_locations=[
            # '/master/grm',
            # '/master/cfx',
            # '/master/efx',
            # '/master/misc'
        ],
        #
        root='/master',
        #
        pathsep='|',
        #
        port_match_patterns=[
            # 'pg_*'
        ]
    )

    def __init__(self, option):
        super(FncExporterForGeometryUsdNew, self).__init__(option)

    def execute(self):
        file_path = self.get('file')
        if not file_path:
            raise RuntimeError()

        directory_path = bsc_storage.StgFileOpt(file_path).get_directory_path()

        root = self.get('root')
        pathsep = self.get('pathsep')
        #
        export_args = []
        for i_branch_key in ['renderable', 'auxiliary']:
            i_branch_data = []
            i_leaf_locations = self.get('{}_locations'.format(i_branch_key))
            for j_leaf_location in i_leaf_locations:
                j_leaf_location_opt_cur = bsc_core.PthNodeOpt(j_leaf_location).translate_to(
                    pathsep
                )
                j_leaf_location_cur = j_leaf_location_opt_cur.get_value()
                if mya_core.CmdObjOpt._get_is_exists_(j_leaf_location_cur) is True:
                    j_leaf_name = j_leaf_location_opt_cur.get_name()
                    j_leaf_file_name = 'geo/{}.usd'.format(j_leaf_name)
                    j_leaf_option = dict(
                        name=j_leaf_name,
                        location=j_leaf_location,
                        file=j_leaf_file_name,
                    )
                    i_branch_data.append(j_leaf_option)
            #
            export_args.append((i_branch_key, i_branch_data))
        #
        if export_args:
            payload_key = 'payload'
            payload_cfg_key = 'usda/geometry/{}'.format(payload_key)
            payload_c = bsc_resource.RscExtendJinja.get_configure(payload_cfg_key)
            payload_t = bsc_resource.RscExtendJinja.get_template(payload_cfg_key)
            with bsc_log.LogProcessContext.create(maximum=len(export_args)) as g_p:
                for i_branch_key, i_branch_data in export_args:
                    g_p.do_update()
                    #
                    if i_branch_data:
                        i_branch_cfg_key = 'usda/geometry/all/{}'.format(i_branch_key)
                        i_branch_c = bsc_resource.RscExtendJinja.get_configure(i_branch_cfg_key)
                        i_branch_t = bsc_resource.RscExtendJinja.get_template(i_branch_cfg_key)
                        for j_leaf_option in i_branch_data:
                            i_branch_c.append_element('elements', j_leaf_option)
                            #
                            j_leaf_file_path = '{}/{}'.format(directory_path, j_leaf_option.get('file'))
                            j_leaf_location = j_leaf_option.get('location')
                            #
                            FncExporterForGeometryUsd(
                                option=dict(
                                    file=j_leaf_file_path,
                                    location=j_leaf_location,
                                    #
                                    default_prim_path=root,
                                    #
                                    with_mesh_uv=True,
                                    with_mesh=True,
                                    with_curve=True,
                                    #
                                    port_match_patterns=self.get('port_match_patterns')
                                )
                            ).execute()
                        #
                        i_branch_raw = i_branch_t.render(
                            **i_branch_c.get_value()
                        )
                        i_branch_file_name = '{}.usda'.format(i_branch_key)
                        i_branch_file_path = '{}/{}'.format(directory_path, i_branch_file_name)
                        #
                        payload_c.append_element('elements', dict(file=i_branch_file_name))
                        #
                        bsc_storage.StgFileOpt(
                            i_branch_file_path
                        ).set_write(
                            i_branch_raw
                        )
            #
            payload_raw = payload_t.render(
                **payload_c.get_value()
            )
            bsc_storage.StgFileOpt(
                file_path
            ).set_write(
                payload_raw
            )
        else:
            bsc_log.Log.trace_method_warning(
                self.KEY,
                'nothing to export'
            )
