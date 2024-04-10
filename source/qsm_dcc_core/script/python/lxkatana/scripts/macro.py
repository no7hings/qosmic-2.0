# coding:utf-8
import collections

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# katana
from ..core.wrap import *


class _MacroMtd(object):
    @classmethod
    def set_warning_show(cls, label, contents):
        import lxgui.core as gui_core

        import lxkatana.core as ktn_core

        if contents:
            if ktn_core.KtnUtil.get_is_ui_mode():
                gui_core.GuiDialog.create(
                    label,
                    content=u'\n'.join(contents),
                    status=gui_core.GuiDialog.ValidationStatus.Warning,
                    #
                    yes_label='Close',
                    #
                    no_visible=False, cancel_visible=False
                )
            else:
                for i in contents:
                    bsc_log.Log.trace_method_warning(
                        label, i
                    )


class LxCameraAlembic(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def set_reset(self):
        import lxkatana.core as ktn_core

        #
        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)

        obj_opt.set_port_raw(
            'alembic.file', ''
        )
        obj_opt.set_port_raw(
            'alembic.location', ''
        )
        #
        obj_opt.set_port_raw(
            'option.resolution_enable', False
        )
        obj_opt.set_port_raw(
            'option.resolution', '512x512'
        )

    def set_file_load(self):
        # adjustScreenWindow=Adjust width to match resolution
        import lxresolver.core as rsv_core
        #
        import lxkatana.core as ktn_core
        #
        import lxkatana.dcc.objects as ktn_dcc_objects

        #
        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        #
        f = ktn_dcc_objects.Scene.get_current_file_path()
        if f:
            resolver = rsv_core.RsvBase.generate_root()
            rsv_task = resolver.get_rsv_task_by_any_file_path(f)
            if rsv_task:
                rsv_entity = rsv_task.get_rsv_resource()
                rsv_camera_task = rsv_entity.get_rsv_task(
                    step='cam',
                    task='camera'
                )
                if rsv_camera_task is not None:
                    rsv_unit = rsv_camera_task.get_rsv_unit(
                        keyword='asset-camera-main-abc-file'
                    )
                    file_path = rsv_unit.get_result(version='latest')
                    if file_path:
                        obj_opt.set_port_raw(
                            'alembic.file',
                            file_path
                        )
                        obj_opt.set_port_raw(
                            'alembic.location',
                            '/root/world/cam/cameras'
                        )


