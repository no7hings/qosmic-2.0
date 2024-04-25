# coding:utf-8


class AbsNodeOpt(object):
    def __init__(self, *args, **kwargs):
        """
        :param args:
            1.str(path)
        """
        self._obj = args[0]

    def get_obj(self):
        return self._obj

    obj = property(get_obj)

    def get_node(self):
        return self._obj

    node = property(get_node)

    def get_path(self):
        return self._obj.path

    path = property(get_path)

    def get_is_exists(self):
        return self._obj.get_is_exists()

    def __str__(self):
        return '{}(path="{}")'.format(
            self.__class__.__name__,
            self._obj.path
        )


class AbsMeshOptDef(object):
    def _init_mesh_opt_def_(self):
        pass

    def set_create(self, face_vertices, points, uv_maps=None, normal_maps=None, color_maps=None):
        raise NotImplementedError()

    def get_face_vertex_counts(self, *args, **kwargs):
        raise NotImplementedError()

    def get_face_vertex_indices(self, *args, **kwargs):
        raise NotImplementedError()

    def get_face_vertices(self, *args, **kwargs):
        raise NotImplementedError()

    def get_points(self, *args, **kwargs):
        raise NotImplementedError()

    def get_uv_map_coords(self, *args, **kwargs):
        raise NotImplementedError()

    def get_uv_map(self, *args, **kwargs):
        raise NotImplementedError()

    def get_uv_map_names(self, *args, **kwargs):
        raise NotImplementedError()

    def get_uv_maps(self, *args, **kwargs):
        raise NotImplementedError()


class AbsCurveOptDef(object):
    def _init_curve_opt_def_(self):
        pass

    def set_create(self, *args, **kwargs):
        pass


class AbsSceneOpt(object):
    @classmethod
    def _build_mesh_comparer_data(cls, content_0, dcc_obj_path, dcc_obj_name, face_vertices_uuid, points_uuid):
        # name
        content_0.append_element('property.name.{}'.format(dcc_obj_name), dcc_obj_path)
        # path
        content_0.set('property.path.{}'.format(dcc_obj_path), dcc_obj_name)
        # face-vertices
        content_0.append_element('face-vertices.uuid.{}'.format(face_vertices_uuid), dcc_obj_path)
        content_0.set('face-vertices.path.{}'.format(dcc_obj_path), face_vertices_uuid)
        # points
        content_0.append_element('points.uuid.{}'.format(points_uuid), dcc_obj_path)
        content_0.set('points.path.{}'.format(dcc_obj_path), points_uuid)
