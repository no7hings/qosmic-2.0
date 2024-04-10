# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# usd
from .. import core as usd_core


class UsdScpForClarisseCleanup(object):
    KEY = 'clarisse USD transfer'

    def __init__(self, file_path):
        self._file_path = file_path
        f_o = bsc_storage.StgFileOpt(self._file_path)
        self._file_path_out = '{}.fix{}'.format(
            f_o.path_base, f_o.ext
        )
        self._file_path_out_usd = '{}.fix.usd'.format(
            f_o.path_base
        )
        self._file_path_out_usda = '{}.fix.usda'.format(
            f_o.path_base
        )
        self._stage_opt = usd_core.UsdStageOpt(self._file_path)
        self._stage_opt_new = usd_core.UsdStageOpt()

    @staticmethod
    def __filter_fnc(marks, path):
        for i_path in marks:
            if path.startswith(i_path) is True:
                return True
        return False

    def transfer(self):
        marks = []
        prims = self._stage_opt.get_all_objs()
        c = len(prims)
        with bsc_log.LogProcessContext.create(maximum=c, label='transfer process') as g_p:
            for i_prim in prims:
                i_prim_opt = usd_core.UsdPrimOpt(i_prim)
                if self.__filter_fnc(marks, i_prim_opt.get_path()) is True:
                    continue

                if i_prim_opt.get_type_name() == 'PointInstancer':
                    self.__instancer_process(i_prim)
                    marks.append(i_prim_opt.get_path())
                elif i_prim_opt.get_type_name() == 'Mesh':
                    self.__mesh_process(i_prim)
                    marks.append(i_prim_opt.get_parent_path())

                # g_p.set_update()

    def __instancer_process(self, instancer_prim):
        instancer_opt = usd_core.UsdInstancerOpt(instancer_prim)
        proto_indices = instancer_opt.get_proto_indices()
        if proto_indices:
            group_prim = instancer_opt.get_parent()
            group_prim_new = self._stage_opt_new.copy_dag_from(group_prim)
            group_opt_new = usd_core.UsdTransformOpt(group_prim_new)
            instancer_prim_new = group_opt_new.create_child(instancer_opt.get_name(), 'PointInstancer')
            instance_opt_new = usd_core.UsdInstancerOpt(instancer_prim_new)
            instance_opt_new.set_proto_indices(proto_indices)

            self.__instancer_protos_process(instancer_opt, instance_opt_new)

            self.__generate_instancer_proxy(instancer_prim_new)

            if not instancer_opt.find_descendants(['PointInstancer']):
                self.__generate_instancer_properties(instancer_prim_new)

    def __mesh_process(self, mesh_prim):
        reference_file_path = self.__find_mesh_valid_reference(mesh_prim)
        if reference_file_path is not None:
            reference_file_path = reference_file_path. \
                replace('/geometry/abc', '/geometry/usd'). \
                replace('.abc', '.usd')

            obj_opt = usd_core.UsdPrimOpt(mesh_prim)
            group_prim = obj_opt.get_parent()
            group_prim_new = self._stage_opt_new.copy_dag_from(group_prim)
            group_opt_new = usd_core.UsdTransformOpt(group_prim_new)
            group_opt_new.add_reference(reference_file_path)
            group_opt_new.create_customize_attribute('usd_file', reference_file_path)
            group_opt_new.set_kind(usd_core.Kind.Tokens.component)

    def __find_mesh_valid_reference(self, mesh_prim):
        obj_opt = usd_core.UsdPrimOpt(mesh_prim)
        all_references = obj_opt.get_all_references()
        for i_reference in all_references:
            i_path, i_file_path = i_reference
            if i_file_path != self._file_path:
                return i_file_path
        return None

    def __instancer_protos_process(self, instancer_opt, instance_opt_new):
        protos_prims_new = []
        group_prim_new = instance_opt_new.create_child('protos', 'Xform')
        group_opt_new = usd_core.UsdPrimOpt(group_prim_new)
        for i_prim in instancer_opt.get_proto_prims():
            i_proto_opt = usd_core.UsdPrimOpt(i_prim)
            if i_proto_opt.get_type_name() == 'PointInstancer':
                i_instancer_prim = i_prim
                i_instancer_opt = usd_core.UsdInstancerOpt(i_instancer_prim)
                if i_instancer_opt.get_proto_indices():
                    i_proto_prim_new = self._stage_opt_new.copy_one_from(
                        i_prim, '{}/{}'.format(group_opt_new.get_path(), i_proto_opt.get_name())
                    )
                    self.__instancer_proto_process(i_prim, i_proto_prim_new)
                else:
                    i_proto_prim_new = self._stage_opt_new.copy_one_from(
                        i_prim, '{}/{}'.format(group_opt_new.get_path(), i_proto_opt.get_name()), 'Xform'
                    )
                protos_prims_new.append(i_proto_prim_new)
            else:
                if i_proto_opt.get_type_name() == 'Xform':
                    i_proto_prim_new = self._stage_opt_new.copy_one_from(
                        i_prim, '{}/{}'.format(group_opt_new.get_path(), i_proto_opt.get_name())
                    )
                    self._stage_opt_new.copy_prim_attributes_fnc(i_prim, i_proto_prim_new)
                    self.__instancer_proto_other_process(i_prim, i_proto_prim_new)
                else:
                    i_proto_prim_new = self._stage_opt_new.copy_one_from(
                        i_prim, '{}/{}'.format(group_opt_new.get_path(), i_proto_opt.get_name()), 'Xform'
                    )
                protos_prims_new.append(i_proto_prim_new)

        instance_opt_new.set_proto_prims(protos_prims_new)

        positions = instancer_opt.get_positions()
        if positions:
            instance_opt_new.set_positions(
                positions
            )
        orientations = instancer_opt.get_orientations()
        if orientations:
            instance_opt_new.set_orientations(
                orientations
            )
        scales = instancer_opt.get_scales()
        if scales:
            instance_opt_new.set_scales(
                scales
            )

    def __instancer_proto_process(self, instancer_prim, instancer_prim_new):
        instancer_opt = usd_core.UsdInstancerOpt(instancer_prim)
        proto_indices = instancer_opt.get_proto_indices()
        if proto_indices:
            instance_opt_new = usd_core.UsdInstancerOpt(instancer_prim_new)
            instance_opt_new.set_proto_indices(proto_indices)
            self.__instancer_protos_process(instancer_opt, instance_opt_new)

    def __instancer_proto_other_process(self, proto_prim, proto_prim_new):
        proto_prim_opt = usd_core.UsdPrimOpt(proto_prim)
        prims = proto_prim_opt.get_descendants()
        marks = []
        for i_prim in prims:
            i_prim_opt = usd_core.UsdPrimOpt(i_prim)
            if self.__filter_fnc(marks, i_prim_opt.get_path()) is True:
                continue
            if i_prim_opt.get_type_name() == 'Mesh':
                self.__instancer_proto_mesh_process(proto_prim_new, i_prim)
                marks.append(i_prim_opt.get_parent_path())

    def __instancer_proto_mesh_process(self, proto_prim_new, mesh_prim):
        reference_file_path = self.__find_mesh_valid_reference(mesh_prim)
        if reference_file_path is not None:
            reference_file_path = reference_file_path. \
                replace('/geometry/abc', '/geometry/usd'). \
                replace('.abc', '.usd')
            proto_opt_new = usd_core.UsdTransformOpt(proto_prim_new)
            proto_opt_new.add_reference(reference_file_path)
            proto_opt_new.create_customize_attribute('usd_file', reference_file_path)
            proto_opt_new.set_kind(usd_core.Kind.Tokens.component)

    def __generate_instancer_properties(self, instancer_prim_new):
        opt = usd_core.UsdInstancerOpt(instancer_prim_new)

        proto_indices = opt.get('protoIndices')
        if proto_indices:
            c = len(proto_indices)
            geometries = []
            for i_prim in opt.get_proto_prims():
                i_opt = usd_core.UsdTransformOpt(i_prim)
                i_usd_file_path = i_opt.get_customize_attribute('usd_file')
                if i_usd_file_path is not None:
                    geometries.append(i_opt.compute_geometry_args())
                else:
                    geometries.append(None)
            # translate
            translates = opt.get('positions')
            if not translates:
                translates = usd_core.Vt.QuathArray([usd_core.Gf.Vec3f((0, 0, 0))]*c)
            opt.create_primvar_as_point_as_uniform(
                'ist_translate',
                translates
            )

            # rotate
            orientations = opt.get('orientations')
            if not orientations:
                orientations = usd_core.Vt.QuathArray([usd_core.Gf.Quath(1, (0, 0, 0))]*c)

            dimensions = []
            for i_index in range(c):
                i_proto_index = proto_indices[i_index]
                i_geometry = geometries[i_proto_index]
                if i_geometry is not None:
                    dimensions.append(usd_core.Gf.Vec3f(*i_geometry[2]))
                else:
                    dimensions.append(usd_core.Gf.Vec3f(0, 0, 0))

            opt.create_primvar_as_point_as_uniform(
                'ist_dimensions', dimensions
            )
            opt.create_primvar_as_point_as_uniform(
                'ist_rotate', map(lambda x: tuple(usd_core.UsdQuaternion(x).to_rotate()), orientations)
            )
            opt.create_primvar_as_point_as_uniform(
                'ist_axis', map(lambda x: tuple(usd_core.UsdQuaternion(x).to_axis()), orientations)
            )
            opt.create_primvar_as_float_as_uniform(
                'ist_angle', map(lambda x: usd_core.UsdQuaternion(x).to_angle(), orientations)
            )
            # scale
            scales = opt.get('scales')
            if not scales:
                scales = usd_core.Vt.Vec3fArray([usd_core.Gf.Vec3f((1, 1, 1))]*c)
            opt.create_primvar_as_point_as_uniform('ist_scale', scales)
            # id
            proto_indices = opt.get('protoIndices')
            opt.create_primvar_as_integer_as_uniform('ist_id', range(len(proto_indices)))
            return opt.create_child('protos', 'Xform')
        else:
            bsc_log.Log.trace_method_warning(
                self.KEY, 'instance error: proto is not found for "{}"'.format(opt.get_path())
            )

    @staticmethod
    def __generate_instancer_proxy(instancer_prim_new):
        opt = usd_core.UsdInstancerOpt(instancer_prim_new)

        c_widths = []
        c_points = []
        c_counts = []
        c_colors = []

        geometries = []
        for i_prim in opt.get_proto_prims():
            i_opt = usd_core.UsdTransformOpt(i_prim)
            i_usd_file_path = i_opt.get_customize_attribute('usd_file')
            if i_usd_file_path is not None:
                geometries.append(i_opt.compute_geometry_args())
            else:
                geometries.append(None)

        proto_indices = opt.get('protoIndices')
        if proto_indices:
            c = len(proto_indices)
            translates = opt.get('positions')
            if not translates:
                translates = usd_core.Vt.QuathArray([usd_core.Gf.Vec3f((0, 0, 0))]*c)
            orientations = opt.get('orientations')
            if not orientations:
                orientations = usd_core.Vt.QuathArray([usd_core.Gf.Quath(1, (0, 0, 0))]*c)
            scales = opt.get('scales')
            if not scales:
                scales = usd_core.Vt.Vec3fArray([usd_core.Gf.Vec3f((1, 1, 1))]*c)

            c_r = bsc_core.RawRgbRange(c)

            for i_index, i_center in enumerate(translates):
                i_proto_index = proto_indices[i_index]
                i_geometry = geometries[i_proto_index]
                if i_geometry is None:
                    continue

                i_orientation = orientations[i_index]
                i_scale = scales[i_index]
                i_size = i_geometry[2]
                i_rgb = c_r.get_rgb(i_index, maximum=1.0)
                i_x, i_y, i_z = i_center
                i_w, i_h, i_d = i_size
                i_w, i_h, i_d = i_w, i_h, i_d
                i_transformation_matrix = usd_core.UsdTransformation(
                    i_center, i_orientation, i_scale
                ).to_matrix()
                # y line
                i_p_y_o = usd_core.Gf.Vec3f(i_x, i_y+i_h, i_z)
                i_p_y = i_transformation_matrix.Transform(i_p_y_o)
                i_points_y = [i_center, i_center, i_p_y, i_p_y]
                c_points.extend(i_points_y)
                c_counts.append(len(i_points_y))
                c_widths.append(0.003)
                c_colors.append(i_rgb)
                # z line
                i_p_z_o = usd_core.Gf.Vec3f(i_x, i_y, i_z+i_d/2)
                i_p_z = i_transformation_matrix.Transform(i_p_z_o)
                i_points_z = [i_center, i_center, i_p_z, i_p_z]
                c_points.extend(i_points_z)
                c_counts.append(len(i_points_z))
                c_widths.append(0.003)
                c_colors.append(i_rgb)
                # cross line
                i_p_cross_p_0_0_o = usd_core.Gf.Vec3f(i_x-i_w/2, i_y, i_z-i_d/2)
                i_p_cross_p_0_1_o = usd_core.Gf.Vec3f(i_x+i_w/2, i_y, i_z+i_d/2)
                i_p_cross_p_0_0 = i_transformation_matrix.Transform(i_p_cross_p_0_0_o)
                i_p_cross_p_0_1 = i_transformation_matrix.Transform(i_p_cross_p_0_1_o)
                i_points_cross_0 = [i_p_cross_p_0_0, i_p_cross_p_0_0, i_p_cross_p_0_1, i_p_cross_p_0_1]
                c_points.extend(i_points_cross_0)
                c_counts.append(len(i_points_cross_0))
                c_widths.append(0.003)
                c_colors.append(i_rgb)

                i_p_cross_p_1_0_o = usd_core.Gf.Vec3f(i_x-i_w/2, i_y, i_z+i_d/2)
                i_p_cross_p_1_1_o = usd_core.Gf.Vec3f(i_x+i_w/2, i_y, i_z-i_d/2)
                i_p_cross_p_1_0 = i_transformation_matrix.Transform(i_p_cross_p_1_0_o)
                i_p_cross_p_1_1 = i_transformation_matrix.Transform(i_p_cross_p_1_1_o)
                i_points_cross_1 = [i_p_cross_p_1_0, i_p_cross_p_1_0, i_p_cross_p_1_1, i_p_cross_p_1_1]
                c_points.extend(i_points_cross_1)
                c_counts.append(len(i_points_cross_1))
                c_widths.append(0.003)
                c_colors.append(i_rgb)
                # arrow line
                i_p_arrow_p_0_o = usd_core.Gf.Vec3f(i_x-i_w/2, i_y+i_h/2, i_z)
                i_p_arrow_p_0 = i_transformation_matrix.Transform(i_p_arrow_p_0_o)
                i_points_arrow_0 = [i_p_arrow_p_0, i_p_arrow_p_0, i_p_y, i_p_y]
                c_points.extend(i_points_arrow_0)
                c_counts.append(len(i_points_arrow_0))
                c_widths.append(0.003)
                c_colors.append(i_rgb)

                i_p_arrow_p_1_o = usd_core.Gf.Vec3f(i_x+i_w/2, i_y+i_h/2, i_z)
                i_p_arrow_p_1 = i_transformation_matrix.Transform(i_p_arrow_p_1_o)
                i_points_arrow_1 = [i_p_arrow_p_1, i_p_arrow_p_1, i_p_y, i_p_y]
                c_points.extend(i_points_arrow_1)
                c_counts.append(len(i_points_arrow_1))
                c_widths.append(0.003)
                c_colors.append(i_rgb)

            proxy_prim = opt.create_sibling('{}_proxy'.format(opt.get_name()), 'BasisCurves')
            proxy_opt = usd_core.UsdGeometryOpt(proxy_prim)
            proxy_opt.set_purpose_as_proxy()

            basis_curves_opt = usd_core.UsdBasisCurvesOpt(proxy_prim)
            basis_curves_opt.create(
                c_counts, c_points, c_widths
            )
            basis_curves_opt.set_display_colors_as_uniform(c_colors)

    def save_as_usd(self):
        self._stage_opt_new.usd_instance.GetRootLayer().Export(self._file_path_out_usd)

    def save_as_usda(self):
        self._stage_opt_new.usd_instance.GetRootLayer().Export(self._file_path_out_usda)


if __name__ == '__main__':
    cc = UsdScpForClarisseCleanup(
        '/l/prod/cgm/work/assets/env/env_waterfall/srf/surfacing/clarisse/plants_047_test.usd'
        # '/data/f/clarisse_usd_convert/plants.test.usda'
        # '/data/f/clarisse_usd_convert/plants_039.usd'
        # '/data/f/clarisse_usd_convert/plants.v001.test.usda'
    )
    cc.transfer()
    cc.save_as_usd()
