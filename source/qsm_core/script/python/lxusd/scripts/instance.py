# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage
# usd
from .. import core as usd_core


class ScpInstance(object):
    KEY = 'instance color map generate'

    def __init__(self, grow_usd_file_path, instance_usd_file_path):
        self._grow_usd_file_path = grow_usd_file_path
        self._instance_usd_file_path = instance_usd_file_path

    def get_hash_key(self):
        pass

    @classmethod
    def generate_grow_cache(
        cls,
        grow_usd_file_path, image_file_path, uv_map_name,
        cache_usd_file_path
    ):
        grow_usd_stage_opt = usd_core.UsdStageOpt()

        grow_usd_stage_opt.append_sublayer(grow_usd_file_path)
        mesh_prims = grow_usd_stage_opt.get_all_mesh_objs()

        cache_usd_opt = usd_core.UsdStageOpt()
        with bsc_log.LogProcessContext.create_as_bar(maximum=len(mesh_prims), label='generator grow cache') as g_p:
            for i_seq, i_prim in enumerate(mesh_prims):
                i_mesh_opt = usd_core.UsdMeshOpt(i_prim)

                cache_usd_opt.create_one('/grow_preview', 'Xform')

                i_points_p = cache_usd_opt.create_one('/grow_preview/points_{}'.format(i_seq), 'Points')
                i_points_opt = usd_core.UsdPointsOpt(i_points_p)

                i_points = i_mesh_opt.compute_face_points()
                i_colors = i_mesh_opt.compute_face_colors_from_image(image_file_path, uv_map_name)

                i_points_opt.set_points(i_points)
                i_points_opt.set_widths([5.0]*len(i_points))
                i_points_opt.set_display_colors_as_vertex(i_colors)

                g_p.do_update()

        cache_usd_opt.export_to(cache_usd_file_path)

    @classmethod
    def generate_instance_cache(
        cls,
        grow_usd_file_path, instance_usd_file_path, image_file_path, uv_map_name,
        cache_usd_file_path, cache_json_file_path
    ):
        grow_usd_stage_opt = usd_core.UsdStageOpt(grow_usd_file_path)
        instance_usd_stage_opt = usd_core.UsdStageOpt(instance_usd_file_path)
        mesh_prims = grow_usd_stage_opt.get_all_mesh_objs()
        mesh_opt_dict = {}
        for i_mesh_prim in mesh_prims:
            i_mesh_opt = usd_core.UsdMeshOpt(i_mesh_prim)
            mesh_opt_dict[i_mesh_opt.get_path()] = i_mesh_opt

        cache_usd_opt = usd_core.UsdStageOpt()

        image_opt = usd_core.ImageOpt(image_file_path)

        color_dict = {}
        instance_prims = instance_usd_stage_opt.get_all_instance_objs()
        with bsc_log.LogProcessContext.create_as_bar(maximum=len(instance_prims), label='generator instance cache') as g_p:
            for i_seq, i_instance_prim in enumerate(instance_prims):
                i_instance_opt = usd_core.UsdInstancerOpt(i_instance_prim)
                i_matched_point_p = cache_usd_opt.create_one(
                    '/instance_preview/points_{}'.format(i_seq), 'Points'
                )
                i_matched_point_opt = usd_core.UsdPointsOpt(i_matched_point_p)
                i_points = i_instance_opt.get_positions()
                i_matched_point_opt.set_points(i_points)
                i_p_c = len(i_points)
                i_point_all_indices = range(i_p_c)
                i_color_dict = {}
                if not i_instance_opt.find_ancestors(['PointInstancer']):
                    i_point_dict = {_j: _j_seq for _j_seq, _j in enumerate(i_points)}
                    i_points_remaining = {_j: _j_seq for _j_seq, _j in enumerate(i_points)}

                    bsc_log.Log.trace_method_result(cls.KEY, 'start instance: "{}"'.format(i_instance_opt.get_path()))
                    bsc_log.Log.trace_method_result(cls.KEY, 'point count: {}'.format(i_p_c))
                    for j_seq, j_mesh_prim in enumerate(mesh_prims):
                        if i_points_remaining:
                            j_prim_opt = usd_core.UsdPrimOpt(j_mesh_prim)
                            j_key = j_prim_opt.get_path()
                            j_mesh_opt = mesh_opt_dict[j_key]
                            bsc_log.Log.trace_method_result(cls.KEY, 'start mesh: "{}"'.format(j_mesh_opt.get_path()))

                            j_mesh_face_extra = j_mesh_opt.generate_face_extra(uv_map_name)
                            j_face_points_kd_tree = j_mesh_opt.generate_face_points_kd_tree()
                            j_b_box_range = j_mesh_opt.generate_b_box_range()

                            j_points = i_points_remaining.keys()
                            j_contain_points = j_b_box_range.compute_contain_elements(j_points)
                            if j_contain_points:
                                j_contain_point_index_dict = {_j_seq: _j for _j_seq, _j in enumerate(j_contain_points)}
                                j_face_indices = j_face_points_kd_tree.compute_closed_indexes(
                                    j_contain_points, distance_tolerance=10.0
                                )
                                if j_face_indices:
                                    j_points_closed = []
                                    for k_seq, k_face_index in enumerate(j_face_indices):
                                        if k_face_index is not None:
                                            k_point = j_contain_point_index_dict[k_seq]
                                            k_point_index = i_point_dict[k_point]
                                            j_points_closed.append(k_point)
                                            k_coord = j_mesh_face_extra.compute_uv_coord_at(k_face_index, k_point)
                                            if k_coord:
                                                k_u, k_v = k_coord
                                                k_rgb = image_opt.get_rgb_at_coord(k_u, k_v, maximum=1.0)
                                                i_color_dict[k_point_index] = k_rgb
                                            else:
                                                i_color_dict[k_point_index] = (0, 0, 0)

                                    [i_points_remaining.pop(_k) for _k in j_points_closed]
                else:
                    bsc_log.Log.trace_method_warning(
                        cls.KEY, 'instance is nested: "{}"'.format(i_instance_opt.get_path())
                    )

                i_colors = [i_color_dict[_i] if _i in i_color_dict else (0, 0, 0) for _i in i_point_all_indices]
                cache_usd_opt.create_one('/instance_preview', 'Xform')
                i_matched_point_opt.set_display_colors_as_vertex(i_colors)
                i_matched_point_opt.set_widths([5.0]*len(i_points))
                color_dict[i_instance_opt.get_path()] = usd_core.UsdBase.to_point_array(i_colors)

                g_p.do_update()

        bsc_storage.StgFileOpt(cache_json_file_path).set_write(
            color_dict
        )

        cache_usd_opt.export_to(
            cache_usd_file_path
        )


if __name__ == '__main__':
    bsc_log.Log.DEBUG = True
    bsc_log.Log.TEST = True

    # ScpInstance.generate_grow_cache(
    #     '/l/prod/cgm/work/assets/env/env_waterfall/srf/surfacing/maya/scenes/usd/env_waterfall_002.usd',
    #     '/data/e/workspace/lynxi/test/maya/vertex-color/test.<udim>.jpg',
    #     'st',
    #     '/data/e/workspace/lynxi/test/maya/vertex-color/test_grow_color_map.usd'
    # )

    ScpInstance.generate_instance_cache(
        '/l/prod/cgm/work/assets/env/env_waterfall/srf/surfacing/maya/scenes/usd/env_waterfall_002.usd',
        '/l/prod/cgm/work/assets/env/env_waterfall/srf/surfacing/clarisse/plants_038.fix.usd',
        '/data/e/workspace/lynxi/test/maya/vertex-color/test.<udim>.jpg',
        'st',
        '/data/e/workspace/lynxi/test/maya/vertex-color/test_instance_color_map.usd',
        '/data/e/workspace/lynxi/test/maya/vertex-color/test_instance_color_map.json'
    )
