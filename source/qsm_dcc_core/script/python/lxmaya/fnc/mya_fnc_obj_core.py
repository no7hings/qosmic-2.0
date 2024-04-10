# coding:utf-8
import lxbasic.core as bsc_core

import lxmaya.dcc.objects as mya_dcc_objects

import lxmaya.dcc.operators as mya_dcc_operators

import lxusd.dcc.operators as usd_dcc_operators


class FncNodeForUsdBase(object):
    OBJ_PATHSEP = '|'

    def __init__(self, usd_prim, location=None):
        self._usd_prim = usd_prim
        self._usd_stage = usd_prim.GetStage()
        #
        self._dcc_path = usd_prim.GetPath().pathString
        self._usd_path = self._dcc_path
        self._usd_path_dag_opt = bsc_core.PthNodeOpt(self._usd_path)
        self._mya_path_dag_opt = self._usd_path_dag_opt.translate_to(self.OBJ_PATHSEP)
        #
        if location is not None:
            location_path_dag_opt = bsc_core.PthNodeOpt(location)
            mya_root = location_path_dag_opt.translate_to(self.OBJ_PATHSEP)
            self._mya_path_dag_opt.parent_to_path(mya_root.path)

    def __str__(self):
        return '{}(path="{}")'.format(
            self.__class__.__name__,
            self._usd_path
        )

    def create_customize_ports(self, port_match_patterns):
        pass


class FncNodeForUsdTransform(FncNodeForUsdBase):
    def __init__(self, usd_prim, location=None):
        super(FncNodeForUsdTransform, self).__init__(usd_prim, location)

    def set_create(self):
        mya_transform = mya_dcc_objects.Transform(self._mya_path_dag_opt.get_value())
        if mya_transform.get_is_exists() is False:
            usd_transform_opt = usd_dcc_operators.TransformOpt(self._usd_prim)
            matrix = usd_transform_opt.get_matrix()
            #
            mya_transform_opt = mya_dcc_operators.TransformOpt(mya_transform)
            if mya_transform_opt.set_create() is True:
                mya_transform_opt.set_matrix(matrix)


