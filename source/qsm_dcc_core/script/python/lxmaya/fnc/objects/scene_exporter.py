# coding:utf-8
import collections

import lxcontent.core as ctt_core

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.dcc.objects as bsc_dcc_objects

import lxbasic.fnc.abstracts as bsc_fnc_abstracts

import lxbasic.fnc.objects as bsc_fnc_objects
# maya
from ...core.wrap import *

from ... import core as mya_core
# maya dcc
from ...dcc import objects as mya_dcc_objects


class FncExporterForScene(
    bsc_fnc_abstracts.AbsFncOptionBase
):
    WITH_XGEN = 'with_xgen_collection'
    OPTION = dict(
        file='',
        location='',
        with_xgen_collection=False,
        with_set=False,
        ext_extras=[]
    )

    def __init__(self, option=None):
        super(FncExporterForScene, self).__init__(option)

    def execute(self):
        file_path = self.get('file')
        location = self.get('location')
        with_xgen_collection = self.get('with_xgen_collection')
        with_set = self.get('with_set')
        #
        ext_extras = self.get('ext_extras')
        #
        os_file = bsc_dcc_objects.StgFile(file_path)
        os_file.create_directory()
        #
        option = dict(
            type=mya_dcc_objects.Scene._get_file_type_name_(file_path),
            options='v=0;',
            force=True,
            defaultExtensions=True,
            preserveReferences=False,
        )
        _selected_paths = []
        if location:
            root_dag_opt = bsc_core.PthNodeOpt(location)
            root_mya_dag_opt = root_dag_opt.translate_to(
                mya_core.MyaUtil.OBJ_PATHSEP
            )
            _selected_paths = cmds.ls(selection=1, long=1) or []
            if with_set is True:
                ss = mya_dcc_objects.Sets()
                for i in ss.get_paths():
                    i_set = mya_dcc_objects.Set(i)
                    if i_set.get_elements_match('|master|*'):
                        bsc_log.Log.trace_method_result(
                            'maya scene export',
                            u'set="{}" is add to export'.format(i_set.path)
                        )
                        cmds.select(i_set.path, noExpand=True, add=True)
            #
            cmds.select(root_mya_dag_opt.path)
            option['exportSelected'] = True
        else:
            option['exportAll'] = True
        #
        _ = cmds.file(file_path, **option)
        if _:
            self._results = [file_path]
        #
        if with_xgen_collection is True:
            bsc_fnc_objects.FncExporterForDotMa._copy_scene_xgen_collection_files_to(
                mya_dcc_objects.Scene.get_current_file_path(),
                file_path
            )
        #
        if ext_extras:
            file_src = bsc_dcc_objects.StgFile(mya_dcc_objects.Scene.get_current_file_path())
            file_tgt = bsc_dcc_objects.StgFile(file_path)
            for i_ext in ext_extras:
                i_src = '{}.{}'.format(file_src.path_base, i_ext)
                i_tgt = '{}.{}'.format(file_tgt.path_base, i_ext)
                bsc_dcc_objects.StgFile(i_src).copy_to_file(i_tgt)
        #
        if self._results:
            for i in self._results:
                bsc_log.Log.trace_method_result(
                    'maya scene export',
                    u'file="{}"'.format(i)
                )

        if 'exportSelected' in option:
            if _selected_paths:
                cmds.select(_selected_paths)
            else:
                cmds.select(clear=1)

        return self._results

    def get_outputs(self):
        return self._results


