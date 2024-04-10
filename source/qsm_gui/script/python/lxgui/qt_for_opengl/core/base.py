# coding:utf-8
import sys

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# usd
import lxusd.core as usd_core
# qt
from .wrap import *


# noinspection PyUnusedLocal
class GuiGLUsdData(object):
    INDEX_P = '/geometries/{tag}/mesh_001_{index}/mesh_001_{index}Shape'
    TEXTURE_P = '/'

    def __init__(self, file_path, location, rgb=(1.0, 1.0, 1.0), texture_directory_path=None):
        self._translate_x, self._translate_y, self._translate_z = 0.0, 0.0, 0.0
        self._rotate_x, self._rotate_y, self._rotate_z = 90, 0.0, 0.0
        self._scale_factor = 1.0

        self._width, self._height = 512, 512

        self._cache_directory_path = '/data/e/workspace/lynxi-py3/test/opengl'

        self._file_path = file_path

        self._p_o = bsc_core.PtnParseOpt(self.INDEX_P)

        r, g, b = rgb

        self._texture_directory_path = texture_directory_path

        self._r_p, self._g_p, self._b_p = r/1.0, g/1.0, b/1.0

        self._location = location

        self._vertices = []
        self._vbos = []
        self._vbo_points = []
        self._vbo_indices = []

        self.__hash_key = None

        self.__load_stage(
            self._file_path
        )
        self._result = self.__build_stage()

    def __load_stage(self, file_path):
        self._stage_opt = usd_core.UsdStageOpt(file_path)

        (
            (self._x, self._y, self._z),
            (self._c_x, self._c_y, self._c_z),
            (self._w, self._h, self._d)
        ) = self._stage_opt.compute_geometry_args('/')

        s = max(self._w, self._h)

        self._scale_factor = 1.0/max(self._w, self._h)*2
        self._translate_x = -self._c_x*self._scale_factor
        self._translate_y = (-self._c_y-(s-self._h)/2)*self._scale_factor

    def __build_stage(self):
        self._vertices = []
        self._vbos = []
        self._vbo_indices = []
        #
        bsc_log.Log.test_start('build stage')
        prim = self._stage_opt.get_obj(self._location)
        if prim.GetTypeName() == 'Mesh':
            self.__build_mesh(prim)
        else:
            for i_prim in usd_core.UsdPrimOpt(
                self._stage_opt.get_obj(self._location)
            ).get_descendants(
                type_includes=['Mesh']
            ):
                self.__build_mesh(i_prim)
        bsc_log.Log.test_end('build stage')

        self._hash_key = bsc_core.HashMtd.get_hash_value(self._vertices, as_unique_id=True)
        self._image_file_path = '{}/{}.png'.format(self._cache_directory_path, self._hash_key)

        return bsc_storage.StgFileOpt(self._image_file_path).get_is_exists()

    def __build_mesh(self, prim):
        mesh_opt = usd_core.UsdMeshOpt(usd_core.UsdGeom.Mesh(prim))
        path = mesh_opt.get_path()
        r, g, b = bsc_core.PthNodeOpt(path).get_plant_rgb(maximum=1.0)
        r_p, g_p, b_p = r/1.0, g/1.0, b/1.0
        variants = self._p_o.get_variants(path)
        index = int(variants['index'])
        face_vertex_counts, face_vertex_indices = mesh_opt.get_face_vertices()
        vbo_indices = []
        index_cur = 0
        for i_count in face_vertex_counts:
            i_indices = face_vertex_indices[index_cur:index_cur+i_count]
            index_cur += i_count
            vbo_indices.append(map(int, i_indices))
        self._vbo_indices.append(vbo_indices)

        points = mesh_opt.get_points()
        vbo_points = []
        for i_point in points:
            j_x, j_y, j_z = i_point
            i_d = 1.0-abs((j_z-self._c_z)+self._d/2)/self._d
            vbo_points.extend((j_x, j_y, j_z))
            vbo_points.extend((i_d*r_p, i_d*g_p, i_d*b_p))
            #
            self._vertices.extend((j_x, j_y, j_z))
        self._vbo_points.append(vbo_points)

    def build_vbos(self):
        for i_points in self._vbo_points:
            i_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, i_vbo)
            GL.glBufferData(
                GL.GL_ARRAY_BUFFER, len(i_points)*4, (GL.GLfloat*len(i_points))(*i_points), GL.GL_STATIC_DRAW
            )
            self._vbos.append(i_vbo)

    def get_translate(self):
        return self._translate_x, self._translate_y, self._translate_z

    def get_rotate(self):
        return self._rotate_x, self._rotate_y, self._rotate_z

    def get_scale_factor(self):
        return self._scale_factor

    def get_vbos(self):
        return self._vbos

    def get_vbo_indices(self):
        return self._vbo_indices

    def get_image_path(self):
        return self._image_file_path

    def get_result(self):
        return self._result

    def paint_vbo(self):
        bsc_log.Log.test_start('paint')
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glLoadIdentity()
        GL.glTranslatef(*self.get_translate())
        GL.glRotatef(90, 0, 1, 0)
        GL.glScaled(*[self.get_scale_factor()]*3)

        GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
        GL.glEnableClientState(GL.GL_COLOR_ARRAY)

        for i_vbo, i_indices in zip(self.get_vbos(), self.get_vbo_indices()):
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, i_vbo)
            GL.glVertexPointer(3, GL.GL_FLOAT, 6*4, None)
            GL.glColorPointer(3, GL.GL_FLOAT, 6*4, GL.ctypes.c_void_p(3*4))
            for j_face_indices in i_indices:
                j_face_count = len(j_face_indices)
                GL.glDrawElements(
                    GL.GL_POLYGON,
                    j_face_count,
                    GL.GL_UNSIGNED_INT,
                    j_face_indices
                )

        GL.glDisableClientState(GL.GL_VERTEX_ARRAY)
        GL.glDisableClientState(GL.GL_COLOR_ARRAY)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        bsc_log.Log.test_end('paint')


