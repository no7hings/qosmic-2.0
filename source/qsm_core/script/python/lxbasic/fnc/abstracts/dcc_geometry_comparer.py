# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.dcc.core as bsc_dcc_core

import lxcontent.core as ctt_core

from . import base as bsc_fnc_abs_base


class AbsFncMatcherForDccMesh(object):
    FNC_DCC_MESH_CLS = None
    # cache for exchanged
    DCC_CACHE_SRC = ctt_core.Content(value=dict())

    @classmethod
    def _push_geometry_cache(cls, path_src, path_tgt):
        if cls.FNC_DCC_MESH_CLS is not None:
            cls.DCC_CACHE_SRC.set(
                '{}.geometry'.format(path_src),
                cls.FNC_DCC_MESH_CLS(path_tgt).get_geometry()
            )

    @classmethod
    def _push_look_cache(cls, path_src, path_tgt):
        if cls.FNC_DCC_MESH_CLS is not None:
            cls.DCC_CACHE_SRC.set(
                '{}.look'.format(path_src),
                cls.FNC_DCC_MESH_CLS(path_tgt).get_look()
            )

    @classmethod
    def _pull_geometry_cache(cls, path_src):
        return cls.DCC_CACHE_SRC.get(
            '{}.geometry'.format(path_src)
        )

    @classmethod
    def _pull_look_cache(cls, path_src):
        return cls.DCC_CACHE_SRC.get(
            '{}.look'.format(path_src)
        )

    def __init__(self, path_src, data_src, data_tgt):
        self._path_src = path_src
        self._src_data = data_src
        self._tgt_data = data_tgt
        #
        self._src_paths = self._src_data.get_key_names_at('property.path')
        self._src_face_vertices_uuid = self._src_data.get('face-vertices.path.{}'.format(self._path_src))
        self._src_points_uuid = self._src_data.get('points.path.{}'.format(self._path_src))
        #
        self._tgt_paths = self._tgt_data.get_key_names_at('property.path')
        self._tgt_face_vertices_uuids = self._tgt_data.get_key_names_at('face-vertices.uuid')
        self._tgt_points_uuids = self._tgt_data.get_key_names_at('points.uuid')

    def __get_path_exchanged_(self):
        path_tgt = self._path_src
        #
        output_path = path_tgt
        check_statuses = [
            bsc_dcc_core.DccMeshCheckStatus.FaceVerticesChanged,
            bsc_dcc_core.DccMeshCheckStatus.PointsChanged
        ]
        #
        tgt_face_vertices_uuid_has_matched = self._src_face_vertices_uuid in self._tgt_face_vertices_uuids
        tgt_points_uuid_has_matched = self._src_points_uuid in self._tgt_points_uuids
        tgt_uuid_has_matched_condition = tgt_face_vertices_uuid_has_matched, tgt_points_uuid_has_matched
        if tgt_uuid_has_matched_condition == (True, True):
            tgt_face_vertices_uuid = self._src_face_vertices_uuid
            tgt_points_uuid = self._src_points_uuid
            tgt_paths_in_face_vertices = self._tgt_data.get(
                'face-vertices.uuid.{}'.format(tgt_face_vertices_uuid)
            ) or []
            tgt_paths_in_points = self._tgt_data.get(
                'points.uuid.{}'.format(tgt_points_uuid)
            ) or []
            uuid_matched_tgt_paths = bsc_core.RawListMtd.get_intersection(
                tgt_paths_in_face_vertices,
                tgt_paths_in_points
            )
            if uuid_matched_tgt_paths:
                output_path = uuid_matched_tgt_paths[0]
                check_statuses = [
                    bsc_dcc_core.DccMeshCheckStatus.PathExchanged
                ]
        elif tgt_uuid_has_matched_condition == (True, False):
            tgt_face_vertices_uuid = self._src_face_vertices_uuid
            tgt_paths_in_face_vertices = self._tgt_data.get(
                'face-vertices.uuid.{}'.format(tgt_face_vertices_uuid)
            ) or []
            uuid_matched_tgt_paths = tgt_paths_in_face_vertices
            if uuid_matched_tgt_paths:
                output_path = uuid_matched_tgt_paths[0]
                check_statuses = [
                    bsc_dcc_core.DccMeshCheckStatus.PathExchanged,
                    bsc_dcc_core.DccMeshCheckStatus.PointsChanged
                ]
        elif tgt_uuid_has_matched_condition == (False, True):
            tgt_points_uuid = self._src_points_uuid
            tgt_paths_in_points = self._tgt_data.get(
                'points.uuid.{}'.format(tgt_points_uuid)
            ) or []
            uuid_matched_tgt_paths = tgt_paths_in_points
            if uuid_matched_tgt_paths:
                output_path = uuid_matched_tgt_paths[0]
                check_statuses = [
                    bsc_dcc_core.DccMeshCheckStatus.PathExchanged,
                    bsc_dcc_core.DccMeshCheckStatus.FaceVerticesChanged
                ]
        elif tgt_uuid_has_matched_condition == (False, False):
            output_path = path_tgt
            check_statuses = [
                bsc_dcc_core.DccMeshCheckStatus.FaceVerticesChanged,
                bsc_dcc_core.DccMeshCheckStatus.PointsChanged
            ]
        #
        self._push_geometry_cache(self._path_src, output_path)
        self._push_look_cache(self._path_src, output_path)
        return output_path, check_statuses

    def __get_path_changed_(self):
        output_path = self._path_src
        check_statuses = [bsc_dcc_core.DccMeshCheckStatus.Deletion]
        #
        tgt_face_vertices_uuid_has_matched = self._src_face_vertices_uuid in self._tgt_face_vertices_uuids
        tgt_points_uuid_has_matched = self._src_points_uuid in self._tgt_points_uuids
        tgt_uuid_has_matched_condition = tgt_face_vertices_uuid_has_matched, tgt_points_uuid_has_matched
        if tgt_uuid_has_matched_condition == (True, True):
            tgt_face_vertices_uuid = self._src_face_vertices_uuid
            tgt_points_uuid = self._src_points_uuid
            #
            tgt_paths_in_face_vertices = self._tgt_data.get(
                'face-vertices.uuid.{}'.format(tgt_face_vertices_uuid)
            ) or []
            tgt_paths_in_points = self._tgt_data.get(
                'points.uuid.{}'.format(tgt_points_uuid)
            ) or []
            #
            uuid_matched_tgt_paths = bsc_core.RawListMtd.get_addition(
                bsc_core.RawListMtd.get_intersection(tgt_paths_in_face_vertices, tgt_paths_in_points) or [],
                self._src_paths
            ) or []
            if uuid_matched_tgt_paths:
                output_path = uuid_matched_tgt_paths[0]
                check_statuses = [
                    bsc_dcc_core.DccMeshCheckStatus.PathChanged
                ]
        elif tgt_uuid_has_matched_condition == (True, False):
            tgt_face_vertices_uuid = self._src_face_vertices_uuid
            tgt_paths_in_face_vertices = self._tgt_data.get(
                'face-vertices.uuid.{}'.format(tgt_face_vertices_uuid)
            ) or []
            uuid_matched_tgt_paths = bsc_core.RawListMtd.get_addition(
                tgt_paths_in_face_vertices,
                self._src_paths
            ) or []
            if uuid_matched_tgt_paths:
                output_path = uuid_matched_tgt_paths[0]
                check_statuses = [
                    bsc_dcc_core.DccMeshCheckStatus.PathChanged,
                    bsc_dcc_core.DccMeshCheckStatus.PointsChanged
                ]
        elif tgt_uuid_has_matched_condition == (False, True):
            tgt_points_uuid = self._src_points_uuid
            tgt_paths_in_points = self._tgt_data.get(
                'points.uuid.{}'.format(tgt_points_uuid)
            ) or []
            uuid_matched_tgt_paths = bsc_core.RawListMtd.get_addition(
                tgt_paths_in_points,
                self._src_paths
            ) or []
            if uuid_matched_tgt_paths:
                output_path = uuid_matched_tgt_paths[0]
                check_statuses = [
                    bsc_dcc_core.DccMeshCheckStatus.PathChanged,
                    bsc_dcc_core.DccMeshCheckStatus.FaceVerticesChanged
                ]
        elif tgt_uuid_has_matched_condition == (False, False):
            output_path = self._path_src
            check_statuses = [bsc_dcc_core.DccMeshCheckStatus.Deletion]
        return output_path, check_statuses

    def execute(self):
        find_path_match = self._path_src in self._tgt_paths
        if find_path_match is True:
            path_tgt = self._path_src
            #
            output_path = path_tgt
            check_statuses = [
                bsc_dcc_core.DccMeshCheckStatus.FaceVerticesChanged,
                bsc_dcc_core.DccMeshCheckStatus.PointsChanged
            ]
            #
            tgt_face_vertices_uuid = self._tgt_data.get(
                'face-vertices.path.{}'.format(path_tgt)
            )
            tgt_points_uuid = self._tgt_data.get('points.path.{}'.format(path_tgt))
            #
            tgt_face_vertices_match = self._src_face_vertices_uuid == tgt_face_vertices_uuid
            tgt_points_match = self._src_points_uuid == tgt_points_uuid
            tgt_match_condition = tgt_face_vertices_match, tgt_points_match
            #
            if tgt_match_condition == (True, True):
                check_statuses = [bsc_dcc_core.DccMeshCheckStatus.NonChanged]
            elif tgt_match_condition == (True, False):
                check_statuses = [bsc_dcc_core.DccMeshCheckStatus.PointsChanged]
            elif tgt_match_condition == (False, True):
                check_statuses = [bsc_dcc_core.DccMeshCheckStatus.FaceVerticesChanged]
            elif tgt_match_condition == (False, False):
                output_path, check_statuses = self.__get_path_exchanged_()
        else:
            output_path, check_statuses = self.__get_path_changed_()
        #
        check_statuses.sort(key=bsc_dcc_core.DccMeshCheckStatus.All.index)
        return output_path, '+'.join(check_statuses)


