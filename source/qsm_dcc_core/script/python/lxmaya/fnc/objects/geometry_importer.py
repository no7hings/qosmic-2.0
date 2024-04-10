# coding:utf-8
import collections

import six

import copy

import os

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.fnc.abstracts as bsc_fnc_abstracts

import lxusd.core as usd_core

import lxusd.dcc.operators as usd_dcc_operators
# maya
from ...core.wrap import *

from ... import core as mya_core
# maya dcc
from ...dcc import objects as mya_dcc_objects

from ...dcc import operators as mya_dcc_operators
# maya fnc
from . import base as mya_fnc_obj_base


class FncImporterForGeometryUsd(bsc_fnc_abstracts.AbsFncOptionBase):
    OPTION = dict(
        file='',
        location='',
        uv_map_file=None,
        root_override=None,
        #
        port_match_patterns=[]
    )
    PLUG_NAME = None
    OBJ_PATHSEP = mya_core.MyaUtil.OBJ_PATHSEP

    def __init__(self, option=None):
        super(FncImporterForGeometryUsd, self).__init__(option)
        #
        file_path = self.get('file')
        #
        self._usd_stage_opt = usd_core.UsdStageOpt()
        self._usd_stage = self._usd_stage_opt.usd_instance
        #
        if bsc_storage.StgPathOpt(file_path).get_is_file() is True:
            self._usd_stage_opt.append_sublayer(file_path)
            uv_map_file_path = self.get('uv_map_file')
            if uv_map_file_path is not None:
                self._usd_stage_opt.set_sublayer_prepend(uv_map_file_path)
            #
            self._usd_stage.Flatten()
        else:
            bsc_log.Log.trace_method_warning(
                '{}'.format(self.__class__.__name__),
                'file="{}" is non-exist'.format(file_path)
            )

    def execute(self):
        root_override = self.get('root_override')
        port_match_patterns = self.get('port_match_patterns')
        c = len([i for i in self._usd_stage.TraverseAll()])
        if c:
            if root_override is not None:
                self.create_path_fnc(root_override)
            #
            with bsc_log.LogProcessContext.create_as_bar(maximum=c, label='usd import') as l_p:
                for i_usd_prim in self._usd_stage.TraverseAll():
                    i_usd_prim_type_name = i_usd_prim.GetTypeName()
                    if i_usd_prim_type_name == usd_core.UsdNodeTypes.Xform:
                        mya_fnc_obj_base.FncNodeForUsdTransform(i_usd_prim, location=root_override).set_create()
                    elif i_usd_prim_type_name == usd_core.UsdNodeTypes.Mesh:
                        mya_fnc_obj_base.FncNodeForUsdMesh(i_usd_prim, location=root_override).set_create()
                    #
                    mya_fnc_obj_base.FncNodeForUsdBase(i_usd_prim, location=root_override).create_customize_ports(
                        port_match_patterns
                    )
                    #
                    l_p.do_update()

    @classmethod
    def import_fnc(cls, usd_stage, root_override, port_match_patterns):
        c = len([i for i in usd_stage.TraverseAll()])
        if c:
            if root_override is not None:
                cls.create_path_fnc(root_override)
            #
            with bsc_log.LogProcessContext.create(maximum=c, label='usd import') as g_p:
                for i_usd_prim in usd_stage.TraverseAll():
                    i_usd_prim_type_name = i_usd_prim.GetTypeName()
                    if i_usd_prim_type_name == usd_core.UsdNodeTypes.Xform:
                        mya_fnc_obj_base.FncNodeForUsdTransform(i_usd_prim, location=root_override).set_create()
                    elif i_usd_prim_type_name == usd_core.UsdNodeTypes.Mesh:
                        mya_fnc_obj_base.FncNodeForUsdMesh(i_usd_prim, location=root_override).set_create()
                    #
                    mya_fnc_obj_base.FncNodeForUsdBase(i_usd_prim, location=root_override).create_customize_ports(
                        port_match_patterns
                    )
                    #
                    g_p.do_update()

    @classmethod
    def create_root_fnc(cls, path, type_name):
        path_opt = bsc_core.PthNodeOpt(path)
        mya_dag_path = path_opt.translate_to(cls.OBJ_PATHSEP)
        mya_obj = mya_dcc_objects.Transform(mya_dag_path.path)
        if mya_obj.get_is_exists() is False:
            mya_obj.get_dcc_instance(
                type_name
            )

    @classmethod
    def create_path_fnc(cls, path):
        path_opt = bsc_core.PthNodeOpt(path)
        paths = path_opt.get_component_paths()
        if paths:
            paths.reverse()
            for i_path in paths:
                if i_path != '/':
                    cls.create_transform_fnc(i_path)

    @classmethod
    def create_transform_fnc(cls, path, matrix=None):
        path_opt = bsc_core.PthNodeOpt(path)
        mya_dag_path = path_opt.translate_to(cls.OBJ_PATHSEP)
        mya_obj = mya_dcc_objects.Transform(mya_dag_path.path)
        if mya_obj.get_is_exists() is False:
            mya_obj_opt = mya_dcc_operators.TransformOpt(mya_obj)
            if mya_obj_opt.set_create() is True:
                if matrix is not None:
                    mya_obj_opt.set_matrix(matrix)

    @classmethod
    def create_mesh_uv_map_fnc(cls, prim, uv_map_face_vertices_contrast=True):
        obj_path = prim.GetPath().pathString
        usd_dag_path = bsc_core.PthNodeOpt(obj_path)
        mya_dag_path = usd_dag_path.translate_to(cls.OBJ_PATHSEP)
        #
        mya_obj_path = mya_dag_path.path
        mya_obj = mya_dcc_objects.Node(mya_obj_path)
        if mya_obj.get_is_exists() is True:
            if mya_obj.type == 'mesh':
                mesh_mya_obj_opt = mya_dcc_operators.MeshOpt(mya_obj)
                mesh_usd_obj_opt = usd_dcc_operators.MeshOpt(prim)
                #
                face_vertices_uuid_src = mesh_usd_obj_opt.get_face_vertices_as_uuid()
                face_vertices_uuid_tgt = mesh_mya_obj_opt.get_face_vertices_as_uuid()
                if face_vertices_uuid_src == face_vertices_uuid_tgt:
                    uv_maps = mesh_usd_obj_opt.get_uv_maps()
                    if uv_maps:
                        if uv_map_face_vertices_contrast is True:
                            uv_map_face_vertices_uuid_src = mesh_usd_obj_opt.get_uv_map_face_vertices_as_uuid()
                            uv_map_face_vertices_uuid_tgt = mesh_mya_obj_opt.get_uv_map_face_vertices_as_uuid()
                            if uv_map_face_vertices_uuid_src == uv_map_face_vertices_uuid_tgt:
                                # noinspection PyArgumentEqualDefault
                                mesh_mya_obj_opt.assign_uv_maps(uv_maps, clear=False)
                            else:
                                bsc_log.Log.trace_method_warning(
                                    'uv-map(s)-import',
                                    'obj="{}" uv-map-face-vertices is changed'.format(obj_path)
                                )
                        else:
                            uv_map_face_vertices_uuid_src = mesh_usd_obj_opt.get_uv_map_face_vertices_as_uuid()
                            uv_map_face_vertices_uuid_tgt = mesh_mya_obj_opt.get_uv_map_face_vertices_as_uuid()
                            clear = uv_map_face_vertices_uuid_src != uv_map_face_vertices_uuid_tgt
                            mesh_mya_obj_opt.assign_uv_maps(uv_maps, clear=clear)
                    else:
                        bsc_log.Log.trace_method_warning(
                            'uv-map(s)-import',
                            'obj="{}" uv-map is non-exists'.format(obj_path)
                        )
                else:
                    bsc_log.Log.trace_method_warning(
                        'uv-map(s)-import',
                        'obj="{}" face-vertices is changed'.format(obj_path)
                    )
        else:
            bsc_log.Log.trace_method_warning(
                'uv-map(s)-import',
                'obj="{}" is non-exists'.format(obj_path)
            )

    def import_uv_map(self, uv_map_face_vertices_contrast=True):
        self.import_uv_map_fnc(
            self._usd_stage, uv_map_face_vertices_contrast
        )

    @classmethod
    def import_uv_map_fnc(cls, usd_state, uv_map_face_vertices_contrast):
        c = len([i for i in usd_state.TraverseAll()])
        if c:
            with bsc_log.LogProcessContext.create(maximum=c, label='usd uv-map import') as g_p:
                for i_usd_prim in usd_state.TraverseAll():
                    i_usd_prim_type_name = i_usd_prim.GetTypeName()
                    if i_usd_prim_type_name == usd_core.UsdNodeTypes.Mesh:
                        cls.create_mesh_uv_map_fnc(
                            i_usd_prim,
                            uv_map_face_vertices_contrast=uv_map_face_vertices_contrast
                        )
                    #
                    g_p.do_update()