class LxRenderSettings(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def set_reset(self):
        pass

    def set_stats_file(self):
        pass

    def set_profile_file(self):
        pass

    def set_render_output(self):
        import lxresolver.core as rsv_core
        #
        import lxkatana.core as ktn_core
        #
        import lxkatana.dcc.objects as ktn_dcc_objects

        #
        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        #
        f = ktn_dcc_objects.Scene.get_current_file_path()
        if f:
            resolver = rsv_core.RsvBase.generate_root()
            rsv_task = resolver.get_rsv_task_by_any_file_path(
                f
            )
            if rsv_task:
                # todo: use user render output instance
                rsv_unit = rsv_task.get_rsv_unit(keyword='asset-temporary-katana-render-output-dir')
                result = rsv_unit.get_result(
                    version='new'
                )
                v = '{}/main/<camera>.<layer>.<light-pass>.<look-pass>.<quality>/<render-pass>.####.exr'.format(
                    result
                )
                #
                obj_opt.set_port_raw(
                    'lynxi_settings.render_output', v
                )


# noinspection PyUnusedLocal
class LxAsset(object):
    VARIANTS = {
        #
        'modeling': 'usd.variants.asset_version.model',
        'groom': 'usd.variants.asset_version.groom',
        'rigging': 'usd.variants.asset_version.rig',
        'effects': 'usd.variants.asset_version.effect',
        'surfacing': 'usd.variants.asset_version.surface',
        #
        'model_override': 'usd.variants.asset_version_override.model',
        'groom_override': 'usd.variants.asset_version_override.groom',
        'rig_override': 'usd.variants.asset_version_override.rig',
        'effect_override': 'usd.variants.asset_version_override.effect',
        'surface_override': 'usd.variants.asset_version_override.surface',
        #
        'animation': 'usd.variants.shot_version.animation',
        #
        'animation_override': 'usd.variants.shot_version_override.animation',
    }
    ASSET_OVERRIDE_VARIANTS = {
        ('model', 'mod', 'modeling'),
        ('groom', 'grm', 'groom'),
        ('rig', 'rig', 'rigging'),
        ('surface', 'srf', 'surfacing'),
    }

    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def set_reset(self):
        import lxkatana.core as ktn_core

        #
        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)

        obj_opt.set(
            'options.asset', ''
        )
        obj_opt.set_as_enumerate(
            'options.shot', ['None']
        )

        obj_opt.set_port_raw(
            'usd.asset.enable', 0
        )
        obj_opt.set_port_raw(
            'usd.asset.file', ''
        )

    def set_guess(self):
        import lxgui.core as gui_core

        import lxresolver.core as rsv_core

        import lxkatana.core as ktn_core

        import lxkatana.dcc.objects as ktn_dcc_objects

        content = None
        #
        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        #
        scheme = obj_opt.get('options.scheme')
        #
        rsv_asset = None
        resolver = rsv_core.RsvBase.generate_root()
        #
        rsv_asset_path = obj_opt.get_port_raw('options.asset')
        if rsv_asset_path:
            rsv_asset = self._get_rsv_asset_(rsv_asset_path)
            if rsv_asset is None:
                content = 'asset="{}" is not available'.format(rsv_asset_path)
        else:
            file_path = ktn_dcc_objects.Scene.get_current_file_path()
            rsv_task = resolver.get_rsv_task_by_any_file_path(file_path)
            if rsv_task:
                rsv_asset = rsv_task.get_rsv_resource()
            else:
                content = 'file="{}" is not available'.format(file_path)

        if rsv_asset is not None:
            self.__set_rsv_asset_(rsv_asset)
            if scheme in ['shot_asset']:
                self.__set_rsv_asset_shots_(rsv_asset)

        if content is not None:
            if ktn_core.KtnUtil.get_is_ui_mode():
                gui_core.GuiDialog.create(
                    'Shot Asset Loader',
                    content=content,
                    status=gui_core.GuiDialog.ValidationStatus.Warning,
                    #
                    yes_label='Close',
                    #
                    no_visible=False, cancel_visible=False
                )

    @classmethod
    def _get_rsv_asset_(cls, rsv_asset_path):
        import lxresolver.core as rsv_core

        #
        _ = rsv_asset_path.split('/')
        project, role, asset = _[1:]
        resolver = rsv_core.RsvBase.generate_root()
        return resolver.get_rsv_resource(
            project=project,
            asset=asset
        )

    @classmethod
    def _get_rsv_shot_(cls, rsv_shot_path):
        import lxresolver.core as rsv_core

        #
        _ = rsv_shot_path.split('/')
        project, sequence, shot = _[1:]
        resolver = rsv_core.RsvBase.generate_root()
        return resolver.get_rsv_resource(project=project, shot=shot)

    @classmethod
    def _get_rsv_asset_auto_(cls):
        import lxresolver.core as rsv_core
        #
        import lxkatana.dcc.objects as ktn_dcc_objects

        #
        any_scene_file_path = ktn_dcc_objects.Scene.get_current_file_path()
        #
        if any_scene_file_path:
            resolver = rsv_core.RsvBase.generate_root()
            rsv_task = resolver.get_rsv_task_by_any_file_path(any_scene_file_path)
            if rsv_task:
                rsv_asset = rsv_task.get_rsv_resource()
                return rsv_asset

    def _get_rsv_shot_auto_(self, rsv_asset):
        import lxkatana.core as ktn_core

        import lxusd.rsv.objects as usd_rsv_objects

        #
        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        #
        rsv_shots = usd_rsv_objects.RsvUsdAssetSetCreator._get_rsv_asset_shots(rsv_asset)
        if rsv_shots:
            obj_opt.set_as_enumerate(
                'options.shot', [i.path for i in rsv_shots]
            )
            return rsv_shots[0]

    def __set_rsv_asset_(self, rsv_asset):
        import lxkatana.core as ktn_core

        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)

        obj_opt.set(
            'options.asset', rsv_asset.path
        )

    def __set_rsv_asset_shots_(self, rsv_asset):
        import lxkatana.core as ktn_core

        import lxusd.rsv.objects as usd_rsv_objects

        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)

        rsv_shots = usd_rsv_objects.RsvUsdAssetSetCreator._get_rsv_asset_shots(rsv_asset)
        if rsv_shots:
            obj_opt.set_as_enumerate(
                'options.shot', [i.path for i in rsv_shots]
            )

    def __set_asset_usd_create_(self, rsv_asset):
        import lxkatana.core as ktn_core

        import lxkatana.dcc.objects as ktn_dcc_objects

        import lxusd.rsv.objects as usd_rsv_objects

        import lxresolver.core as rsv_core

        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)

        any_scene_file_path = ktn_dcc_objects.Scene.get_current_file_path()

        resolver = rsv_core.RsvBase.generate_root()
        rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
        if rsv_scene_properties:
            asset_set_usd_file_path = usd_rsv_objects.RsvUsdAssetSetCreator._create_asset_usd_file(
                rsv_asset,
                rsv_scene_properties
            )
            if asset_set_usd_file_path:
                obj_opt.set_port_raw(
                    'usd.asset.enable', 1
                )
                obj_opt.set(
                    'usd.asset.file', asset_set_usd_file_path
                )
                obj_opt.set('lynxi_settings.render_start_frame', 1001.0)
                obj_opt.set('lynxi_settings.render_end_frame', 1240.0)
                obj_opt.set('lynxi_settings.render_resolution', '2048x2048')
                usd_variant_dict = usd_rsv_objects.RsvUsdAssetSetCreator._get_usd_variant_dict(
                    rsv_asset,
                    rsv_scene_properties,
                    asset_set_usd_file_path
                )
                self.__set_usd_variant_by_dict_(usd_variant_dict)
                #
                bsc_log.Log.trace_method_result(
                    'set usd create for asset',
                    'file="{}"'.format(asset_set_usd_file_path)
                )
        #
        CacheManager.flush()

    def __set_asset_shot_usd_create_(self, rsv_asset, rsv_shot):
        import lxkatana.core as ktn_core

        import lxkatana.dcc.objects as ktn_dcc_objects

        import lxusd.rsv.objects as usd_rsv_objects

        import lxresolver.core as rsv_core

        #
        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)

        any_scene_file_path = ktn_dcc_objects.Scene.get_current_file_path()

        resolver = rsv_core.RsvBase.generate_root()
        rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
        if rsv_scene_properties:
            asset_shot_set_usd_file_path = usd_rsv_objects.RsvUsdAssetSetCreator._create_asset_shot_usd_file(
                rsv_asset, rsv_shot,
                rsv_scene_properties
            )
            if asset_shot_set_usd_file_path:
                obj_opt.set_port_raw(
                    'usd.asset.enable', 1
                )
                obj_opt.set(
                    'usd.asset.file', asset_shot_set_usd_file_path
                )
                start_frame, end_frame = usd_rsv_objects.RsvUsdAssetSetCreator._get_shot_frame_range(rsv_shot)
                obj_opt.set('lynxi_settings.render_start_frame', start_frame)
                obj_opt.set('lynxi_settings.render_end_frame', end_frame)
                #
                obj_opt.set('lynxi_settings.render_resolution', '2048x858')
                #
                shot_asset_main_dict = usd_rsv_objects.RsvUsdAssetSetCreator._get_shot_asset_dict(
                    rsv_asset, rsv_shot
                )
                shot_assets = [i for i in shot_asset_main_dict.keys()]
                shot_assets.append('None')
                obj_opt.set_enumerate_strings(
                    'usd.variants.shot_asset', shot_assets
                )
                #
                shot_asset_override_dict = usd_rsv_objects.RsvUsdAssetSetCreator._get_shot_asset_override_dict(
                    rsv_asset, rsv_shot, rsv_scene_properties
                )
                shot_assets_override = [i for i in shot_asset_override_dict.keys()]
                shot_assets_override.append('None')
                obj_opt.set_enumerate_strings(
                    'usd.variants.shot_asset_override', shot_assets_override
                )
                #
                ktn_dcc_objects.Scene.set_frame_range(start_frame, end_frame)
                #
                usd_variant_dict = usd_rsv_objects.RsvUsdAssetSetCreator._get_usd_variant_dict(
                    rsv_asset,
                    rsv_scene_properties,
                    asset_shot_set_usd_file_path
                )
                #
                self.__set_usd_variant_by_dict_(
                    usd_variant_dict
                )
                #
                bsc_log.Log.trace_method_result(
                    'set usd create for shot-asset',
                    'file="{}"'.format(asset_shot_set_usd_file_path)
                )
        #
        CacheManager.flush()

    def __set_asset_info_update_(self, rsv_task):
        import lxkatana.core as ktn_core

        #
        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        #
        for k, v in rsv_task.properties.value.items():
            obj_opt.set('lynxi_properties.{}'.format(k), v)

    def __set_usd_variant_by_dict_(self, dict_):
        import lxkatana.core as ktn_core

        #
        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        for k, v in dict_.items():
            i_port_path = 'usd.{}'.format(v['port_path'])
            i_variant_names = v['variant_names']
            i_current_variant_name = v['variant_name']
            obj_opt.set_as_enumerate(
                i_port_path, i_variant_names
            )
            obj_opt.set(
                i_port_path,
                i_current_variant_name
            )

    def set_create(self):
        import lxkatana.core as ktn_core

        #
        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        #
        obj_opt.set_port_raw(
            'usd.asset.enable', 0
        )
        #
        scheme = obj_opt.get('options.scheme')
        #
        if scheme in ['asset']:
            self.__set_asset_create_()
        elif scheme in ['shot_asset']:
            self.__set_asset_shot_create_()

    def __set_asset_create_(self):
        import lxgui.core as gui_core

        import lxkatana.core as ktn_core

        content = None
        #
        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        #
        rsv_asset_path = obj_opt.get_port_raw('options.asset')
        if rsv_asset_path:
            rsv_asset = self._get_rsv_asset_(rsv_asset_path)
            if rsv_asset is None:
                content = 'asset="{}" is not available'.format(rsv_asset_path)
        else:
            rsv_asset = self._get_rsv_asset_auto_()
        #
        if rsv_asset is not None:
            self.__set_rsv_asset_(rsv_asset)
            self.__set_asset_usd_create_(rsv_asset)
        #
        if content is not None:
            if ktn_core.KtnUtil.get_is_ui_mode():
                gui_core.GuiDialog.create(
                    'Shot Asset Loader',
                    content=content,
                    status=gui_core.GuiDialog.ValidationStatus.Warning,
                    #
                    yes_label='Close',
                    #
                    no_visible=False, cancel_visible=False
                )

    def __set_asset_shot_create_(self):
        import lxgui.core as gui_core

        import lxkatana.core as ktn_core

        import lxusd.rsv.objects as usd_rsv_objects

        content = None
        #
        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        #
        rsv_asset_path = obj_opt.get_port_raw('options.asset')
        if rsv_asset_path:
            rsv_asset = self._get_rsv_asset_(rsv_asset_path)
            if rsv_asset is None:
                content = 'asset="{}" is not available'.format(rsv_asset_path)
        else:
            rsv_asset = self._get_rsv_asset_auto_()

        if rsv_asset:
            self.__set_rsv_asset_(rsv_asset)
            #
            rsv_shot_path = obj_opt.get_port_raw('options.shot')
            if rsv_shot_path != 'None':
                rsv_shot = self._get_rsv_shot_(rsv_shot_path)
            else:
                rsv_shot = self._get_rsv_shot_auto_(rsv_asset)

            if rsv_asset and rsv_shot:
                shot_set_dress_usd_file_path = usd_rsv_objects.RsvUsdAssetSetCreator._generate_shot_set_dress_usd_file_path_as_latest(
                    rsv_shot
                )
                if shot_set_dress_usd_file_path:
                    self.__set_asset_shot_usd_create_(
                        rsv_asset,
                        rsv_shot
                    )
                else:
                    content = u'shot="{}" set-dress file is non-exists'.format(rsv_shot_path)
            else:
                content = u'asset="{}" shot(s) is non-exists'.format(rsv_asset.path)
        #
        if content is not None:
            if ktn_core.KtnUtil.get_is_ui_mode():
                gui_core.GuiDialog.create(
                    'Shot Asset Loader',
                    content=content,
                    status=gui_core.GuiDialog.ValidationStatus.Warning,
                    #
                    yes_label='Close',
                    #
                    no_visible=False, cancel_visible=False
                )

    def set_translate_to_center(self):
        import lxusd.core as usd_core

        import lxkatana.core as ktn_core

        #
        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        #
        file_path = obj_opt.get('usd.asset.file')
        if file_path:
            root = '/master'
            sub_locations = [
                '/master/hi',
                '/master/shape',
            ]
            s_opt = usd_core.UsdStageOpt(
                file_path
            )
            [s_opt.set_active_at(i, True) for i in sub_locations]
            g = s_opt.compute_geometry_args(root)
            (x, y, z), (c_x, c_y, c_z), (w, h, d) = g
            if obj_opt.get('extra.transformation.translate_above_axis_y'):
                obj_opt.set(
                    'extra.transformation.translate_offset', [-c_x, -y, -c_z]
                )
            else:
                obj_opt.set(
                    'extra.transformation.translate_offset', [-c_x, -c_y, -c_z]
                )