class AbsFncRepairerForUsdMesh(object):
    FNC_USD_MESH_CLS = None

    def __init__(self, usd_prim_src, path_tgt, check_statuses):
        self._usd_prim_src = usd_prim_src
        self._path_src = usd_prim_src.GetPath().pathString
        self._path_tgt = path_tgt
        self._check_statuses = check_statuses

    @classmethod
    def delete_fnc(cls, path_tgt):
        cls.FNC_USD_MESH_CLS.delete_fnc(path_tgt)

    @classmethod
    def remove_fnc(cls, path_tgt):
        cls.FNC_USD_MESH_CLS.remove_fnc(path_tgt)

    def execute(self):
        # 1
        if self._check_statuses == '+'.join(
            [
                bsc_dcc_core.DccMeshCheckStatus.FaceVerticesChanged,
                bsc_dcc_core.DccMeshCheckStatus.PointsChanged
            ]
        ):
            self.FNC_USD_MESH_CLS(self._usd_prim_src).do_replace()
        elif self._check_statuses == '+'.join(
            [
                bsc_dcc_core.DccMeshCheckStatus.FaceVerticesChanged
            ]
        ):
            self.FNC_USD_MESH_CLS(self._usd_prim_src).do_replace()
        elif self._check_statuses == '+'.join(
            [
                bsc_dcc_core.DccMeshCheckStatus.PointsChanged
            ]
        ):
            self.FNC_USD_MESH_CLS(self._usd_prim_src).set_points()
        # 2
        elif self._check_statuses == '+'.join(
            [
                bsc_dcc_core.DccMeshCheckStatus.Deletion
            ]
        ):
            self.FNC_USD_MESH_CLS(self._usd_prim_src).set_create()
        #
        elif self._check_statuses == '+'.join(
            [
                bsc_dcc_core.DccMeshCheckStatus.PathChanged
            ]
        ):
            self.FNC_USD_MESH_CLS(self._usd_prim_src).do_repath_to(self._path_tgt)
        elif self._check_statuses == '+'.join(
            [
                bsc_dcc_core.DccMeshCheckStatus.PathChanged,
                bsc_dcc_core.DccMeshCheckStatus.FaceVerticesChanged
            ]
        ):
            self.FNC_USD_MESH_CLS(self._usd_prim_src).do_repath_to(self._path_tgt)
            self.FNC_USD_MESH_CLS(self._usd_prim_src).do_replace(
                keep_materials=True,
                keep_properties=True,
                keep_visibilities=True,
                transfer_uv_maps=True
            )
        elif self._check_statuses == '+'.join(
            [
                bsc_dcc_core.DccMeshCheckStatus.PathChanged,
                bsc_dcc_core.DccMeshCheckStatus.PointsChanged
            ]
        ):
            self.FNC_USD_MESH_CLS(self._usd_prim_src).do_repath_to(self._path_tgt)
            self.FNC_USD_MESH_CLS(self._usd_prim_src).set_points()
        # 3
        elif self._check_statuses == '+'.join(
            [
                bsc_dcc_core.DccMeshCheckStatus.PathExchanged
            ]
        ):
            geometry = AbsFncMatcherForDccMesh._pull_geometry_cache(self._path_src)
            look = AbsFncMatcherForDccMesh._pull_look_cache(self._path_src)
            self.FNC_USD_MESH_CLS(self._usd_prim_src).set_exchange(
                geometry, look
            )
        elif self._check_statuses == '+'.join(
            [
                bsc_dcc_core.DccMeshCheckStatus.PathExchanged,
                bsc_dcc_core.DccMeshCheckStatus.PointsChanged
            ]
        ):
            geometry = AbsFncMatcherForDccMesh._pull_geometry_cache(self._path_src)
            look = AbsFncMatcherForDccMesh._pull_look_cache(self._path_src)
            self.FNC_USD_MESH_CLS(self._usd_prim_src).set_exchange(
                geometry, look
            )
        elif self._check_statuses == '+'.join(
            [
                bsc_dcc_core.DccMeshCheckStatus.PathExchanged,
                bsc_dcc_core.DccMeshCheckStatus.FaceVerticesChanged
            ]
        ):
            geometry = AbsFncMatcherForDccMesh._pull_geometry_cache(self._path_src)
            look = AbsFncMatcherForDccMesh._pull_look_cache(self._path_src)
            self.FNC_USD_MESH_CLS(self._usd_prim_src).set_exchange(
                geometry, look
            )