class GuiGLUsdBatchRender(object):
    def __init__(self, data):
        self._data = data

        self._width, self._height = 512, 512

        self._index = 0
        self._index_max = len(data)-1

    def __do_export(self, file_path):
        from PIL import Image, ImageOps

        image_data = GL.glReadPixels(0, 0, self._width, self._height, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE)
        image = Image.frombytes('RGBA', (self._width, self._height), image_data)
        image.transpose(Image.FLIP_TOP_BOTTOM)
        image = ImageOps.flip(image)
        image.save(file_path, format='PNG')

    def __do_paint(self, data):
        data.build_vbos()
        bsc_log.Log.test_start('paint')
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)

        GL.glLoadIdentity()
        GL.glTranslatef(*data.get_translate())
        # GL.glRotatef(*data.get_rotate())
        GL.glScaled(*[data.get_scale_factor()]*3)

        GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
        GL.glEnableClientState(GL.GL_COLOR_ARRAY)

        for i_vbo, i_indices in zip(data.get_vbos(), data.get_vbo_indices()):
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, i_vbo)
            GL.glVertexPointer(3, GL.GL_FLOAT, 6*4, None)
            GL.glColorPointer(3, GL.GL_FLOAT, 6*4, GL.ctypes.c_void_p(3*4))
            for j_face_indices in i_indices:
                j_face_count = len(j_face_indices)
                GL.glDrawElements(
                    GL.GL_POLYGON,
                    j_face_count,
                    GL.GL_UNSIGNED_INT,
                    j_face_indices
                )

        GL.glDisableClientState(GL.GL_VERTEX_ARRAY)
        GL.glDisableClientState(GL.GL_COLOR_ARRAY)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        bsc_log.Log.test_end('paint')

        self.__do_export(data.get_image_path())

    def __do_render(self):
        if self._index >= self._index_max:
            GLUT.glutLeaveMainLoop()
            return
        else:
            file_path, location = self._data[self._index]
            d = GuiGLUsdData(file_path, location)
            # if d.get_result() is False:
            self.__do_paint(d)

        self._index += 1

    def start(self):
        GLUT.glutInit(sys.argv)
        GLUT.glutInitDisplayMode(GLUT.GLUT_RGBA|GLUT.GLUT_DOUBLE)

        GLUT.glutInitWindowPosition(0, 0)
        GLUT.glutInitWindowSize(self._width, self._height)
        GLUT.glutCreateWindow('render window')

        GL.glClearColor(0.0, 0.0, 0.0, 0.0)
        GL.glEnable(GL.GL_DEPTH_TEST)

        GLUT.glutDisplayFunc(self.__do_render)
        GLUT.glutIdleFunc(self.__do_render)

        GLUT.glutMainLoop()