class LxAssetAss(object):
    RENDER_MODE = 'previewRender'

    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    @classmethod
    def _get_input_dynamic_usd_file_(cls, rsv_asset):
        rsv_task = rsv_asset.get_rsv_task(
            step='mod', task='mod_dynamic'
        )
        if rsv_task is not None:
            keyword = 'asset-geometry-usd-var-file'
            usd_file_rsv_unit = rsv_task.get_rsv_unit(
                keyword=keyword
            )
            return usd_file_rsv_unit.get_exists_result(version='latest', variants_extend=dict(var='hi'))

    @classmethod
    def _get_output_ass_file_(cls, rsv_scene_properties, rsv_task, look_pass_name):
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-look-ass-file'
            keyword_1 = 'asset-look-ass-sub-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-look-ass-file'
            keyword_1 = 'asset-temporary-look-ass-sub-file'
        else:
            raise TypeError()
        #
        if look_pass_name == 'default':
            look_ass_file_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_0)
            look_ass_file_path = look_ass_file_rsv_unit.get_result(version=version)
        else:
            look_ass_file_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_1)
            look_ass_file_path = look_ass_file_rsv_unit.get_result(
                version=version, variants_extend=dict(look_pass=look_pass_name)
            )
        return look_ass_file_path

    @classmethod
    def _get_look_pass_(cls, obj_opt):
        targets = obj_opt.get_targets('output')
        if targets:
            for i in targets:
                i_node = i.getNode()
                if i_node.getType() == 'LookFileBake':
                    return i.getName()
        return 'default'

    def set_guess(self):
        import lxusd.core as usd_core

        import lxkatana.core as ktn_core

        import lxresolver.core as rsv_core

        import lxkatana.dcc.objects as ktn_dcc_objects

        contents = []

        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)

        any_scene_file_path = ktn_dcc_objects.Scene.get_current_file_path()
        resolver = rsv_core.RsvBase.generate_root()
        rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
        if rsv_scene_properties:
            rsv_task = resolver.get_rsv_task(**rsv_scene_properties.value)

            input_dynamic_usd_file_path = self._get_input_dynamic_usd_file_(
                rsv_task.get_rsv_resource()
            )
            if input_dynamic_usd_file_path is not None:
                guess_frame_range = usd_core.UsdStageOpt(
                    input_dynamic_usd_file_path
                ).get_frame_range()
                #
                obj_opt.set(
                    'export.scheme', 'dynamic'
                )
                obj_opt.set(
                    'export.start_frame', guess_frame_range[0]
                )
                obj_opt.set(
                    'export.end_frame', guess_frame_range[1]
                )
                obj_opt.set('export.usd.input_dynamic_file', input_dynamic_usd_file_path)
            else:
                obj_opt.set(
                    'export.scheme', 'static'
                )
            #
            look_pass_name = self._get_look_pass_(obj_opt)
            obj_opt.set('export.look.pass', look_pass_name)
            #
            scheme = obj_opt.get('export.scheme')
            #
            output_ass_file_path = self._get_output_ass_file_(
                rsv_scene_properties, rsv_task, look_pass_name
            )
            if scheme == 'static':
                obj_opt.set_expression_enable('export.ass.output_file', False)
                obj_opt.set(
                    'export.ass.output_file', output_ass_file_path
                )
            elif scheme == 'dynamic':
                output_ass_file = bsc_storage.StgFileOpt(output_ass_file_path)
                path_base = output_ass_file.path_base
                ext = output_ass_file.ext
                file_path = u'{}.%04d{}'.format(path_base, ext)
                expression = '\'{}\' % (frame)'.format(file_path)
                obj_opt.set_expression_enable('export.ass.output_file', True)
                obj_opt.set_expression('export.ass.output_file', expression)
        else:
            contents.append(
                'current scene is not available'
            )

    def set_ass_export(self):
        import lxkatana.core as ktn_core

        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        #
        scheme = obj_opt.get('export.scheme')
        look_pass_name = obj_opt.get('export.look.pass')
        camera_path = obj_opt.get('export.camera.path')
        ass_file_path = obj_opt.get('export.ass.output_file')
        if not ass_file_path:
            return
        #
        rss = RenderManager.RenderingSettings()
        rss.ignoreROI = True
        rss.asynch = False
        rss.interactiveOutputs = True
        rss.interactiveMode = True
        #
        if not ktn_core.KtnUtil.get_is_ui_mode():
            # noinspection PyUnresolvedReferences
            from UI4.Manifest import Nodes2DAPI
            Nodes2DAPI.CreateExternalRenderListener(15900)
        #
        if scheme == 'static':
            rss.frame = ktn_core.NGNodeOpt(
                NodegraphAPI.GetRootNode()
            ).get('currentTime')
            RenderManager.StartRender(
                self.RENDER_MODE,
                node=self._ktn_obj,
                views=[camera_path],
                settings=rss
            )
        elif scheme == 'dynamic':
            stat_frame, end_frame = obj_opt.get('export.start_frame'), obj_opt.get('export.end_frame')
            if stat_frame != end_frame:
                frames = range(int(stat_frame), int(end_frame)+1)
                with bsc_log.LogProcessContext.create_as_bar(maximum=len(frames), label='ass sequence export') as l_p:
                    for i_frame in frames:
                        ktn_core.NGNodeOpt(
                            NodegraphAPI.GetRootNode()
                        ).set('currentTime', i_frame)
                        rss.frame = i_frame
                        RenderManager.StartRender(
                            self.RENDER_MODE,
                            node=self._ktn_obj,
                            views=[camera_path],
                            settings=rss
                        )
                        l_p.do_update()
                        bsc_log.Log.trace_method_result(
                            'ass sequence export',
                            'look-pass="{}", frame="{}"'.format(look_pass_name, i_frame)
                        )