class AbsFncComparerForUsdGeometry(bsc_fnc_abs_base.AbsFncOptionBase):
    KEY = 'geometry comparer'
    OPTION = dict(
        file_src='',
        file_tgt='',
        location=''
    )
    FNC_MATCHER_FOR_DCC_MESH_CLS = None

    CACHE = dict()

    def __init__(self, option):
        super(AbsFncComparerForUsdGeometry, self).__init__(option)

    @classmethod
    def _generate_data(cls, file_path, location):
        if file_path is not None:
            import lxusd.dcc.objects as usd_dcc_objects

            import lxusd.dcc.operators as usd_dcc_operators

            hash_key = bsc_core.UuidMtd.generate_by_file(file_path)

            if hash_key in cls.CACHE:
                return cls.CACHE[hash_key]

            scene = usd_dcc_objects.Scene()
            scene.load_from_dot_usd(
                file_path,
                location
            )
            universe = scene.universe
            stage_opt = usd_dcc_operators.SceneOpt(scene.usd_stage, 'usd')
            comparer_data = stage_opt.get_mesh_comparer_data(
                file_path
            )
            #
            geometries = []
            mesh_type = universe.get_obj_type('Mesh')
            if mesh_type is not None:
                geometries = mesh_type.get_objs()
            #
            cls.CACHE[hash_key] = geometries, comparer_data
            return geometries, comparer_data

    def __generate_data_fnc(self, file_path, location):
        self._comparer_data.append(
            self._generate_data(file_path, location)
        )

    def __generate_result_fnc(self):
        objs_src, data_src = self._comparer_data[0]
        objs_tgt, data_tgt = self._comparer_data[1]

        if objs_src:
            with bsc_log.LogProcessContext.create(maximum=len(objs_src), label='comparer by data') as g_p:
                for i_obj_src in objs_src:
                    if i_obj_src.type_name == 'Mesh':
                        i_path_src = i_obj_src.path

                        i_matcher_for_mesh = self.FNC_MATCHER_FOR_DCC_MESH_CLS(
                            i_path_src, data_src, data_tgt
                        )
                        i_path_tgt, i_check_statuses = i_matcher_for_mesh.execute()

                        self._comparer_results.append(
                            (i_path_src, i_path_tgt, i_check_statuses)
                        )

                    g_p.do_update()
        # addition
        paths_src = [i.path for i in objs_src]
        paths_tgt = [i.path for i in objs_tgt]
        path_addition = list(
            set(paths_tgt)-set(paths_src)
        )
        for i_path_tgt in path_addition:
            self._comparer_results.append(
                (i_path_tgt, i_path_tgt, bsc_dcc_core.DccMeshCheckStatus.Addition)
            )

    def __generate_results(self):
        self._comparer_data = []
        self._comparer_results = []
        #
        mtds = [
            # gain source data
            (self.__generate_data_fnc, (self.get('file_src'), self.get('location'))),
            # gain target data
            (self.__generate_data_fnc, (self.get('file_tgt'), self.get('location'))),
            # comparer
            (self.__generate_result_fnc, ())
        ]
        if mtds:
            with bsc_log.LogProcessContext.create(maximum=len(mtds), label='geometry comparer') as g_p:
                for i_mtd, i_args in mtds:
                    g_p.do_update()
                    i_mtd(*i_args)
        return self._comparer_results

    def generate_results(self, check_status_includes=None):
        results = self.__generate_results()
        if check_status_includes is not None:
            list_ = []
            for i_path_src, i_path_tgt, i_check_status in results:
                for j_e in check_status_includes:
                    if j_e in i_check_status:
                        list_.append(
                            (i_path_src, i_path_tgt, i_check_status)
                        )
            return list_
        return results