class FncImporterForGeometryFbx(bsc_fnc_abstracts.AbsFncOptionBase):
    OPTION = dict(
        file=''
    )
    PLUG_NAME = 'fbxmaya'

    def __init__(self, option=None):
        super(FncImporterForGeometryFbx, self).__init__(option)

    def execute(self):
        """
        FBXImport -f "/production/library/resource/all/3d_asset/cement_bollard_with_base_sdfx4/v0001/geometry/fbx/cement_bollard_with_base_sdfx4.fbx" -caller "FBXMayaTranslator";
        :return:
        """
        cmds.loadPlugin(self.PLUG_NAME, quiet=1)
        mel.eval(
            'FBXImport -f "{file}";'.format(
                **dict(
                    file=self.get('file')
                )
            )
        )


class FncImporterForGeometryUsdOld(object):
    """
-apiSchema	-api	string (multi)	none	Imports the given API schemas' attributes as Maya custom attributes. This only recognizes API schemas that have been applied to prims on the stage. The attributes will properly round-trip if you re-export back to USD.
-chaser	-chr	string(multi)	none	Specify the import chasers to execute as part of the export. See "Import Chasers" below.
-chaserArgs	-cha	string[3] multi	none	Pass argument names and values to import chasers. Each argument to -chaserArgs should be a triple of the form: (<chaser name>, <argument name>, <argument value>). See "Import Chasers" below.
-excludePrimvar	-epv	string (multi)	none	Excludes the named primvar(s) from being imported as color sets or UV sets. The primvar name should be the full name without the primvars: namespace prefix.
-file	-f	string	none	Name of the USD being loaded
-frameRange	-fr	float float	none	The frame range of animations to import
-importInstances	-ii	bool	true	Import USD instanced geometries as Maya instanced shapes. Will flatten the scene otherwise.
-metadata	-md	string (multi)	hidden, instanceable, kind	Imports the given USD metadata fields as Maya custom attributes (e.g. USD_hidden, USD_kind, etc.) if they're authored on the USD prim. The metadata will properly round-trip if you re-export back to USD.
-parent	-p	string	none	Name of the Maya scope that will be the parent of the imported data.
-primPath	-pp	string	none (defaultPrim)	Name of the USD scope where traversing will being. The prim at the specified primPath (including the prim) will be imported. Specifying the pseudo-root (/) means you want to import everything in the file. If the passed prim path is empty, it will first try to import the defaultPrim for the rootLayer if it exists. Otherwise, it will behave as if the pseudo-root was passed in.
-preferredMaterial	-prm	string	lambert	Indicate a preference towards a Maya native surface material for importers that can resolve to multiple Maya materials. Allowed values are none (prefer plugin nodes like pxrUsdPreviewSurface and aiStandardSurface) or one of lambert, standardSurface, blinn, phong. In displayColor shading mode, a value of none will default to lambert.
-readAnimData	-ani	bool	false	Read animation data from prims while importing the specified USD file. If the USD file being imported specifies startTimeCode and/or endTimeCode, Maya's MinTime and/or MaxTime will be expanded if necessary to include that frame range. Note: Only some types of animation are currently supported, for example: animated visibility, animated transforms, animated cameras, mesh and NURBS surface animation via blend shape deformers. Other types are not yet supported, for example: time-varying curve points, time-varying mesh points/normals, time-varying NURBS surface points
-shadingMode	-shd	string[2] multi	useRegistry UsdPreviewSurface	Ordered list of shading mode importers to try when importing materials. The search stops as soon as one valid material is found. Allowed values for the first parameter are: none (stop search immediately, must be used to signal no material import), displayColor (if there are bound materials in the USD, create corresponding Lambertian shaders and bind them to the appropriate Maya geometry nodes), pxrRis (attempt to reconstruct a Maya shading network from (presumed) Renderman RIS shading networks in the USD), useRegistry (attempt to reconstruct a Maya shading network from (presumed) UsdShade shading networks in the USD) the second item in the parameter pair is a convertMaterialFrom flag which allows specifying which one of the registered USD material sources to explore. The full list of registered USD material sources can be found via the mayaUSDListShadingModesCommand command.
-useAsAnimationCache	-uac	bool	false	Imports geometry prims with time-sampled point data using a point-based deformer node that references the imported USD file. When this parameter is enabled, MayaUSDImportCommand will create a pxrUsdStageNode for the USD file that is being imported. Then for each geometry prim being imported that has time-sampled points, a pxrUsdPointBasedDeformerNode will be created that reads the points for that prim from USD and uses them to deform the imported Maya geometry. This provides better import and playback performance when importing time-sampled geometry from USD, and it should reduce the weight of the resulting Maya scene since it will bypass creating blend shape deformers with per-object, per-time sample geometry. Only point data from the geometry prim will be computed by the deformer from the referenced USD. Transform data from the geometry prim will still be imported into native Maya form on the Maya shape's transform node. Note: This means that a link is created between the resulting Maya scene and the USD file that was imported. With this parameter off (as is the default), the USD file that was imported can be freely changed or deleted post-import. With the parameter on, however, the Maya scene will have a dependency on that USD file, as well as other layers that it may reference. Currently, this functionality is only implemented for Mesh prims/Maya mesh nodes.
-verbose	-v	noarg	false	Make the command output more verbose.
-variant	-var	string[2]	none	Set variant key value pairs
-importUSDZTextures	-itx	bool	false	Imports textures from USDZ archives during import to disk. Can be used in conjuction with -importUSDZTexturesFilePath to specify an explicit directory to write imported textures to. If not specified, requires a Maya project to be set in the current context.
-importUSDZTexturesFilePath	-itf	string	none	Specifies an explicit directory to write imported textures to from a USDZ archive. Has no effect if -importUSDZTextures is not specified.
    """
    OPTION = dict()
    PLUG_NAME = 'mayaUsdPlugin'
    OBJ_PATHSEP = mya_core.MyaUtil.OBJ_PATHSEP

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
    def _set_cmd_run_(cls, file_path, **kwargs):
        cmds.loadPlugin(cls.PLUG_NAME, quiet=1)
        return cmds.file(file_path, **kwargs)

    def set_run(self):
        cmds.loadPlugin(self.PLUG_NAME, quiet=1)
        #
        cmds.mayaUSDImport(
            file=self._file_path
        )


