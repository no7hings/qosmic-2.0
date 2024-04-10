# coding:utf-8
import copy

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# usd
from .. import core as usd_core


class ShotUsdCombine(object):
    def __init__(self, file_path_src, location):
        self._file_path_src = file_path_src
        self._location = location

    @classmethod
    def _get_tmp_file_(cls, file_path_src):
        user_directory_path = bsc_storage.StgTmpBaseMtd.get_user_directory('shot-usd-combine')
        return '{}/{}.usda'.format(
            user_directory_path,
            bsc_core.TimestampOpt(
                bsc_storage.StgFileOpt(file_path_src).get_modify_timestamp()
            ).get_as_tag_36()
        )

    def set_run(self):
        file_path_src = self._file_path_src
        file_path_tgt = self._get_tmp_file_(file_path_src)
        location = self._location

        usd_stage_opt = usd_core.UsdStageOpt(file_path_src)

        usd_prim = usd_stage_opt.get_obj(location)

        prim_opt = usd_core.UsdPrimOpt(usd_prim)

        list_ = []
        cs = prim_opt.get_children()
        with bsc_log.LogProcessContext.create_as_bar(maximum=len(cs), label='usd combine') as l_p:
            for i_prim in cs:
                l_p.do_update()
                #
                i_prim_opt = usd_core.UsdPrimOpt(i_prim)
                i_port = i_prim_opt.get_port('userProperties:pgOpIn:usd:opArgs:fileName')
                i_path = i_prim_opt.get_path()
                list_.append(
                    i_path
                )
                if i_port is None:
                    bsc_log.Log.trace_error(
                        'attribute="{}.fileName" is non-exists'.format(i_path)
                    )
                    continue
                if i_port.Get() is None:
                    bsc_log.Log.trace_error(
                        'attribute="{}.fileName" is non-data'.format(i_path)
                    )
                    continue
                i_file_path = i_port.Get().resolvedPath

                i_yaml_file_path = bsc_storage.StgTmpYamlMtd.get_file_path(
                    i_file_path, 'usd-hierarchy-cacher'
                )
                i_yaml_file_opt = bsc_storage.StgFileOpt(i_yaml_file_path)
                if i_yaml_file_opt.get_is_exists() is True:
                    i_list = i_yaml_file_opt.set_read()
                    list_.extend([i_path+j for j in i_list])
                else:
                    i_file_path_ = bsc_storage.StgFileMtdForMultiply.convert_to(
                        i_file_path, ['*.####.{format}']
                    )
                    i_file_tile_paths = bsc_storage.StgFileMtdForMultiply.get_exists_unit_paths(
                        i_file_path_
                    )
                    i_list = []
                    for j_file_path in i_file_tile_paths:
                        j_stage_opt = usd_core.UsdStageOpt(j_file_path)
                        j_rls_paths = j_stage_opt.get_all_obj_paths()
                        i_list.extend(j_rls_paths)
                    #
                    i_list_ = list(set(i_list))
                    i_list_.sort(key=i_list.index)
                    #
                    bsc_storage.StgFileOpt(i_yaml_file_path).set_write(
                        i_list_
                    )
                    #
                    list_.extend([i_path+j for j in i_list_])

        file_write_opt = usd_core.UsdFileWriteOpt(file_path_tgt)

        file_write_opt.set_location_add(location)

        with bsc_log.LogProcessContext.create_as_bar(maximum=len(list_), label='usd create') as l_p:
            for i in list_:
                l_p.do_update()
                file_write_opt.set_obj_add(i)

        file_write_opt.set_save()
        return file_path_tgt