class AbsFncComparerForDccGeometry(bsc_fnc_abs_base.AbsFncOptionBase):
    OPTION = dict(
        file='',
        location='',
        location_source='',
    )

    DCC_SCENE_CLS = None
    DCC_SCENE_OPT_CLS = None

    FNC_MATCHER_FOR_DCC_MESH_CLS = None
    FNC_REPAIRER_FOR_USD_MESH_CLS = None

    CACHE = dict()

    RSV_KEYWORD = 'asset-geometry-usd-payload-file'
    DCC_NAMESPACE = 'usd'

    def __init__(self, option):
        super(AbsFncComparerForDccGeometry, self).__init__(option)
        import lxresolver.core as rsv_core

        self._file_path = self.get('file')
        self._location = self.get('location')
        self._location_source = self.get('location_source')
        #
        self._cache_directory = bsc_core.EnvBaseMtd.get_temporary_root()
        self._resolver = rsv_core.RsvBase.generate_root()
        #
        self._rsv_scene_properties = self._resolver.get_rsv_scene_properties_by_any_scene_file_path(
            file_path=self._file_path
        )
        if self._rsv_scene_properties is not None:
            step = self._rsv_scene_properties.get('step')
            if step in ['mod', 'srf', 'rig', 'grm']:
                keyword = self.RSV_KEYWORD
                rsv_resource = self._resolver.get_rsv_resource(
                    **self._rsv_scene_properties.get_value()
                )
                rsv_model_task = rsv_resource.get_rsv_task(
                    step='mod', task='modeling'
                )
                if rsv_model_task is not None:
                    rsv_unit = rsv_model_task.get_rsv_unit(
                        keyword=keyword
                    )
                    result = rsv_unit.get_result()
                    if result:
                        self.set_source_file(result)
            else:
                raise TypeError()
        else:
            raise TypeError()
        #
        self._init_source_fnc()
        self._init_target_fnc()
        #
        self._results = []

    def set_source_file(self, file_path):
        self._source_file_path = file_path

    def _init_source_fnc(self):
        import lxusd.dcc.objects as usd_dcc_objects
        #
        import lxusd.dcc.operators as usd_dcc_operators

        #
        self._dcc_scene_src = usd_dcc_objects.Scene()
        self._dcc_universe_src = self._dcc_scene_src.universe
        self._dcc_stage_opt_src = usd_dcc_operators.SceneOpt(self._dcc_scene_src.usd_stage, self.DCC_NAMESPACE)
        self._dcc_comparer_data_src = ctt_core.Content(
            value={}
        )
        #
        self._dcc_geometries_src = []

    def _init_target_fnc(self):
        import lxusd.dcc.objects as usd_dcc_objects
        #
        import lxusd.dcc.operators as usd_dcc_operators

        #
        self._dcc_scene_tgt = usd_dcc_objects.Scene()
        self._dcc_universe_tgt = self._dcc_scene_tgt.universe
        self._dcc_stage_opt_tgt = usd_dcc_operators.SceneOpt(self._dcc_scene_tgt.usd_stage, self.DCC_NAMESPACE)
        self._dcc_comparer_data_tgt = ctt_core.Content(
            value={}
        )
        #
        self._dcc_geometries_tgt = []

    def _update_source_fnc(self):
        import lxusd.dcc.objects as usd_dcc_objects
        #
        import lxusd.dcc.operators as usd_dcc_operators

        #
        usd_file_path = self._source_file_path
        if usd_file_path is not None:
            hash_key = bsc_core.UuidMtd.generate_by_file(usd_file_path)
            if hash_key in AbsFncComparerForDccGeometry.CACHE:
                self._dcc_scene_src = AbsFncComparerForDccGeometry.CACHE[hash_key]
                self._dcc_universe_src = self._dcc_scene_src.universe
            else:
                self._dcc_scene_src = usd_dcc_objects.Scene()
                self._dcc_scene_src.load_from_dot_usd(
                    usd_file_path,
                    self._location,
                    self._location_source
                )
                AbsFncComparerForDccGeometry.CACHE[hash_key] = self._dcc_scene_src
                self._dcc_universe_src = self._dcc_scene_src.universe
            #
            self._dcc_stage_opt_src = usd_dcc_operators.SceneOpt(self._dcc_scene_src.usd_stage, self.DCC_NAMESPACE)
            self._dcc_comparer_data_src = self._dcc_stage_opt_src.get_mesh_comparer_data(
                usd_file_path
            )
            #
            self._dcc_geometries_src = []
            mesh_type = self._dcc_universe_src.get_obj_type('Mesh')
            if mesh_type is not None:
                self._dcc_geometries_src = mesh_type.get_objs()

    def _update_target_fnc(self):
        scene_file_path = self._file_path
        location = self._location
        #
        self._dcc_scene_tgt = self.DCC_SCENE_CLS()
        self._dcc_scene_tgt.load_from_location(location, include_obj_type=['mesh'])
        self._dcc_universe_tgt = self._dcc_scene_tgt.universe
        self._dcc_stage_opt_tgt = self.DCC_SCENE_OPT_CLS(self._dcc_universe_tgt)
        self._dcc_comparer_data_tgt = self._dcc_stage_opt_tgt.get_mesh_comparer_data(scene_file_path)
        #
        self._dcc_geometries_tgt = []
        mesh_type = self._dcc_universe_tgt.get_obj_type('mesh')
        if mesh_type is not None:
            self._dcc_geometries_tgt = mesh_type.get_objs()

    def get_geometry_src(self, dcc_geometry_path):
        return self._dcc_universe_src.get_obj(dcc_geometry_path)

    def get_geometry_tgt(self, dcc_geometry_path):
        return self._dcc_universe_tgt.get_obj(dcc_geometry_path)

    def do_match_mesh(self, path_src):
        data_src = self._dcc_comparer_data_src
        data_tgt = self._dcc_comparer_data_tgt
        return self.FNC_MATCHER_FOR_DCC_MESH_CLS(
            path_src, data_src, data_tgt
        ).execute()

    def do_repair_mesh(self, path_src, path_tgt, check_statuses):
        # print path_src
        usd_prim_src = self._dcc_scene_src.usd_stage.GetPrimAtPath(path_src)
        if usd_prim_src.IsValid() is True:
            self.FNC_REPAIRER_FOR_USD_MESH_CLS(
                usd_prim_src, path_tgt, check_statuses
            ).execute()
        else:
            if check_statuses == '+'.join(
                [
                    bsc_dcc_core.DccMeshCheckStatus.Addition
                ]
            ):
                self.FNC_REPAIRER_FOR_USD_MESH_CLS.delete_fnc(path_tgt)

    def generate_results(self):
        list_ = []

        methods = [
            self._update_source_fnc,
            self._update_target_fnc
        ]
        if methods:
            with bsc_log.LogProcessContext.create(
                maximum=len(methods), label='execute geometry-comparer method'
            ) as g_p:
                for i_mtd in methods:
                    g_p.do_update()
                    i_mtd()

        geometries_src = self._dcc_geometries_src
        geometries_tgt = self._dcc_geometries_tgt

        dcc_geometry_paths = []
        if geometries_src:
            with bsc_log.LogProcessContext.create(
                maximum=len(geometries_src), label='gain geometry-comparer result'
            ) as g_p:
                for i_geometry_src in geometries_src:
                    g_p.do_update()
                    if i_geometry_src.type_name == 'Mesh':
                        i_mesh_path_src = i_geometry_src.path
                        i_mesh_path_tgt, i_check_statuses = self.do_match_mesh(path_src=i_mesh_path_src)
                        list_.append(
                            (i_mesh_path_src, i_mesh_path_tgt, i_check_statuses)
                        )
                        dcc_geometry_paths.append(i_mesh_path_tgt)
        # addition
        dcc_geometry_paths_src = [i.path for i in geometries_src]
        dcc_geometry_paths_tgt = [i.path for i in geometries_tgt]
        geometry_paths_addition = list(set(dcc_geometry_paths_tgt)-set(dcc_geometry_paths_src)-set(dcc_geometry_paths))
        for i_geometry_path_tgt in geometry_paths_addition:
            list_.append(
                (i_geometry_path_tgt, i_geometry_path_tgt, bsc_dcc_core.DccMeshCheckStatus.Addition)
            )
        return list_