class FncImporterForGeometryAbc(bsc_fnc_abstracts.AbsFncOptionBase):
    OPTION = dict(
        file='',
        location='',
        namespace=':',
        hidden=False
    )
    PLUG_NAME = 'AbcImport'
    OBJ_PATHSEP = mya_core.MyaUtil.OBJ_PATHSEP

    def __init__(self, option=None):
        super(FncImporterForGeometryAbc, self).__init__(option)

    def execute(self):
        cmds.loadPlugin(self.PLUG_NAME, quiet=1)
        #
        namespace_temporary = 'alembic_import_{}'.format(bsc_core.SysBaseMtd.get_time_tag())
        file_path = self.get('file')
        location = self.get('location')
        root = bsc_core.PthNodeOpt(location).translate_to(
            self.OBJ_PATHSEP
        ).path
        group = mya_dcc_objects.Group(root)
        group.set_dag_components_create()
        #
        cmds.file(
            file_path,
            i=1,
            options='v=0;',
            type='Alembic',
            ra=1,
            mergeNamespacesOnClash=1,
            namespace=namespace_temporary,
            preserveReferences=1
        )
        bsc_log.Log.trace_method_result(
            'geometry abc import',
            'file="{}"'.format(file_path)
        )
        #
        hidden = self.get('hidden')
        #
        namespace_obj = mya_dcc_objects.Namespace(namespace_temporary)
        self._results = []
        objs = namespace_obj.get_objs()
        for obj in objs:
            bsc_log.Log.trace_method_result(
                'geometry abc import',
                u'obj="{}"'.format(obj.path)
            )
            if obj.type == 'transform':
                if hidden is True:
                    obj.set_visible(False)
                #
                target_obj_path = '{}|{}'.format(
                    root, bsc_core.PthNodeMtd.get_dag_name_with_namespace_clear(obj.name)
                )
                if cmds.objExists(target_obj_path) is False:
                    obj.parent_to_path(root)
                else:
                    obj.do_delete()

            obj._update_path_()
        #
        namespace_obj.do_delete()