class UsdMeshSubdiv(object):
    OPTION = dict(
        root_prefix_src='',
        root_prefix_tgt=''
    )

    def __init__(self, file_path_src, file_path_tgt, option=None):
        self._file_path_src = file_path_src
        self._file_path_tgt = file_path_tgt

        self._option = copy.copy(self.OPTION)
        if option is not None:
            self._option.update(option)

    @classmethod
    def _get_face_count_tuple_(cls, face_counts):
        list_ = []
        keys = list(set(face_counts))
        keys.sort()
        for i_key in keys:
            list_.append((i_key, face_counts.count(i_key)))
        return tuple(list_)

    @classmethod
    def _get_subdiv_face_count_(cls, face_count_tuple, subdiv_count):
        def rcs_fnc_(face_count_tuple_):
            return ((4, sum([_i_key*_i_count for _i_key, _i_count in face_count_tuple_])),)

        face_count_tuple__ = face_count_tuple
        for i in range(subdiv_count):
            face_count_tuple__ = rcs_fnc_(face_count_tuple__)

        return face_count_tuple__

    def _get_face_count_dict_(self, usd_stage, root_prefix):
        dict_ = {}
        # usd_stage.Flatten()
        for i_usd_prim in usd_stage.TraverseAll():
            if i_usd_prim.GetTypeName() == 'Mesh':
                i_usd_mesh = usd_core.UsdGeom.Mesh(i_usd_prim)
                i_path = i_usd_prim.GetPath().pathString
                a = i_usd_mesh.GetFaceVertexCountsAttr()
                if a.GetNumTimeSamples():
                    i_counts = a.Get(0)
                else:
                    i_counts = a.Get()
                dict_[root_prefix+i_path] = self._get_face_count_tuple_(list(i_counts))
        return dict_

    def _get_subdiv_dict_(self, dict_src, dict_tgt):
        dict_ = {}
        for k, v in dict_src.items():
            if k in dict_tgt:
                i_face_count_src = v
                i_face_count_tgt = dict_tgt[k]
                if i_face_count_src != i_face_count_tgt:
                    for j_subdiv in range(1, 5):
                        j_count_src = sum(
                            [j_c for j_k, j_c in self._get_subdiv_face_count_(i_face_count_src, j_subdiv)]
                            )
                        j_count_tgt = sum([j_c for j_k, j_c in i_face_count_tgt])
                        if j_count_src == j_count_tgt:
                            dict_[k] = j_subdiv
                            break
                        elif j_count_src > j_count_tgt:
                            break
        return dict_

    def set_run(self):
        self._stage_src = usd_core.UsdStageOpt(
            self._file_path_src
        )
        self._root_src_prefix = self._option.get('root_prefix_src')
        self._stage_tgt = usd_core.UsdStageOpt(
            self._file_path_tgt
        )
        self._root_tgt_prefix = self._option.get('root_prefix_tgt')

        dict_src = self._get_face_count_dict_(
            self._stage_src._usd_stage, self._root_src_prefix
        )
        dict_tgt = self._get_face_count_dict_(
            self._stage_tgt._usd_stage, self._root_tgt_prefix
        )

        self._subdiv_dict = self._get_subdiv_dict_(dict_src, dict_tgt)

        print self._subdiv_dict


class UsdMeshCompare(object):
    OPTION = dict()

    def __init__(self, file_path_src, file_path_tgt, option=None):
        self._file_path_src = file_path_src
        self._file_path_tgt = file_path_tgt

        self._option = copy.copy(self.OPTION)
        if option is not None:
            self._option.update(option)

    def test(self):
        import lxusd.dcc.objects as usd_dcc_objects

        import lxusd.dcc.operators as usd_dcc_operators

        s_src = usd_dcc_objects.Scene()
        s_src.load_from_dot_usd(self._file_path_src, '/master')

        s_tgt = usd_dcc_objects.Scene()
        s_tgt.load_from_dot_usd(self._file_path_tgt, '/master')

        n = 'L_legorna_002_hiShape'

        m_src = s_src.universe.get_obj(n)

        m_tgt = s_tgt.universe.get_obj(n)

        m_opt_src = usd_dcc_operators.MeshOpt(
            m_src._usd_obj
        )

        m_opt_tgt = usd_dcc_operators.MeshOpt(
            m_tgt._usd_obj
        )

        # a_src = m_opt_src.get_face_vertex_indices()
        # bsc_storage.StgFileOpt('/data/f/usd_uv_map_export_test/a_0.yml').set_write(a_src)
        # a_tgt = m_opt_tgt.get_face_vertex_indices()
        # bsc_storage.StgFileOpt('/data/f/usd_uv_map_export_test/a_1.yml').set_write(a_tgt)
        print m_opt_src.get_face_vertices_as_uuid()
        print m_opt_tgt.get_face_vertices_as_uuid()
        print len(m_opt_src.get_face_vertex_counts())
        print len(m_opt_tgt.get_face_vertex_counts())


if __name__ == '__main__':
    pass