# noinspection PyUnusedLocal
class FncExporterForPreview(
    bsc_fnc_abstracts.AbsFncOptionBase
):
    OPTION = dict(
        file='',
        root='',

        convert_to_dot_mov=True,
        use_render=False,
        frame=(0, 0),
        color_space='Linear'
    )

    def __init__(self, file_path, root=None, option=None):
        super(FncExporterForPreview, self).__init__(option)

        self._file_path = self.get('file')
        #
        self._root = self.get('root')
        if root is not None:
            self._root_dat_opt = bsc_core.PthNodeOpt(root)
        else:
            self._root_dat_opt = None

    @classmethod
    def _set_playblast_(
        cls, file_path, root, use_default_material=False, frame=(0, 0), size=(1024, 1024), persp_view=True,
        default_material_color=None
    ):
        output_file = bsc_dcc_objects.StgFile(file_path)
        output_file_path_base = output_file.path_base
        ext = output_file.ext
        compression = ext[1:]
        #
        preview_window = 'preview_export'
        mya_dcc_objects.Scene.set_window_delete(preview_window)
        cmds.window(preview_window, title='preview_export')
        image_width, image_height = size
        layout = cmds.paneLayout(width=image_width, height=image_height)
        camera, camera_shape = FncExporterForCameraYml._set_camera_create_(root, persp_view)
        preview_export_viewport = cmds.modelPanel(
            label='snapShotPanel',
            parent=layout,
            menuBarVisible=1,
            modelEditor=1,
            camera=camera
        )
        #
        if not use_default_material:
            mya_dcc_objects.Scene.set_display_mode(6)
        else:
            mya_dcc_objects.Scene.set_display_mode(5)
        #
        cmds.displayRGBColor('background', .25, .25, .25)
        cmds.displayRGBColor('backgroundTop', .25, .25, .25)
        cmds.displayRGBColor('backgroundBottom', .25, .25, .25)
        cmds.showWindow(preview_window)
        # Set ModelPanel ( Viewport 2.0 )
        mya_dcc_objects.Scene._set_preview_viewport_setup_(preview_export_viewport, mode=1)
        #
        cmds.modelEditor(
            preview_export_viewport,
            edit=1,
            activeView=1,
            useDefaultMaterial=use_default_material,
            wireframeOnShaded=0,
            fogging=0,
            dl='default',
            twoSidedLighting=1,
            allObjects=0,
            manipulators=0,
            grid=0,
            hud=1,
            sel=0
        )
        #
        cmds.modelEditor(
            preview_export_viewport,
            edit=1,
            activeView=1,
            polymeshes=1,
            subdivSurfaces=1,
            fluids=1,
            strokes=1,
            nCloths=1,
            nParticles=1,
            pluginShapes=1,
            pluginObjects=['gpuCacheDisplayFilter', 1],
            displayAppearance='smoothShaded'
        )
        #
        if default_material_color is not None:
            r, g, b = default_material_color
            cmds.setAttr('lambert1.color', r, g, b)
        else:
            cmds.setAttr('lambert1.color', 0, .75, .75)
        #
        start_frame, end_frame = frame
        cmds.playblast(
            startTime=start_frame,
            endTime=end_frame,
            format='iff',
            filename=output_file_path_base,
            sequenceTime=0,
            clearCache=1,
            viewer=0,
            showOrnaments=0,
            offScreen=0,
            framePadding=4,
            percent=100,
            compression=compression,
            quality=100,
            widthHeight=size
        )
        #
        cmds.isolateSelect(preview_export_viewport, state=0)
        mya_dcc_objects.Scene.set_window_delete(preview_window)
        mya_dcc_objects.Scene.set_display_mode(5)
        #
        cmds.setAttr('lambert1.color', .5, .5, .5)
        cmds.delete(camera)

    @classmethod
    def _set_render_(cls, file_path, root, persp_view=True, size=(1024, 1024), frame=(0, 0)):
        output_file = bsc_dcc_objects.StgFile(file_path)
        output_file_path_base = output_file.path_base
        ext = output_file.ext
        compression = ext[1:]
        image_width, image_height = size
        camera, camera_shape = FncExporterForCameraYml._set_camera_create_(root, persp_view)
        #
        render_option = mya_dcc_objects.RenderOption()
        start_frame, end_frame = frame
        render_option.set_animation_enable(True)
        render_option.set_frame_range(start_frame, end_frame)
        render_option.set_image_size(image_width, image_height)
        render_option.set_output_file_path(output_file_path_base)
        #
        light = cls.create_arnold_lights_fnc()
        cls.create_arnold_options_fnc()
        cls._set_arnold_options_update_()
        cls._set_arnold_render_run_(camera, image_width, image_height)
        cmds.delete(light)
        cmds.delete(camera)

    @classmethod
    def create_arnold_lights_fnc(cls):
        light = mya_dcc_objects.Shape('light')
        if light.get_is_exists() is False:
            light = light.set_create('aiStandIn')
        #
        atr_raw = dict(
            dso=bsc_storage.StgPathMapper.map_to_current(
                '/l/resource/td/asset/ass/default-light.ass'
            )
        )
        [light.get_port(k).set(v) for k, v in atr_raw.items()]
        return light.transform.path

    @classmethod
    def create_arnold_options_fnc(cls):
        # noinspection PyBroadException
        try:
            cmds.loadPlugin('mtoa', quiet=1)
            # noinspection PyUnresolvedReferences
            import mtoa.core as core

            core.createOptions()
        except Exception:
            pass

    @classmethod
    def _set_arnold_options_update_(cls):
        arnold_render_option = mya_dcc_objects.AndRenderOption()
        arnold_render_option.set_image_format('exr')
        arnold_render_option.set_aa_sample(6)

    @classmethod
    def _set_arnold_render_run_(cls, camera, image_width, image_height, frame=None):
        cls.create_arnold_options_fnc()
        #
        cmds.arnoldRender(
            seq='', cam=camera, w=image_width, h=image_height, srv=False
        )
        return True

    def execute(self):
        use_render = self._option.get('use_render')
        self._mya_root_dag_path = self._root_dat_opt.translate_to(
            mya_core.MyaUtil.OBJ_PATHSEP
        )
        root_mya_obj = mya_dcc_objects.Group(self._mya_root_dag_path.path)
        mya_dcc_objects.Scene.set_render_resolution(1024, 1024)
        if root_mya_obj.get_is_exists() is True:
            if use_render is True:
                self._set_render_run_()
                bsc_log.Log.trace_method_result(
                    'maya-render-preview-export',
                    u'file="{}"'.format(self._file_path)
                )
            else:
                self._set_snapshot_run_()
                bsc_log.Log.trace_method_result(
                    'maya-snapshot-preview-export',
                    u'file="{}"'.format(self._file_path)
                )
        else:
            bsc_log.Log.trace_method_warning(
                'maya-preview-export',
                u'obj="{}" is non-exists'.format(self._root)
            )

    def _set_snapshot_run_(self):
        self._file_obj = bsc_dcc_objects.StgFile(self._file_path)
        file_path_base = self._file_obj.path_base
        #
        jpg_file_path = '{}.snapshot/image{}'.format(file_path_base, '.jpg')
        jpg_seq_file_path = '{}.snapshot/image.%04d{}'.format(file_path_base, '.jpg')
        mov_file_path = '{}{}'.format(file_path_base, '.mov')
        frame = self._option.get('frame')
        self._set_playblast_(
            jpg_file_path,
            self._root,
            frame=frame
        )
        jpg_seq_file = bsc_dcc_objects.StgFile(jpg_seq_file_path)
        if self._option.get('convert_to_dot_mov') is True:
            if jpg_seq_file.get_exists_units():
                bsc_storage.VdoFileOpt(
                    mov_file_path
                ).set_create_from(
                    jpg_seq_file_path
                )
        else:
            jpg_seq_file = bsc_dcc_objects.StgFile(jpg_seq_file_path)
            exist_files = jpg_seq_file.get_exists_units()
            if exist_files:
                jpg_seq_file.get_exists_units()[0].copy_to_file(
                    self._file_path
                )
        #
        self._results = [mov_file_path]

    def _set_render_run_(self):
        self._file_obj = bsc_dcc_objects.StgFile(self._file_path)
        file_path_base = self._file_obj.path_base
        #
        jpg_file_path = '{}.render/image{}'.format(file_path_base, '.exr')
        jpg_seq_file_path = '{}.render/image.%04d{}'.format(file_path_base, '.exr')
        mov_file_path = '{}{}'.format(file_path_base, '.mov')

        self._set_render_(
            jpg_file_path,
            self._mya_root_dag_path.path
        )
        jpg_seq_file = bsc_dcc_objects.StgFile(jpg_seq_file_path)
        if self._option.get('convert_to_dot_mov') is True:
            if jpg_seq_file.get_exists_units():
                bsc_storage.VdoFileOpt(
                    mov_file_path
                ).set_create_from(
                    jpg_seq_file_path
                )

        self._results = [mov_file_path]