class LxGeometrySettings(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def set_reset(self):
        import lxkatana.core as ktn_core

        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)

        obj_opt.set('usd.location', '')
        obj_opt.set('usd.file', '')
        obj_opt.set('usd.start_frame', 1001)
        obj_opt.set('usd.end_frame', 1001)
        obj_opt.set('usd.override_enable', False)
        obj_opt.set('usd.shot_override.file', '')

    def set_usd_guess(self):
        import lxusd.core as usd_core

        import lxkatana.core as ktn_core

        contents = []

        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        stage_opt = ktn_core.KtnStageOpt(self._ktn_obj)

        location = None
        scheme = obj_opt.get('options.scheme')
        if scheme == 'asset':
            location = '/root/world/geo/master'
        elif scheme == 'shot':
            rsv_asset = LxAsset._get_rsv_asset_auto_()
            if rsv_asset is not None:
                location = '/root/world/geo/assets/efx/{}'.format(
                    rsv_asset.get('asset')
                )
            else:
                contents.append(
                    'current scene is not available'
                )
        #
        if stage_opt.get_obj_exists(location) is True:
            obj_opt.set(
                'usd.location', location
            )
        else:
            contents.append(
                'location="{}" is not found'.format(location)
            )
        #
        guess_usd_file_path = self._get_usd_file_path_()
        if guess_usd_file_path:
            obj_opt.set(
                'usd.file', guess_usd_file_path
            )
            guess_frame_range = usd_core.UsdStageOpt(
                guess_usd_file_path
            ).get_frame_range()
            obj_opt.set(
                'usd.start_frame', guess_frame_range[0]
            )
            obj_opt.set(
                'usd.end_frame', guess_frame_range[1]
            )
        else:
            contents.append(
                'usd-file is not found'
            )

        _MacroMtd.set_warning_show(
            'look settings guess', contents
        )

    def _get_usd_file_path_(self):
        import lxkatana.core as ktn_core

        stage_opt = ktn_core.KtnStageOpt(self._ktn_obj)

        return stage_opt.get('/root/world/geo.info.usdOpArgs.fileName')

    def set_create(self):
        import lxkatana.core as ktn_core

        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        stage_opt = ktn_core.KtnStageOpt(self._ktn_obj)

        contents = []

        obj_opt.set('usd.override_enable', False)
        scheme = obj_opt.get('options.scheme')
        if scheme == 'asset':
            obj_opt.set('usd.override_enable', False)
        elif scheme == 'shot':
            location = obj_opt.get('usd.location')
            if stage_opt.get_obj_exists(location) is True:
                usd_file_path = self._set_override_usd_create_()
                obj_opt.set(
                    'usd.shot_override.file', usd_file_path
                )
            else:
                contents.append(
                    'location="{}" is not available'.format(location)
                )

        _MacroMtd.set_warning_show(
            'look settings guess', contents
        )

    def _set_override_usd_create_(self):
        import lxkatana.core as ktn_core

        import lxusd.scripts as us_scripts

        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        #
        file_path_src = obj_opt.get('usd.file')
        root = obj_opt.get('usd.shot_override.location')
        if root:
            location = obj_opt.get('usd.location')
            #
            return us_scripts.ShotUsdCombine(
                file_path_src, location[len(root):]
            ).set_run()