class FncNodeForUsdMesh(FncNodeForUsdBase):
    def __init__(self, usd_prim, location=None):
        super(FncNodeForUsdMesh, self).__init__(usd_prim, location)
        #
        self._usd_transform_path_dag_opt = self._usd_path_dag_opt.get_parent()
        self._usd_group_path_dag_opt = self._usd_transform_path_dag_opt.get_parent()
        #
        self._mya_transform_path_dag_opt = self._mya_path_dag_opt.get_parent()
        self._mya_group_path_dag_opt = self._mya_transform_path_dag_opt.get_parent()

    def do_repath_to(self, path_tgt):
        self.do_create_group()
        #
        tgt_path_dag_opt = bsc_core.PthNodeOpt(path_tgt)
        tgt_mya_path_dag_opt = tgt_path_dag_opt.translate_to(self.OBJ_PATHSEP)
        tgt_mya_mesh = mya_dcc_objects.Mesh(tgt_mya_path_dag_opt.get_value())
        #
        if tgt_mya_mesh.get_is_exists() is True:
            tgt_mya_transform = tgt_mya_mesh.transform
            tgt_mya_transform.set_repath(self._mya_transform_path_dag_opt.get_value())

    def do_create_group(self):
        mya_group = mya_dcc_objects.Group(self._mya_group_path_dag_opt.get_value())
        if mya_group.get_is_exists() is False:
            usd_paths = self._usd_group_path_dag_opt.get_component_paths()
            if usd_paths:
                usd_paths.reverse()
                for i_usd_path in usd_paths:
                    if i_usd_path != '/':
                        FncNodeForUsdTransform(
                            self._usd_stage.GetPrimAtPath(i_usd_path)
                        ).set_create()

    def do_create_transform(self):
        mya_transform = mya_dcc_objects.Transform(self._mya_transform_path_dag_opt.get_value())
        if mya_transform.get_is_exists() is False:
            FncNodeForUsdTransform(
                self._usd_stage.GetPrimAtPath(self._usd_transform_path_dag_opt.get_value())
            ).set_create()

    def set_create(self, with_group=True, with_transform=True):
        if with_group is True:
            self.do_create_group()
        #
        if with_transform is True:
            self.do_create_transform()
        #
        mya_mesh = mya_dcc_objects.Mesh(self._mya_path_dag_opt.get_value())
        if mya_mesh.get_is_exists() is False:
            usd_mesh_opt = usd_dcc_operators.MeshOpt(self._usd_prim)
            face_vertices = usd_mesh_opt.get_face_vertices()
            points = usd_mesh_opt.get_points()
            #
            mya_mesh_opt = mya_dcc_operators.MeshOpt(mya_mesh)
            is_create = mya_mesh_opt.set_create(
                face_vertices=face_vertices, points=points
            )
            if is_create is True:
                uv_maps = usd_mesh_opt.get_uv_maps()
                mya_mesh_opt.assign_uv_maps(uv_maps)
                #
                mesh_opt_new = mya_dcc_operators.MeshLookOpt(mya_mesh)
                mesh_opt_new.set_default_material_assign()

    def do_replace(self):
        mesh_old = mya_dcc_objects.Mesh(self._mya_path_dag_opt.get_value())
        if mesh_old.get_is_exists() is True:
            mesh_opt_old = mya_dcc_operators.MeshOpt(mesh_old)
            face_vertices_uuid_old = mesh_opt_old.get_face_vertices_as_uuid()
            #
            geometry = FncDccMesh(self._dcc_path).get_geometry()
            look = FncDccMesh(self._dcc_path).get_look()
            #
            transform_old = mesh_old.transform
            transform_old.set_visible(False)
            transform_old.parent_to_path(self.OBJ_PATHSEP)
            # instance after
            mesh_new = mya_dcc_objects.Mesh(self._mya_path_dag_opt.get_value())
            if mesh_new.get_is_exists() is False:
                self.do_create_transform()

                usd_mesh_new_opt = usd_dcc_operators.MeshOpt(self._usd_prim)
                face_vertices_uuid_new = usd_mesh_new_opt.get_face_vertices_as_uuid()
                face_vertices = usd_mesh_new_opt.get_face_vertices()
                points = usd_mesh_new_opt.get_points()

                mya_mesh_opt = mya_dcc_operators.MeshOpt(mesh_new)
                is_create = mya_mesh_opt.set_create(
                    face_vertices=face_vertices, points=points
                )

                if is_create is True:
                    if face_vertices_uuid_new == face_vertices_uuid_old:
                        uv_maps = geometry['uv_maps']
                        mya_mesh_opt.assign_uv_maps(uv_maps)
                    else:
                        mesh_old._update_path_()
                        mesh_old.set_uv_maps_transfer_to(mesh_new.path, clear_history=True)

                    mesh_opt_new = mya_dcc_operators.MeshLookOpt(mesh_new)

                    material_assigns = look['material_assigns']
                    properties = look['properties']
                    visibilities = look['visibilities']

                    mesh_opt_new.assign_materials(material_assigns)
                    mesh_opt_new.assign_render_properties(properties)
                    mesh_opt_new.assign_render_visibilities(visibilities)
            #
            transform_old._update_path_()
            transform_old.do_delete()

    def set_exchange(self, geometry, look):
        mesh_old = mya_dcc_objects.Mesh(self._mya_path_dag_opt.get_value())
        if mesh_old.get_is_exists() is True:
            mesh_opt_old = mya_dcc_operators.MeshOpt(mesh_old)
            face_vertices_uuid_old = mesh_opt_old.get_face_vertices_as_uuid()

            transform_old = mesh_old.transform
            transform_old.set_visible(False)
            transform_old.parent_to_path(self.OBJ_PATHSEP)

            mesh_new = mya_dcc_objects.Mesh(self._mya_path_dag_opt.get_value())
            if mesh_new.get_is_exists() is False:
                self.do_create_transform()

                usd_mesh_new_opt = usd_dcc_operators.MeshOpt(self._usd_prim)
                face_vertices_uuid_new = usd_mesh_new_opt.get_face_vertices_as_uuid()

                face_vertices = usd_mesh_new_opt.get_face_vertices()
                points = usd_mesh_new_opt.get_points()

                mya_mesh_opt = mya_dcc_operators.MeshOpt(mesh_new)
                is_create = mya_mesh_opt.set_create(
                    face_vertices=face_vertices, points=points
                )
                if is_create is True:
                    face_vertices_uuid_old = geometry['face_vertices_uuid']
                    if face_vertices_uuid_new == face_vertices_uuid_old:
                        uv_maps = geometry['uv_maps']
                        mya_mesh_opt.assign_uv_maps(uv_maps)
                    else:
                        mesh_old._update_path_()
                        mesh_old.set_uv_maps_transfer_to(mesh_new.path, clear_history=True)

                    mesh_opt_new = mya_dcc_operators.MeshLookOpt(mesh_new)

                    material_assigns = look['material_assigns']
                    properties = look['properties']
                    visibilities = look['visibilities']

                    mesh_opt_new.assign_materials(material_assigns)
                    mesh_opt_new.assign_render_properties(properties)
                    mesh_opt_new.assign_render_visibilities(visibilities)

                transform_old._update_path_()
                transform_old.do_delete()

    def set_points(self):
        mya_mesh = mya_dcc_objects.Mesh(self._mya_path_dag_opt.get_value())
        if mya_mesh.get_is_exists() is True:
            usd_mesh_opt = usd_dcc_operators.MeshOpt(self._usd_prim)
            #
            mya_mesh_opt = mya_dcc_operators.MeshOpt(mya_mesh)
            points = usd_mesh_opt.get_points()
            mya_mesh_opt.set_points(points)

    def assign_uv_maps(self):
        mya_mesh = mya_dcc_objects.Mesh(self._mya_path_dag_opt.get_value())
        if mya_mesh.get_is_exists() is True:
            usd_mesh_opt = usd_dcc_operators.MeshOpt(self._usd_prim)
            #
            mya_mesh_opt = mya_dcc_operators.MeshOpt(mya_mesh)
            uv_maps = usd_mesh_opt.get_uv_maps()
            mya_mesh_opt.assign_uv_maps(uv_maps)

    @classmethod
    def delete_fnc(cls, path_tgt):
        mesh_dcc_path_dag_opt = bsc_core.PthNodeOpt(path_tgt)
        transform_dcc_path_dag_opt = mesh_dcc_path_dag_opt.get_parent()
        transform_mya_path_dag_opt = transform_dcc_path_dag_opt.translate_to(cls.OBJ_PATHSEP)
        mya_dcc_objects.Node(transform_mya_path_dag_opt.get_value()).do_delete()

    @classmethod
    def remove_fnc(cls, path_tgt):
        mesh_dcc_path_dag_opt = bsc_core.PthNodeOpt(path_tgt)
        transform_dcc_path_dag_opt = mesh_dcc_path_dag_opt.get_parent()
        transform_mya_path_dag_opt = transform_dcc_path_dag_opt.translate_to(cls.OBJ_PATHSEP)
        mya_dcc_objects.Node(transform_mya_path_dag_opt.get_value()).set_to_world()


