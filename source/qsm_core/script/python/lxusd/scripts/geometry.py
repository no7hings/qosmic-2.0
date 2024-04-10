# coding:utf-8
# usd
from .. import core as usd_core


class VertexColorBaker(object):
    def __init__(self):
        pass

    def load(self, file_path, image_mapper):
        self._stage_opt = usd_core.UsdStageOpt()
        self._stage_opt.append_sublayer(file_path)

        for i_prim in self._stage_opt.get_all_mesh_objs():
            i_key = i_prim.GetPath().pathString.split('/')[-1]
            i_image_file_path = image_mapper[i_key]
            i_mesh_opt = usd_core.UsdMeshOpt(i_prim)
            i_color_map = i_mesh_opt.compute_vertex_color_map_from_image(i_image_file_path, 'st')
            i_mesh_opt.set_display_colors_as_vertex(i_color_map)

    def save(self):
        self._stage_opt.export_to(
            '/data/e/workspace/lynxi/test/maya/vertex-color/test_2.color.usda'
        )


if __name__ == '__main__':
    b = VertexColorBaker()

    # b.load_texture(
    #     '/data/e/workspace/lynxi/test/maya/vertex-color/test_1.jpg'
    # )

    b.load(
        '/data/e/workspace/lynxi/test/maya/vertex-color/test_2.usda',
        {
            'pCubeShape1': '/data/e/workspace/lynxi/test/maya/vertex-color/test_1.jpg'
        }
    )

    b.save()