class LxCamera(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def set_reset(self):
        import lxkatana.core as ktn_core

        #
        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        obj_opt.set_port_raw(
            'alembic.enable', 0
        )
        obj_opt.set_port_raw(
            'alembic.file', ''
        )
        obj_opt.set_port_raw(
            'alembic.location', '/root/world/cam/cameras/main'
        )

    def set_load(self):
        import lxresolver.core as rsv_core

        import lxkatana.core as ktn_core

        import lxkatana.dcc.objects as ktn_dcc_objects

        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        #
        obj_opt.set_port_raw(
            'alembic.enable',
            0
        )
        #
        contents = []
        #
        f = ktn_dcc_objects.Scene.get_current_file_path()
        if f:
            resolver = rsv_core.RsvBase.generate_root()
            rsv_task = resolver.get_rsv_task_by_any_file_path(f)
            if rsv_task is not None:
                rsv_entity = rsv_task.get_rsv_resource()
                rsv_camera_task = rsv_entity.get_rsv_task(
                    step='cam',
                    task='camera'
                )
                if rsv_camera_task is not None:
                    rsv_unit = rsv_camera_task.get_rsv_unit(
                        keyword='asset-camera-main-abc-file'
                    )
                    file_path = rsv_unit.get_result(version='latest')
                    if file_path:
                        obj_opt.set_port_raw(
                            'alembic.enable',
                            1
                        )
                        #
                        obj_opt.set_port_raw(
                            'alembic.file',
                            file_path
                        )
                        obj_opt.set_port_raw(
                            'alembic.location',
                            '/root/world/cam/cameras/main'
                        )
                else:
                    contents.append(
                        u'asset="{}" camera task is non-exists'.format(rsv_entity.path)
                    )
            else:
                contents.append(
                    u'file={} is not not available'.format(f)
                )
        else:
            contents.append(
                u'file={} is not not available'.format(f)
            )

        _MacroMtd.set_warning_show(
            'camera load', contents
        )

    def set_variable_register(self):
        import lxkatana.core as ktn_core

        #
        camera_scheme = ktn_core.NGNodeOpt(self._ktn_obj).get_port_raw(
            'lynxi_variants.camera_scheme'
        )
        key = 'camera'
        if camera_scheme in ['character']:
            values = [
                'full_body', 'upper_body', 'upper_body_35', 'upper_body_50', 'close_up',
                'add_0', 'add_1',
                'shot',
                'asset_free', 'shot_free'
            ]
            ktn_core.VariablesSetting().register(
                key, values
            )
        elif camera_scheme in ['prop']:
            values = [
                'full', 'half',
                'add_0', 'add_1'
                         'shot',
                'asset_free', 'shot_free'
            ]
            ktn_core.VariablesSetting().register(
                key, values
            )

    def set_front_fill_to_front(self):
        import lxusd.core as usd_core

        import lxkatana.core as ktn_core

        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        stage_opt = ktn_core.KtnStageOpt(self._ktn_obj)

        location = '/root/world/geo'

        file_path = stage_opt.get(
            '/root/world/geo.info.usdOpArgs.fileName'.format(location)
        )
        translate_offset = stage_opt.get(
            '/root/world/geo/master.xform.interactive.translate'.format(location)
        )
        if file_path:
            root = '/master'
            sub_locations = [
                '/master/hi',
                '/master/shape',
            ]
            s_opt = usd_core.UsdStageOpt(
                file_path
            )
            [s_opt.set_active_at(i, True) for i in sub_locations]
            g = s_opt.compute_geometry_args(root)
            if translate_offset:
                x_o, y_o, z_o = translate_offset
            else:
                x_o, y_o, z_o = 0, 0, 0
            #
            (x, y, z), (c_x, c_y, c_z), (w, h, d) = g
            #
            w += .1
            h += .2
            c_y += .1
            #
            (t_x, t_y, t_z), (r_x, r_y, r_z), (s_x, s_y, s_z) = bsc_core.CameraMtd.compute_front_transformation(
                geometry_args=((x, y, z), (c_x, c_y, c_z), (w, h, d)),
                angle=1,
            )
            #
            obj_opt.set('settings.screen_modify_mode', 'fill')
            #
            obj_opt.set('cameras.front.translate', (t_x+x_o, t_y+y_o, t_z+z_o))
            obj_opt.set('cameras.front.rotate', (r_x, r_y, r_z))
            obj_opt.set('cameras.front.scale', (s_x, s_y, s_z))
            #
            width, height = int(w*50), int(h*50)
            #
            obj_opt.set(
                'cameras.front.render_resolution', '{}x{}'.format(width, height)
            )

    def set_front_fill_to_all(self):
        import lxusd.core as usd_core

        import lxkatana.core as ktn_core

        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        stage_opt = ktn_core.KtnStageOpt(self._ktn_obj)

        location = '/root/world/geo'

        file_path = stage_opt.get(
            '/root/world/geo.info.usdOpArgs.fileName'.format(location)
        )
        pivot = stage_opt.get(
            '/root/world/geo/master.xform.interactive.translate'.format(location)
        )
        if file_path:
            root = '/master'
            sub_locations = [
                '/master/hi',
                '/master/shape',
            ]
            s_opt = usd_core.UsdStageOpt(
                file_path
            )
            [s_opt.set_active_at(i, True) for i in sub_locations]
            g = s_opt.compute_geometry_args(root)
            if pivot:
                x_o, y_o, z_o = pivot
            else:
                x_o, y_o, z_o = 0, 0, 0
            (x, y, z), (c_x, c_y, c_z), (w, h, d) = g
            #
            r = s_opt.get_radius(pivot)
            w = r*2
            #
            w += .1
            h += .2
            c_y += .1
            #
            (t_x, t_y, t_z), (r_x, r_y, r_z), (s_x, s_y, s_z) = bsc_core.CameraMtd.compute_front_transformation(
                geometry_args=((x, y, z), (c_x, c_y, c_z), (w, h, d)),
                angle=1,
                mode=1
            )
            #
            obj_opt.set('settings.screen_modify_mode', 'fill')
            #
            obj_opt.set('cameras.front.translate', (t_x+x_o, t_y+y_o, t_z+z_o))
            obj_opt.set('cameras.front.rotate', (r_x, r_y, r_z))
            obj_opt.set('cameras.front.scale', (s_x, s_y, s_z))
            #
            multipy = 4
            #
            width, height = int(w*50*multipy), int(h*50*multipy)
            #
            width_, height_ = bsc_core.RawSizeMtd.set_clamp_to(
                width, height, 2048, 512
            )
            #
            obj_opt.set(
                'cameras.front.render_resolution', '{}x{}'.format(int(width_), int(height_))
            )


# noinspection PyMethodMayBeStatic
class LxRenderer(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj
        #
        self._search_dic = collections.OrderedDict(
            [
                ('camera', ['lynxi_variants.camera_enable', 'lynxi_variants.cameras']),
                ('layer', ['lynxi_variants.layer_enable', 'lynxi_variants.layers']),
                ('light_pass', ['lynxi_variants.light_pass_enable', 'lynxi_variants.light_passes']),
                ('look_pass', ['lynxi_variants.look_pass_enable', 'lynxi_variants.look_passes']),
                ('quality', ['lynxi_variants.quality_enable', 'lynxi_variants.qualities']),
            ]
        )

    def _get_variable_switches_(self):
        pass

    def set_reset(self):
        pass

    def _set_create_(self):
        import collections

        import lxkatana.core as ktn_core

        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        variants_dic = collections.OrderedDict()
        for k, v in self._search_dic.items():
            enable_port_path, values_port_path = v
            i_raw = obj_opt.get_port_raw(
                values_port_path
            )
            if i_raw:
                i_variants = map(lambda i: str(i).strip(), i_raw.split(','))
            else:
                i_variants = []
            #
            variants_dic[k] = i_variants
        #
        variant_mapper = {
            'layer': 'lynxi_variants.layer',
            'quality': 'lynxi_variants.quality',
            'camera': 'lynxi_variants.camera',
            'look_pass': 'lynxi_variants.look_pass',
            'light_pass': 'lynxi_variants.light_pass'
        }
        combinations = bsc_core.RawVariablesMtd.get_all_combinations(
            variants_dic
        )
        x, y = 0, 0

        for seq, i_variants in enumerate(combinations):
            i_label = '__'.join(['{}'.format(v) for k, v in i_variants.items()])
            #
            i_settings_name = 'settings__{}'.format(i_label)
            i_settings_path = '{}/{}'.format(obj_opt.get_path(), i_settings_name)
            #
            i_settings = ktn_core.NGNodeOpt._set_create_(i_settings_path, 'lx_render_settings')
            i_settings_opt = ktn_core.NGNodeOpt(i_settings)
            i_x, i_y = x, y-(seq+1)*240
            i_settings_opt.set_position(
                i_x, i_y
            )
            i_settings_opt.set_color((.75, .5, .25))
            obj_opt.get_send_port('input').connect(
                i_settings_opt.get_input_port('input')
            )
            i_settings_opt.set_port_raw('variables.over', 1)
            for j_k, j_v in i_variants.items():
                i_settings_opt.set_port_raw(
                    variant_mapper[j_k], j_v
                )
            #
            i_renderer_name = 'renderer__{}'.format(i_label)
            i_renderer_path = '{}/{}'.format(obj_opt.get_path(), i_renderer_name)
            i_renderer = ktn_core.NGNodeOpt._set_create_(i_renderer_path, 'Render')
            i_renderer_opt = ktn_core.NGNodeOpt(i_renderer)
            i_renderer_opt.set_port_raw(
                'passName', i_renderer_name
            )
            i_renderer_opt.set_position(
                i_x, i_y-120
            )
            i_renderer_opt.set_color((.5, .25, .25))
            i_settings_opt.get_output_port('output').connect(
                i_renderer_opt.get_input_port('input')
            )

    def _set_clear_(self):
        import lxkatana.core as ktn_core

        [ktn_core.NGNodeOpt(i).do_delete() for i in ktn_core.NGNodeOpt(self._ktn_obj).get_children()]

    def set_refresh(self):
        import lxkatana.core as ktn_core

        variants = ktn_core.VariablesSetting().get_variants()

        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        for k, v in variants.items():
            if k in self._search_dic:
                enable_port_path, values_port_path = self._search_dic[k]
                if obj_opt.get_port_raw(enable_port_path) == 1:
                    obj_opt.set_port_raw(
                        values_port_path, ', '.join(v)
                    )

    def set_create(self):
        Utils.UndoStack.OpenGroup(self._ktn_obj.getName())
        try:
            self._set_clear_()
            self._set_create_()
        except Exception:
            raise
        finally:
            Utils.UndoStack.CloseGroup()

    def set_submit_to_deadline(self):
        import lxkatana.dcc.objects as ktn_dcc_objects

        import lxtool.submitter.gui.widgets as smt_gui_widgets

        file_path = ktn_dcc_objects.Scene.get_current_file_path()

        w = smt_gui_widgets.PnlSubmitterForAssetRender(
            hook_option='file={}'.format(
                file_path
            )
        )
        w.set_window_show()


class LxVariant(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def _get_key_(self):
        import lxkatana.core as ktn_core

        return ktn_core.NGNodeOpt(self._ktn_obj).get_port_raw('variableName')

    @classmethod
    def _get_values_(cls, ktn_obj):
        import lxkatana.core as ktn_core

        ktn_port = ktn_core.NGNodeOpt(ktn_obj).get_port('patterns')
        return [ktn_core.NGPortOpt(i).get() for i in ktn_core.NGNodeOpt(ktn_port).get_children()]

    def set_variable_register(self):
        import lxkatana.core as ktn_core

        key = self._get_key_()
        values = self._get_values_(self._ktn_obj)
        ktn_core.VariablesSetting().register(
            key, values
        )


class LxVariantChoose(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def _set_value_update_(self, values):
        import lxkatana.core as ktn_core

        #
        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)

        key = 'lynxi_variants.value'
        value = obj_opt.get(key)
        obj_opt.set_as_enumerate(key, values)
        if value in values:
            obj_opt.set(
                key, value
            )

    def set_variable_value_load(self):
        import lxkatana.core as ktn_core

        #
        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        #
        key = obj_opt.get('lynxi_variants.key')
        source_objs = obj_opt.get_all_source_objs()
        values = []
        if source_objs:
            for i_ktn_obj in source_objs:
                i_obj_opt = ktn_core.NGNodeOpt(i_ktn_obj)
                if i_obj_opt.type_name == 'VariableSwitch':
                    i_key = i_obj_opt.get('variableName')
                    if i_key == key:
                        i_values = LxVariant._get_values_(i_ktn_obj)
                        [values.append(j) for j in i_values if j not in values]
        #
        if values:
            self._set_value_update_(values)
        else:
            self._set_value_update_(['None'])
        return


class LxLook(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj


class LxWorkspace(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def set_workspace_create(self):
        import lxkatana.core as ktn_core

        import lxkatana.fnc.objects as ktn_fnc_objects

        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)

        ktn_fnc_objects.FncCreatorForLookWorkspaceOld(
            option=dict(
                location=obj_opt.get_path()
            )
        ).set_run()

    def set_look_pass_add(self):
        pass


# noinspection PyUnusedLocal
class LxLight(object):
    def __init__(self, ktn_obj):
        self._ktn_obj = ktn_obj

    def set_guess(self):
        import lxresolver.core as rsv_core

        import lxkatana.core as ktn_core

        import lxkatana.dcc.objects as ktn_dcc_objects

        content = None
        #
        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        #
        scheme = obj_opt.get('options.scheme')
        #
        rsv_asset = None
        resolver = rsv_core.RsvBase.generate_root()
        #
        rsv_asset_path = obj_opt.get_port_raw('options.asset')
        if rsv_asset_path:
            rsv_asset = LxAsset._get_rsv_asset_(rsv_asset_path)
            if rsv_asset is not None:
                pass
            else:
                content = u'asset="{}" is not available'.format(rsv_asset_path)
        else:
            file_path = ktn_dcc_objects.Scene.get_current_file_path()
            rsv_task = resolver.get_rsv_task_by_any_file_path(file_path)
            if rsv_task:
                rsv_asset = rsv_task.get_rsv_resource()
            else:
                content = u'file="{}" is not available'.format(file_path)

        if rsv_asset is not None:
            self.__set_rsv_asset_(rsv_asset)

    def __set_rsv_asset_(self, rsv_asset):
        import lxkatana.core as ktn_core

        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)

        obj_opt.set(
            'options.asset', rsv_asset.path
        )

    def set_create(self):
        pass

    def set_refresh_light_rig(self):
        import lxkatana.core as ktn_core

        import lxshotgun.rsv.scripts as stg_rsv_scripts

        contents = []

        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)

        rsv_asset_path = obj_opt.get_port_raw('options.asset')
        if rsv_asset_path:
            rsv_asset = LxAsset._get_rsv_asset_(rsv_asset_path)
        else:
            rsv_asset = LxAsset._get_rsv_asset_auto_()
        #
        if rsv_asset is not None:
            self.__set_rsv_asset_(rsv_asset)
            rsv_project = rsv_asset.get_rsv_project()
            name = obj_opt.get('lights.light_rig.name')
            index = obj_opt.get('lights.light_rig.index') or 0

            light_rig_rsv_assets = stg_rsv_scripts.RsvStgProjectOpt(
                rsv_project
            ).get_standard_light_rig_rsv_assets()
            if light_rig_rsv_assets:
                #
                names = [i.name for i in light_rig_rsv_assets]
                obj_opt.set_as_enumerate(
                    'lights.light_rig.name',
                    names
                )
                index = max(min(int(index), len(names)-1), 0)
                if name != 'None':
                    if name in names:
                        obj_opt.set('lights.light_rig.name', name)
                    else:
                        obj_opt.set('lights.light_rig.name', names[index])
                else:
                    obj_opt.set('lights.light_rig.name', names[index])
            else:
                contents.append(
                    'light-rig(s) is not found'
                )

        _MacroMtd.set_warning_show(
            'light rig refresh', contents
        )

    def set_load_light_rig(self):
        import lxkatana.core as ktn_core

        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        asset = obj_opt.get('lights.light_rig.name')

        self._set_load_from_asset_light_rig_(asset)

    def _set_load_from_asset_light_rig_(self, light_rig_asset):
        import lxkatana.core as ktn_core

        contents = []

        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)

        rsv_asset_path = obj_opt.get_port_raw('options.asset')
        if rsv_asset_path:
            rsv_asset = LxAsset._get_rsv_asset_(rsv_asset_path)
        else:
            rsv_asset = LxAsset._get_rsv_asset_auto_()
        #
        if rsv_asset is not None:
            self.__set_rsv_asset_(rsv_asset)

            rsv_project = rsv_asset.get_rsv_project()

            light_rsv_task = rsv_project.get_rsv_task(
                asset=light_rig_asset, step='lgt', task='lighting'
            )
            if light_rsv_task:
                light_group_rsv_unit = light_rsv_task.get_rsv_unit(
                    keyword='asset-live_group-file'
                )
                light_group_file_path = light_group_rsv_unit.get_result(
                    version='latest'
                )
                if light_group_file_path:
                    obj_opt.set(
                        'lights.light_rig.live_group', light_group_file_path
                    )
                else:
                    contents.append(
                        u'light-rig="{}" file is non-exists, use default'.format(
                            light_rig_asset
                        )
                    )
            #
            # CacheManager.flush()
            self.set_live_groups_update()
        #
        _MacroMtd.set_warning_show(
            'light rig load', contents
        )

    def set_live_groups_update(self):
        import lxkatana.core as ktn_core

        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)

        children = obj_opt.get_children(type_includes=['LiveGroup'])

        for i in children:
            i.reloadFromSource()