class FncDccMesh(object):
    OBJ_PATHSEP = '|'

    def __init__(self, dcc_path):
        self._dcc_path_dag_opt = bsc_core.PthNodeOpt(dcc_path)
        self._mya_path_dag_opt = self._dcc_path_dag_opt.translate_to(self.OBJ_PATHSEP)
        self._maya_mesh = mya_dcc_objects.Mesh(self._mya_path_dag_opt.get_value())
        #
        self._mya_mesh_opt = mya_dcc_operators.MeshOpt(self._maya_mesh)
        self._mya_mesh_look_opt = mya_dcc_operators.MeshLookOpt(self._maya_mesh)

    def get_geometry(self):
        if self._maya_mesh.get_is_exists() is True:
            return dict(
                face_vertices=self._mya_mesh_opt.get_face_vertices(),
                face_vertices_uuid=self._mya_mesh_opt.get_face_vertices_as_uuid(),
                points=self._mya_mesh_opt.get_points(),
                uv_maps=self._mya_mesh_opt.get_uv_maps()

            )
        return {}

    def get_look(self):
        if self._maya_mesh.get_is_exists() is True:
            return dict(
                material_assigns=self._mya_mesh_look_opt.get_material_assigns(),
                properties=self._mya_mesh_look_opt.get_render_properties(),
                visibilities=self._mya_mesh_look_opt.get_render_visibilities()
            )
        return {}
