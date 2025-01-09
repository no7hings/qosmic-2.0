# coding:utf-8
import lxbasic.core as bsc_core

import lxusd.core as usd_core

import random


def main():

    random.seed(0)

    s_o = usd_core.UsdStageOpt(
        '/data/e/workspace/lynxi/test/maya/vertex-color/test_plane_2.usda'
    )

    m_p = s_o.get_obj('/pPlane1/pPlaneShape1')

    mesh_opt = usd_core.UsdMeshOpt(m_p)

    (x, y, z), (c_x, c_y, c_z), (w, h, d) = mesh_opt.compute_geometry_args()

    i_color_map = mesh_opt.compute_vertex_color_map_from_image(
        '/data/e/workspace/lynxi/test/maya/vertex-color/test.<udim>.jpg', 'st'
    )
    mesh_opt.set_display_colors_as_vertex(i_color_map)
    image_opt = usd_core.ImageOpt('/data/e/workspace/lynxi/test/maya/vertex-color/test.<udim>.jpg')

    m = 100.0

    xs, ys, zs = range(int(w*m)), range(10), range(int(d*m))

    v_c = 100

    check_points = []
    for i in range(v_c):
        i_x, i_y, i_z = random.choice(xs)/m, random.choice(ys)/m, random.choice(zs)/m
        check_points.append(usd_core.Gf.Vec3f((i_x+x, i_y, i_z+z)))

    mesh_face_extra = mesh_opt.generate_face_extra('st')

    kd_tree = mesh_opt.generate_face_points_kd_tree()

    face_indices = kd_tree.compute_closed_indexes(check_points, distance_tolerance=.2)

    project_points = []
    project_colors = []

    check_colors = []

    uv_points = []

    for i_seq, i_face_index in enumerate(face_indices):
        if i_face_index is not None:
            i_check_point = check_points[i_seq]

            i_project_point = mesh_face_extra.compute_project_point_at(i_face_index, i_check_point)
            i_coord = mesh_face_extra.compute_uv_coord_at(i_face_index, i_check_point)
            if i_coord:
                i_u, i_v = i_coord
                i_rgb = image_opt.get_rgb_at_coord(i_u, i_v, maximum=1.0)
                check_colors.append(i_rgb)
                uv_points.append(usd_core.Gf.Vec3f(i_v, .01, i_u))
            else:
                pass

            project_points.append(i_project_point)
            project_colors.append((0, 0, 0))
        else:
            check_colors.append((0, 0, 0))
            project_points.append((0, 0, 0))
            project_colors.append((0, 0, 0))

    check_prim = s_o.create_one(
        '/pPlane1/check_points', 'Points'
    )
    check_point_opt = usd_core.UsdPointsOpt(check_prim)
    check_point_opt.set_points(check_points)
    check_point_opt.set_widths([0.1]*len(check_points))
    check_point_opt.set_display_colors_as_vertex(check_colors)

    project_prim = s_o.create_one(
        '/pPlane1/project_points', 'Points'
    )
    project_point_opt = usd_core.UsdPointsOpt(project_prim)
    project_point_opt.set_points(project_points)
    project_point_opt.set_widths([0.1]*len(project_points))
    project_point_opt.set_display_colors_as_vertex(project_colors)

    s_o.export_to(
        '/data/e/workspace/lynxi/test/maya/vertex-color/test_plane_2.points.usda'
    )


if __name__ == '__main__':
    main()