class FncImporterForGeometryXgen(
    bsc_fnc_abstracts.AbsFncOptionBase,
    bsc_fnc_abstracts.AbsFncForDotXgenDef
):
    OPTION = dict(
        xgen_collection_file='',
        xgen_collection_directory='',
        xgen_location='',
        #
        grow_file='',
        grow_location='',
        #
        namespace=':',
    )
    PLUG_NAME = 'xgenToolkit'

    def __init__(self, option=None):
        super(FncImporterForGeometryXgen, self).__init__(option)

    @classmethod
    def import_grow_fnc(cls, grow_file, grow_location):
        if isinstance(grow_file, six.string_types):
            file_paths = [grow_file]
        else:
            file_paths = grow_file
        #
        for i_file_path in file_paths:
            FncImporterForGeometryAbc(
                option=dict(
                    file=i_file_path,
                    location=grow_location,
                    namespace=':',
                    hidden=True
                )
            ).execute()

    @classmethod
    def import_xgen_fnc(cls, xgen_collection_file, xgen_collection_directory, xgen_location):
        # noinspection PyUnresolvedReferences
        import xgenm as xg
        # noinspection PyUnresolvedReferences,PyPep8Naming
        import xgenm.xgGlobal as xgg

        #
        group = mya_dcc_objects.Group(
            bsc_core.PthNodeOpt(xgen_location).translate_to('|').get_value()
        )
        group.set_dag_components_create()
        #
        if isinstance(xgen_collection_file, six.string_types):
            file_paths = [xgen_collection_file]
        else:
            file_paths = xgen_collection_file
        #
        namespace = ''
        for i_file_path in file_paths:
            i_xgen_collection_name = xg.importPalette(
                str(i_file_path),
                [],
                namespace
            )
            i_xgen_collection_data_directory = '{}/{}'.format(
                xgen_collection_directory, i_xgen_collection_name
            )
            cmds.xgmSetAttr(
                attribute='xgDataPath',
                object=i_xgen_collection_name,
                palette=i_xgen_collection_name,
                value=i_xgen_collection_data_directory,
            )
            for i_xgen_guide in mya_dcc_objects.Group(
                    bsc_core.PthNodeOpt(xgen_location).translate_to('|').value
            ).get_all_paths(include_obj_type=['xgmSplineGuide']):
                mya_dcc_objects.Node(i_xgen_guide).set('width', .01)
            #
            if mya_core.MyaUtil.get_is_ui_mode() is True:
                mel.eval('XgCreateDescriptionEditor;')
                de = xgg.DescriptionEditor
                de.clearCacheAction.setChecked(True)
                de.updateClearControls()
                de.previewAutoAction.setChecked(False)

    def execute(self):
        cmds.loadPlugin(self.PLUG_NAME, quiet=1)
        xgen_collection_file = self.get('xgen_collection_file')
        xgen_collection_directory = self.get('xgen_collection_directory')
        xgen_location = self.get('xgen_location')
        #
        grow_file = self.get('grow_file')
        grow_location = self.get('grow_location')
        if grow_file:
            self.import_grow_fnc(
                grow_file,
                grow_location,
            )
        #
        if xgen_collection_file:
            self.import_xgen_fnc(
                xgen_collection_file,
                xgen_collection_directory,
                xgen_location
            )


class FncImporterForDatabaseGeometry(object):
    def __init__(self):
        self._selected_path = mya_dcc_objects.Selection.get_selected_paths(include=['mesh'])

    def _set_uv_map_export_import_(self):
        if self._selected_path:
            g_p = bsc_log.LogProcessContext(maximum=len(self._selected_path))
            for path in self._selected_path:
                g_p.do_update()
                mesh = mya_dcc_objects.Mesh(path)
                mesh_opt = mya_dcc_operators.MeshOpt(mesh)
                if mesh_opt.get_shell_count() == 1:
                    key = mesh_opt.get_face_vertices_as_uuid()
                    uv_maps = bsc_storage.DccTempCacheMtdForGeometryUv.get_value(key)
                    mesh_opt.assign_uv_maps(uv_maps, clear=True)
            #
            g_p.set_stop()

    def set_run(self):
        self._set_uv_map_export_import_()


class FncImporterForGeometryNew(bsc_fnc_abstracts.AbsFncOptionBase):
    """
# coding:utf-8
import lxmaya

lxmaya.set_reload()

import lxmaya.fnc.objects as mya_fnc_objects

mya_fnc_objects.FncImporterForGeometryNew(
    option=dict(
        file='/production/shows/nsa_dev/assets/chr/td_test/user/team.srf/extend/geometry/usd/v022/geo/hi.usd',
        renderable_locations=['/master/mod/hi']
    )
).execute()
    """
    OPTION = dict(
        file='',
        #
        root='/master',
        root_type='transform',
        #
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
        active_locations=[
            '/master/aux'
        ],
        #
        path_mapper=[
            # source >> target
            # renderable
            #   model
            ('/master/hi', '/master/mod/hi'),
            ('/master/lo', '/master/mod/lo'),
            # auxiliary
            ('/master/aux/grm', '/master/grm'),
            ('/master/aux/cfx', '/master/cfx'),
            ('/master/aux/efx', '/master/efx'),
            ('/master/aux/misc', '/master/misc')
        ],
        #
        root_override=None,
        #
        port_match_patterns=[],
        #
        uv_map_only=False,
        uv_map_face_vertices_contrast=True,
    )

    def __init__(self, option):
        super(FncImporterForGeometryNew, self).__init__(option)

    def get_locations_fnc(self, locations):
        list_ = []
        m = bsc_core.PthNodeMapOpt(
            collections.OrderedDict(self.get('path_mapper'))
        )
        for i_tgt in locations:
            i_src = m.get_as_reverse(i_tgt)
            if i_tgt != i_src:
                list_.append(
                    (i_src, i_tgt)
                )
            else:
                list_.append(i_src)
        return list_

    @mya_core.MyaModifier.undo_run
    def execute(self):
        file_path = self.get('file')
        root_location = self.get('root')
        root_type_name = self.get('root_type')
        #
        locations = self.get_locations_fnc(
            self.get('renderable_locations')+self.get('auxiliary_locations')
        )
        s_opt = usd_core.UsdStageOpt()

        s_opt.load_by_locations_fnc(
            file_path,
            locations=locations,
            active_locations=self.get('active_locations')
        )

        usd_stage = s_opt.usd_instance
        #
        if self.get('uv_map_only') is True:
            FncImporterForGeometryUsd.import_uv_map_fnc(
                usd_stage, self.get('uv_map_face_vertices_contrast')
            )
        else:
            FncImporterForGeometryUsd.create_root_fnc(
                root_location, root_type_name
            )
            FncImporterForGeometryUsd.import_fnc(
                usd_stage, self.get('root_override'), self.get('port_match_patterns')
            )
