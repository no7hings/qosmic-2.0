# coding:utf-8
import six

import collections

import lxcontent.core as ctt_core

import lxresource as bsc_resource

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.dcc.objects as bsc_dcc_objects

import lxbasic.fnc.abstracts as bsc_fnc_abstracts

import lxresolver.core as rsv_core

from lxutil.rsv import utl_rsv_obj_abstract


class RsvUsdAssetSetCreator(object):
    STEP_MAPPER = {
        'mod': 'model',
        'grm': 'groom',
        'rig': 'rig',
        'effect': 'efx',
        'srf': 'surface',
    }
    TASK_MAPPER = {
        'modeling': 'model',
        'groom': 'groom',
        'rigging': 'rig',
        'effects': 'effect',
        'surfacing': 'surface',
    }
    VARIANTS_MAPPER = {
        'modeling': 'variants.asset_version.model',
        'groom': 'variants.asset_version.groom',
        'rigging': 'variants.asset_version.rig',
        'effects': 'variants.asset_version.effect',
        'surfacing': 'variants.asset_version.surface',
        #
        'model_override': 'variants.asset_version_override.model',
        'groom_override': 'variants.asset_version_override.groom',
        'rig_override': 'variants.asset_version_override.rig',
        'effect_override': 'variants.asset_version_override.effect',
        'surface_override': 'variants.asset_version_override.surface',
        #
        'animation': 'variants.shot_version.animation',
        #
        'animation_override': 'variants.shot_version_override.animation',
    }
    VARIANTS_MAPPER_0 = {
        'model_main': 'variants.asset_version.model',
        'groom_main': 'variants.asset_version.groom',
        'rig_main': 'variants.asset_version.rig',
        'effect_main': 'variants.asset_version.effect',
        'surface_main': 'variants.asset_version.surface',
        #
        'model_override': 'variants.asset_version_override.model',
        'groom_override': 'variants.asset_version_override.groom',
        'rig_override': 'variants.asset_version_override.rig',
        'effect_override': 'variants.asset_version_override.effect',
        'surface_override': 'variants.asset_version_override.surface',
        #
        'animation': 'variants.shot_version.animation',
        #
        'animation_override': 'variants.shot_version_override.animation',
    }
    VARIANTS_VERSION_INDEX = {
        'model_main': -1,
        'groom_main': -1,
        'rig_main': 0,
        'effect_main': -1,
        'surface_main': -1,
    }

    def __init__(self, rsv_asset):
        self._rsv_asset = rsv_asset

    @classmethod
    def _get_shot_asset_cache(cls, rsv_asset, rsv_shot):
        file_path = cls._generate_shot_set_dress_usd_file_path_as_latest(rsv_shot)
        if file_path:
            yml_file_path = bsc_storage.StgTmpYamlMtd.get_file_path(file_path, 'shot-asset/{}'.format(rsv_asset.name))
            file_opt = bsc_storage.StgFileOpt(yml_file_path)
            if file_opt.get_is_exists() is True:
                return file_opt.set_read()
            if bsc_core.SysBaseMtd.get_is_linux():
                dict_ = cls._get_shot_asset_dict(rsv_asset, rsv_shot)
                file_opt.set_write(dict_)
                return dict_
            return {}
        return ctt_core.Content(value={})

    @classmethod
    def _get_shot_asset_dict(cls, rsv_asset, rsv_shot):
        import lxusd.core as usd_core

        dict_ = collections.OrderedDict()

        shot_set_dress_usd_file_path = cls._generate_shot_set_dress_usd_file_path_as_latest(rsv_shot)
        #
        # noinspection PyBroadException
        try:
            paths = usd_core.UsdStageOpt(
                shot_set_dress_usd_file_path
            ).find_obj_paths(
                '/assets/*/{}*'.format(
                    rsv_asset.get('asset')
                )
            )
            if paths:
                paths = bsc_core.RawTextsOpt(paths).sort_by_number()
            #
            for i_location in paths:
                i_shot_asset = i_location.split('/')[-1]
                dict_[i_shot_asset] = i_location
        except:
            bsc_log.Log.trace_method_error(
                'shot-asset resolver',
                'file="{}" is error'.format(shot_set_dress_usd_file_path)
            )
        finally:
            return dict_

    @classmethod
    def _get_shot_asset_override_dict(cls, rsv_asset, rsv_shot, rsv_scene_properties):
        dict_ = collections.OrderedDict()
        shot_asset = rsv_asset.get('asset')
        asset_shot = rsv_shot.get('shot')
        #
        workspace_cur = rsv_scene_properties.get('workspace')
        step_cur = rsv_scene_properties.get('step')
        cur_task = rsv_scene_properties.get('task')
        cur_version = rsv_scene_properties.get('version')
        cur_rsv_task = rsv_asset.get_rsv_task(
            step=step_cur,
            task=cur_task
        )
        if workspace_cur == rsv_scene_properties.get('workspaces.source'):
            pass
        elif workspace_cur == rsv_scene_properties.get('workspaces.release'):
            pass
        elif workspace_cur == rsv_scene_properties.get('workspaces.temporary'):
            comp_register_usd_file_rsv_unit = cur_rsv_task.get_rsv_unit(
                keyword='asset-temporary-shot_asset-component-registry-usd-file'
            )
            register_usd_file_path = comp_register_usd_file_rsv_unit.get_result(
                version=cur_version,
                variants_extend=dict(
                    asset_shot=asset_shot,
                    shot_asset=shot_asset
                )
            )
            if register_usd_file_path is not None:
                dict_[shot_asset] = register_usd_file_path
        return dict_

    @classmethod
    def _get_rsv_asset_shots(cls, rsv_asset):
        lis = []
        #
        resolver = rsv_core.RsvBase.generate_root()
        #
        rsv_shots = resolver.get_rsv_resources(
            project=rsv_asset.get('project'), branch='shot'
        )
        for i_rsv_shot in rsv_shots:
            i_rsv_shot_set_task = i_rsv_shot.get_rsv_task(
                step='set', task='registry'
            )
            if i_rsv_shot_set_task is not None:
                i_rsv_shot_set_usd_file = i_rsv_shot_set_task.get_rsv_unit(
                    keyword='shot-set-dress-usd-file'
                )
                i_shot_set_usd_file_path = i_rsv_shot_set_usd_file.get_result(
                    version='latest'
                )
                if i_shot_set_usd_file_path is not None:
                    shot_assets_dict = cls._get_shot_asset_cache(
                        rsv_asset, i_rsv_shot
                    )
                    if shot_assets_dict:
                        lis.append(i_rsv_shot)
        return lis

    @classmethod
    def _get_shot_frame_range(cls, rsv_shot):
        import lxusd.core as usd_core

        shot_set_dress_usd_file_path = cls._generate_shot_set_dress_usd_file_path_as_latest(rsv_shot)
        if shot_set_dress_usd_file_path:
            return usd_core.UsdStageOpt(
                shot_set_dress_usd_file_path
            ).get_frame_range()

    @classmethod
    def _generate_asset_set_dress_usd_file_path_as_latest(cls, rsv_asset):
        rsv_asset_set_task = rsv_asset.get_rsv_task(
            step='set', task='registry'
        )
        if rsv_asset_set_task is not None:
            asset_set_dress_usd_file_rsv_unit = rsv_asset_set_task.get_rsv_unit(
                keyword='asset-set-dress-usd-file'
            )
            return asset_set_dress_usd_file_rsv_unit.get_result(
                version='latest'
            )

    @classmethod
    def _generate_shot_set_dress_usd_file_path_as_latest(cls, rsv_shot):
        rsv_shot_set_task = rsv_shot.get_rsv_task(
            step='set', task='registry'
        )
        if rsv_shot_set_task is not None:
            shot_set_dress_usd_file_rsv_unit = rsv_shot_set_task.get_rsv_unit(
                keyword='shot-set-dress-usd-file'
            )
            return shot_set_dress_usd_file_rsv_unit.get_result(
                version='latest'
            )

    @classmethod
    def _generate_asset_usd_file_path_as_new(cls, rsv_asset, rsv_scene_properties):
        if rsv_scene_properties:
            resolver = rsv_core.RsvBase.generate_root()
            workspace = rsv_scene_properties.get('workspace')
            version = rsv_scene_properties.get('version')
            rsv_task = resolver.get_rsv_task(**rsv_scene_properties.value)
            if workspace in {
                rsv_scene_properties.get('workspaces.source'),
                rsv_scene_properties.get('workspaces.user')
            }:
                usd_file_rsv_unit = rsv_task.get_rsv_unit(
                    keyword='asset-source-asset-set-usd-file'
                )
                # debug for usd update error, auto update version
                usd_file_path = usd_file_rsv_unit.get_result(version='new')
            elif workspace in {
                rsv_scene_properties.get('workspaces.release')
            }:
                usd_file_rsv_unit = rsv_task.get_rsv_unit(
                    keyword='asset-asset-set-usd-file'
                )
                usd_file_path = usd_file_rsv_unit.get_result(version=version)
            elif workspace in {
                rsv_scene_properties.get('workspaces.temporary')
            }:
                usd_file_rsv_unit = rsv_task.get_rsv_unit(
                    keyword='asset-temporary-asset-set-usd-file'
                )
                usd_file_path = usd_file_rsv_unit.get_result(version=version)
            else:
                raise RuntimeError()
        else:
            usd_file_path = '{}{}.usda'.format(
                bsc_storage.StgUserMtd.get_user_temporary_directory(),
                rsv_asset.path
            )
        return usd_file_path

    @classmethod
    def _generate_asset_usd_file_path_as_latest(cls, rsv_asset, rsv_scene_properties):
        if rsv_scene_properties:
            resolver = rsv_core.RsvBase.generate_root()
            workspace = rsv_scene_properties.get('workspace')
            version = rsv_scene_properties.get('version')
            rsv_task = resolver.get_rsv_task(**rsv_scene_properties.value)
            if workspace in {
                rsv_scene_properties.get('workspaces.source'),
                rsv_scene_properties.get('workspaces.user')
            }:
                usd_file_rsv_unit = rsv_task.get_rsv_unit(
                    keyword='asset-source-asset-set-usd-file'
                )
                usd_file_path = usd_file_rsv_unit.get_result(version='latest')
            elif workspace in {
                rsv_scene_properties.get('workspaces.release')
            }:
                usd_file_rsv_unit = rsv_task.get_rsv_unit(
                    keyword='asset-asset-set-usd-file'
                )
                usd_file_path = usd_file_rsv_unit.get_result(version=version)
            elif workspace in {
                rsv_scene_properties.get('workspaces.temporary')
            }:
                usd_file_rsv_unit = rsv_task.get_rsv_unit(
                    keyword='asset-temporary-asset-set-usd-file'
                )
                usd_file_path = usd_file_rsv_unit.get_result(version=version)
            else:
                raise RuntimeError()
        else:
            usd_file_path = '{}{}.usda'.format(
                bsc_storage.StgUserMtd.get_user_temporary_directory(),
                rsv_asset.path
            )
        return usd_file_path

    @classmethod
    def _generate_asset_shot_usd_file_path_as_new(cls, rsv_asset, rsv_shot, rsv_scene_properties):
        usd_file_path = None
        if rsv_scene_properties:
            resolver = rsv_core.RsvBase.generate_root()
            rsv_task = resolver.get_rsv_task(**rsv_scene_properties.value)
            workspace = rsv_scene_properties.get('workspace')
            version = rsv_scene_properties.get('version')
            if workspace in {
                rsv_scene_properties.get('workspaces.source'),
                rsv_scene_properties.get('workspaces.user')
            }:
                usd_file_rsv_unit = rsv_task.get_rsv_unit(
                    keyword='asset-source-shot-set-usd-file'
                )
                usd_file_path = usd_file_rsv_unit.get_result(
                    version='new',
                    variants_extend=dict(
                        asset_shot=rsv_shot.get('shot')
                    )
                )
            elif workspace in {
                rsv_scene_properties.get('workspaces.release')
            }:
                usd_file_rsv_unit = rsv_task.get_rsv_unit(
                    keyword='asset-shot-set-usd-file'
                )
                usd_file_path = usd_file_rsv_unit.get_result(
                    version=version,
                    variants_extend=dict(
                        asset_shot=rsv_shot.get('shot')
                    )
                )
            elif workspace in {
                rsv_scene_properties.get('workspaces.temporary')
            }:
                usd_file_rsv_unit = rsv_task.get_rsv_unit(
                    keyword='asset-temporary-shot-set-usd-file'
                )
                usd_file_path = usd_file_rsv_unit.get_result(
                    version=version,
                    variants_extend=dict(
                        asset_shot=rsv_shot.get('shot')
                    )
                )
        else:
            usd_file_path = '{}{}.usda'.format(
                bsc_storage.StgUserMtd.get_user_temporary_directory(),
                rsv_asset.path
            )
        return usd_file_path

    @classmethod
    def _get_asset_usd_set_dress_variant_dict(cls, rsv_asst):
        usd_file_path = cls._generate_asset_set_dress_usd_file_path_as_latest(rsv_asst)
        return cls._get_usd_file_variant_dict(usd_file_path)

    @classmethod
    def _get_asset_usd_set_dress_variant_cache(cls, rsv_asset):
        file_path = cls._generate_asset_set_dress_usd_file_path_as_latest(rsv_asset)
        if file_path:
            yml_file_path = bsc_storage.StgTmpYamlMtd.get_file_path(file_path, 'asset-versions/{}'.format(rsv_asset.name))
            file_opt = bsc_storage.StgFileOpt(yml_file_path)
            if file_opt.get_is_exists() is True:
                return file_opt.set_read()
            else:
                if bsc_core.SysBaseMtd.get_is_linux():
                    dict_ = cls._get_asset_usd_set_dress_variant_dict(rsv_asset)
                    file_opt.set_write(dict_)
                    return dict_
                return {}
        else:
            return ctt_core.Content(value={})

    @classmethod
    def _get_shot_usd_set_dress_variant_dict(cls, rsv_shot):
        usd_file_path = cls._generate_shot_set_dress_usd_file_path_as_latest(rsv_shot)
        return cls._get_usd_file_variant_dict(usd_file_path)

    @classmethod
    def _get_usd_file_variant_dict(cls, usd_file_path):
        import lxusd.core as usd_core

        c = ctt_core.Content(value=collections.OrderedDict())
        usd_stage_opt = usd_core.UsdStageOpt(usd_file_path)
        usd_prim_opt = usd_core.UsdPrimOpt(usd_stage_opt.get_obj('/master'))
        if usd_file_path:
            usd_variant_dict = usd_prim_opt.get_variant_dict()
            for i_variant_set_name, i_port_path in cls.VARIANTS_MAPPER.items():
                c.set(
                    '{}.port_path'.format(i_variant_set_name),
                    i_port_path
                )
                if i_variant_set_name in usd_variant_dict:
                    i_current_variant_name, i_variant_names = usd_variant_dict[i_variant_set_name]
                    c.set(
                        '{}.variant_names'.format(i_variant_set_name),
                        i_variant_names
                    )
                    c.set(
                        '{}.variant_name'.format(i_variant_set_name),
                        i_current_variant_name
                    )
                else:
                    c.set(
                        '{}.variant_names'.format(i_variant_set_name),
                        ['None']
                    )
                    c.set(
                        '{}.variant_name'.format(i_variant_set_name),
                        'None'
                    )
        return c.value

    @classmethod
    def _get_usd_variant_dict(cls, rsv_asset, rsv_scene_properties, asset_usd_file_path):
        import lxusd.core as usd_core

        c = ctt_core.Content(value=collections.OrderedDict())
        step_cur = rsv_scene_properties.get('step')
        cur_key = cls.STEP_MAPPER[step_cur]
        usd_stage_opt = usd_core.UsdStageOpt(asset_usd_file_path)
        usd_prim_opt = usd_core.UsdPrimOpt(usd_stage_opt.get_obj('/master'))
        usd_variant_dict = usd_prim_opt.get_variant_dict()
        asset_set_dress_usd_file_path = cls._generate_asset_set_dress_usd_file_path_as_latest(rsv_asset)
        if asset_set_dress_usd_file_path:
            variants_mapper = cls.VARIANTS_MAPPER
        else:
            variants_mapper = cls.VARIANTS_MAPPER_0
        #
        for i_variant_set_name, i_port_path in variants_mapper.items():
            c.set(
                '{}.port_path'.format(i_variant_set_name),
                i_port_path
            )
            if i_variant_set_name in usd_variant_dict:
                i_current_variant_name, i_variant_names = usd_variant_dict[i_variant_set_name]
                if i_variant_names:
                    c.set(
                        '{}.variant_names'.format(i_variant_set_name),
                        i_variant_names
                    )
                    if i_variant_set_name.endswith('override'):
                        if step_cur in cls.STEP_MAPPER:
                            per_key = cls.STEP_MAPPER[step_cur]
                            if i_variant_set_name == '{}_override'.format(per_key):
                                i_current_variant_name = i_variant_names[-1]
                    else:
                        if step_cur in cls.STEP_MAPPER:
                            if i_variant_set_name in cls.TASK_MAPPER:
                                per_key = cls.TASK_MAPPER[i_variant_set_name]
                                if cur_key == per_key:
                                    i_current_variant_name = 'None'
                    #
                    if i_variant_set_name in cls.VARIANTS_VERSION_INDEX:
                        if i_variant_names:
                            i_current_variant_name = i_variant_names[cls.VARIANTS_VERSION_INDEX[i_variant_set_name]]
                    #
                    c.set(
                        '{}.variant_name'.format(i_variant_set_name),
                        i_current_variant_name
                    )
            else:
                c.set(
                    '{}.variant_names'.format(
                        i_variant_set_name
                    ),
                    ['None']
                )
                c.set(
                    '{}.variant_name'.format(i_variant_set_name),
                    'None'
                )
        return c.value

    @classmethod
    def _update_asset_all_variants(cls, configure, rsv_asset, rsv_scene_properties):
        asset_step_query = rsv_scene_properties.get('asset_steps')
        asset_task_query = rsv_scene_properties.get('asset_tasks')
        keys = [
            'model',
            'groom',
            'rig',
            'effect',
            'surface',
            'light',
        ]
        for i_key in keys:
            i_step = asset_step_query.get(i_key)
            i_task = asset_task_query.get(i_key)
            #
            i_rsv_task = rsv_asset.get_rsv_task(
                step=i_step, task=i_task
            )
            if i_rsv_task is not None:
                i_version_main_dict = cls._generate_asset_main_variants_at(
                    i_rsv_task
                )
                configure.set(
                    'asset.version_main.{}'.format(i_key), i_version_main_dict
                )
                i_version_override_dict = cls._generate_asset_override_variants_at(
                    rsv_scene_properties,
                    i_rsv_task
                )
                configure.set(
                    'asset.version_override.{}'.format(i_key), i_version_override_dict
                )

        cls._update_asset_component_variants(configure, rsv_asset)

    @classmethod
    def _update_asset_component_variants(cls, configure, rsv_asset):
        rsv_tasks = rsv_asset.get_rsv_tasks(task='mod_var_*')
        if rsv_tasks:
            for i_rsv_task in rsv_tasks:
                i_key = i_rsv_task.get_name()
                configure.set(
                    'asset.component.{}_component_main'.format(i_key),
                    cls._generate_asset_main_variants_at(i_rsv_task)
                )

    @classmethod
    def _generate_asset_main_variants_at(cls, cur_rsv_task):
        dict_ = collections.OrderedDict()
        comp_register_usd_file_rsv_unit = cur_rsv_task.get_rsv_unit(
            keyword='asset-component-registry-usd-file'
        )
        comp_register_usd_file_paths = comp_register_usd_file_rsv_unit.get_result(
            version='all'
        )
        for i_file_path in comp_register_usd_file_paths:
            i_properties = comp_register_usd_file_rsv_unit.generate_properties_by_result(i_file_path)
            i_version = i_properties.get('version')
            dict_[i_version] = i_file_path
        return dict_

    @classmethod
    def _generate_asset_override_variants_at(cls, rsv_scene_properties, cur_rsv_task):
        dict_ = collections.OrderedDict()
        #
        workspace_cur = rsv_scene_properties.get('workspace')
        step_cur = cur_rsv_task.get('step')
        if workspace_cur in {
            rsv_scene_properties.get('workspaces.source'),
            rsv_scene_properties.get('workspaces.user')
        }:
            if step_cur in {'srf'}:
                RsvTaskOverrideUsdCreator(
                    cur_rsv_task
                ).create_all_source_geometry_uv_map_over()
                #
                rsv_unit_override = cur_rsv_task.get_rsv_unit(
                    keyword='asset-source-geometry-usd-uv_map-file'
                )
                file_paths_override = rsv_unit_override.get_result(
                    version='all'
                )
                for i_file_path_override in file_paths_override:
                    i_properties = rsv_unit_override.generate_properties_by_result(i_file_path_override)
                    i_version = i_properties.get('version')
                    dict_[i_version] = i_file_path_override
        elif workspace_cur in {
            rsv_scene_properties.get('workspaces.release')
        }:
            comp_register_usd_file_rsv_unit = cur_rsv_task.get_rsv_unit(
                keyword='asset-component-registry-usd-file'
            )
            register_usd_file_paths = comp_register_usd_file_rsv_unit.get_result(
                version='all'
            )
            for i_file_path in register_usd_file_paths:
                i_properties = comp_register_usd_file_rsv_unit.generate_properties_by_result(i_file_path)
                i_version = i_properties.get('version')
                dict_[i_version] = i_file_path
        elif workspace_cur in {
            rsv_scene_properties.get('workspaces.temporary')
        }:
            comp_register_usd_file_rsv_unit = cur_rsv_task.get_rsv_unit(
                keyword='asset-temporary-component-registry-usd-file'
            )
            register_usd_file_paths = comp_register_usd_file_rsv_unit.get_result(
                version='all'
            )
            for i_file_path in register_usd_file_paths:
                i_properties = comp_register_usd_file_rsv_unit.generate_properties_by_result(i_file_path)
                i_version = i_properties.get('version')
                dict_[i_version] = i_file_path
        return dict_

    @classmethod
    def _create_asset_usd_file(cls, rsv_asset, rsv_scene_properties):
        usd_file_path = cls._generate_asset_usd_file_path_as_new(
            rsv_asset,
            rsv_scene_properties
        )
        cls._create_asset_usd_file_fnc(
            usd_file_path, rsv_asset, rsv_scene_properties
        )
        return usd_file_path

    @classmethod
    def _create_asset_usd_file_fnc(cls, usd_file_path, rsv_asset, rsv_scene_properties):
        asset_set_dress_usd_file_path = cls._generate_asset_set_dress_usd_file_path_as_latest(rsv_asset)

        key = 'usda/asset-set-v003'

        t = bsc_resource.RscExtendJinja.get_template(
            key
        )

        c = bsc_resource.RscExtendJinja.get_configure(
            key
        )

        c.set('file', usd_file_path)
        c.set('asset.project', rsv_asset.get('project'))
        c.set('asset.role', rsv_asset.get('role'))
        c.set('asset.name', rsv_asset.get('asset'))
        #
        c.set('asset.set_file', asset_set_dress_usd_file_path)

        cls._update_asset_all_variants(
            c, rsv_asset, rsv_scene_properties
        )

        c.do_flatten()
        #
        new_raw = t.render(
            c.value
        )
        # print new_raw
        #
        bsc_storage.StgFileOpt(
            usd_file_path
        ).set_write(
            new_raw
        )
        return usd_file_path

    @classmethod
    def _create_asset_shot_usd_file(cls, rsv_asset, rsv_shot, rsv_scene_properties):
        import lxusd.core as usd_core

        shot_set_dress_usd_file_path = cls._generate_shot_set_dress_usd_file_path_as_latest(rsv_shot)
        if shot_set_dress_usd_file_path:
            asset_shot_set_usd_file_path = cls._generate_asset_shot_usd_file_path_as_new(
                rsv_asset, rsv_shot,
                rsv_scene_properties
            )
            start_frame, end_frame = usd_core.UsdStageOpt(shot_set_dress_usd_file_path).get_frame_range()
            shot_asset_main_dict = cls._get_shot_asset_dict(rsv_asset, rsv_shot)
            shot_asset_override_dict = cls._get_shot_asset_override_dict(rsv_asset, rsv_shot, rsv_scene_properties)

            key = 'usda/shot-asset-set-v002'

            t = bsc_resource.RscExtendJinja.get_template(
                key
            )

            c = bsc_resource.RscExtendJinja.get_configure(
                key
            )
            c.set('file', asset_shot_set_usd_file_path)
            c.set('asset.project', rsv_asset.get('project'))
            c.set('asset.role', rsv_asset.get('role'))
            c.set('asset.name', rsv_asset.get('asset'))

            c.set('shot.sequence', rsv_shot.get('sequence'))
            c.set('shot.name', rsv_shot.get('shot'))
            c.set('shot.start_frame', start_frame)
            c.set('shot.end_frame', end_frame)
            c.set('shot.set_file', shot_set_dress_usd_file_path)

            c.set('shot.shot_asset_main', shot_asset_main_dict)
            c.set('shot.shot_asset_override', shot_asset_override_dict)

            cls._update_asset_all_variants(
                c, rsv_asset, rsv_scene_properties
            )

            c.do_flatten()
            raw = t.render(
                c.value
            )

            bsc_storage.StgFileOpt(
                asset_shot_set_usd_file_path
            ).set_write(
                raw
            )
            return asset_shot_set_usd_file_path

    def get_rsv_asset_shots(self):
        return self._get_rsv_asset_shots(
            self._rsv_asset
        )


class RsvUsdAssetSet(object):
    @classmethod
    def generate_asset_variant_dict(cls, usd_file_path, mode='main'):
        resolver = rsv_core.RsvBase.generate_root()
        rsv_project = resolver.get_rsv_project_by_any_file_path(usd_file_path)
        if rsv_project is None:
            return {}
        #
        properties = None
        keywords = [
            'asset-source-asset-set-usd-file',
            'asset-asset-set-usd-file',
            'asset-temporary-asset-set-usd-file',
        ]
        for i_keyword in keywords:
            i_rsv_unit = rsv_project.get_rsv_unit(keyword=i_keyword)
            i_properties = i_rsv_unit.generate_properties_by_result(usd_file_path)
            if i_properties:
                properties = i_properties
                break

        if properties is None:
            return {}

        import lxusd.core as usd_core

        workspace_mapper = {v: k for k, v in properties.get('workspaces').items()}
        asset_step_mapper = {v: k for k, v in properties.get('asset_steps').items()}
        asset_task_query = properties.get('asset_tasks')
        asset_task_mapper = {v: k for k, v in asset_task_query.items()}

        workspace_cur = properties.get('workspace')
        workspace_key_cur = workspace_mapper[workspace_cur]
        step_cur = properties.get('step')
        step_key_cur = asset_step_mapper[step_cur]
        usd_stage_opt = usd_core.UsdStageOpt(usd_file_path)
        usd_prim_opt = usd_core.UsdPrimOpt(usd_stage_opt.get_obj('/master'))
        usd_variant_dict = usd_prim_opt.get_variant_dict()
        if not usd_variant_dict:
            return {}

        c = ctt_core.Dict()

        keys = [
            'model',
            'groom',
            'rig',
            'effect',
            'surface',
            'light'
        ]
        for i_key in keys:
            i_args_main = usd_variant_dict.get('{}_main'.format(i_key))
            if i_args_main is not None:
                i_default_main, i_values_main = i_args_main
                c.set(
                    'asset_version_main.{}.default'.format(i_key), i_default_main
                )
                c.set(
                    'asset_version_main.{}.values'.format(i_key), i_values_main
                )
                #
                i_asset_task = asset_task_query.get(i_key)
                i_args_release = usd_variant_dict.get(i_asset_task)
                # from set dressing
                if i_asset_task in usd_variant_dict:
                    i_default_release, i_values_release = i_args_release
                    # main default use "None" when step-key is current step-key and workspace-key is "source"
                    if (
                        step_key_cur == i_key
                        # and workspace_key_cur in {
                        #     resolver.WorkspaceKeys.Source, resolver.WorkspaceKeys.Temporary
                        # }
                        and mode == 'override'
                    ):
                        i_default_main = 'None'
                    # main default use register
                    else:
                        i_default_main = '{}-default'.format(i_default_release)
                        if i_default_release in i_values_main:
                            i_values_main[i_values_main.index(i_default_release)] = i_default_main
                    #
                    for i_value in i_values_release:
                        if i_value in i_values_main:
                            if i_value != 'None':
                                i_values_main[i_values_main.index(i_value)] = '{}-release'.format(i_value)
                    #
                    c.set(
                        'asset_version_main.{}.default'.format(i_key), i_default_main
                    )
            #
            i_override_args = usd_variant_dict.get('{}_override'.format(i_key))
            if i_override_args:
                i_default_override, i_values_override = i_override_args
                c.set(
                    'asset_version_override.{}.default'.format(i_key), i_default_override
                )
                c.set(
                    'asset_version_override.{}.values'.format(i_key), i_values_override
                )
                if (
                    step_key_cur == i_key
                    # and workspace_key_cur in {
                    #     resolver.WorkspaceKeys.Source, resolver.WorkspaceKeys.Temporary
                    # }
                    and mode == 'override'
                ):
                    i_default_override = i_values_override[-1]
                    c.set(
                        'asset_version_override.{}.default'.format(i_key), i_default_override
                    )
        #
        return c.get_value()

    @classmethod
    def generate_asset_components_variant_dict(cls, usd_file_path):
        import lxusd.core as usd_core

        postfix = '_component_main'

        c = ctt_core.Dict()

        usd_stage_opt = usd_core.UsdStageOpt(usd_file_path)
        usd_prim_opt = usd_core.UsdPrimOpt(usd_stage_opt.get_obj('/master'))
        usd_variant_dict = usd_prim_opt.get_variant_dict()
        if not usd_variant_dict:
            return {}

        for k, v in usd_variant_dict.items():
            if k.endswith(postfix):
                i_default_main, i_values_main = v
                i_key_src = k[:-len(postfix)]
                c.set('{}.default'.format(i_key_src), i_default_main)
                c.set('{}.values'.format(i_key_src), i_values_main)
                if i_key_src in usd_variant_dict:
                    i_default_release, i_values_release = usd_variant_dict[i_key_src]
                    for i_value in i_values_release:
                        if i_value in i_values_main:
                            if i_value != 'None':
                                if i_value == i_default_release:
                                    i_values_main[i_values_main.index(i_value)] = '{}-default'.format(i_value)
                                else:
                                    i_values_main[i_values_main.index(i_value)] = '{}-release'.format(i_value)

                    if i_values_release is not None:
                        c.set('{}.default'.format(i_key_src), '{}-default'.format(i_default_release))

        return c.get_value()


class RsvUsdShotSetCreator(object):
    def __init__(self, rsv_shot):
        self._rsv_shot = rsv_shot

    @classmethod
    def get_effect_component_paths(cls, usd_file_path):
        import lxusd.core as usd_core

        paths = usd_core.UsdStageOpt(
            usd_file_path
        ).find_obj_paths(
            '/assets/efx/effects/*'
        )
        if paths:
            paths = bsc_core.RawTextsOpt(paths).sort_by_number()
        return paths


class RsvTaskOverrideUsdCreator(bsc_fnc_abstracts.AbsFncOptionBase):
    OPTION = dict(
        var_names=['hi'],
        root='/master'
    )
    VAR_NAMES = ['hi']

    def __init__(self, rsv_task, option=None):
        super(RsvTaskOverrideUsdCreator, self).__init__(option)
        if rsv_task is None:
            raise RuntimeError()
        #
        self._rsv_task = rsv_task

        self._rsv_project = rsv_task.get_rsv_project()

        self._dcc_data = self._rsv_project.get_dcc_data(
            application='maya'
        )

        self._renderable_c = self._dcc_data.get_as_content('renderable')

        self._location_mapper = {
            bsc_core.PthNodeOpt(i).get_name(): i for i in self._renderable_c.get_all_leaf_values() if i
        }

    def create_element_geometry_uv_map_over_at(self, directory_path, var_name):
        import lxusd.fnc.objects as usd_fnc_objects

        #
        root = self.get('root')
        #
        file_path = '{}/geo/{}.usd'.format(directory_path, var_name)
        file_path_over = '{}/geo/{}.uv_map.usd'.format(directory_path, var_name)
        if bsc_storage.StgFileOpt(file_path).get_is_exists() is True:
            if bsc_storage.StgFileOpt(file_path_over).get_is_exists() is False:
                usd_fnc_objects.GeometryUvMapExporter(
                    file_path=file_path_over,
                    root=root,
                    option=dict(
                        file_0=file_path,
                        file_1=file_path
                    )
                ).set_run()
            return file_path_over

    def create_geometry_uv_map_at(self, file_path):
        key = 'uv_map'
        if bsc_storage.StgFileOpt(file_path).get_is_exists() is False:
            directory_path = bsc_storage.StgFileOpt(file_path).get_directory_path()
            elements = []
            for i_var in self.VAR_NAMES:
                i_location = self._location_mapper[i_var]
                i_file_path_over = self.create_element_geometry_uv_map_over_at(directory_path, i_var)
                if i_file_path_over:
                    elements.append(
                        dict(
                            name=i_var,
                            location=i_location,
                            file=i_file_path_over[len(directory_path)+1:],
                        )
                    )
            #
            if elements:
                i_c = bsc_resource.RscExtendJinja.get_configure('usda/geometry/all/{}'.format(key))
                i_t = bsc_resource.RscExtendJinja.get_template('usda/geometry/all/{}'.format(key))
                i_c.set('elements', elements)
                i_raw = i_t.render(**i_c.get_value())
                bsc_storage.StgFileOpt(
                    file_path
                ).set_write(i_raw)

    def create_all_source_geometry_uv_map_over(self):
        rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-source-cache-usd-dir'
        )
        directory_paths = rsv_unit.get_result(version='all')
        for i_directory_path in directory_paths:
            file_path = '{}/uv_map.usda'.format(i_directory_path)
            self.create_geometry_uv_map_at(file_path)


class RsvUsdHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    COLOR_SCHEME = [
        'object_color',
        'group_color',
        'asset_color',
        'shell_color',
        'uv_map_color'
    ]

    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvUsdHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def create_asset_shot_asset_component_usd(self):
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        asset_shot = self._hook_option_opt.get('shot')
        shot_asset = self._hook_option_opt.get('shot_asset')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword = 'asset-shot_asset-component-usd-dir'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword = 'asset-temporary-shot_asset-component-usd-dir'
        else:
            raise TypeError()
        #
        component_usd_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword
        )
        component_usd_directory_path = component_usd_directory_rsv_unit.get_result(
            version=version,
            variants_extend=dict(
                asset_shot=asset_shot,
                shot_asset=shot_asset,
            )
        )
        key = 'usda/set/shot-asset'
        c = bsc_resource.RscExtendJinja.get_configure(key)
        c.update_from(
            self._rsv_scene_properties.value
        )
        c.update_from(
            dict(
                asset_shot=asset_shot,
                shot_asset=shot_asset,
            )
        )
        c.do_flatten()

        usda_dict = c.get('usdas')
        #
        for k, v in usda_dict.items():
            t = bsc_resource.RscExtendJinja.get_template(
                '{}/{}'.format(key, k)
            )
            i_raw = t.render(
                **c.value
            )
            i_usda_file_path = u'{}/{}'.format(
                component_usd_directory_path, v
            )
            i_file = bsc_dcc_objects.StgFile(i_usda_file_path)
            if i_file.get_is_exists() is False:
                bsc_dcc_objects.StgFile(i_usda_file_path).set_write(
                    i_raw
                )

    def create_set_asset_shot_set_usd(self):
        pass

    def create_asset_user_property_usd(self):
        import lxusd.core as usd_core

        import lxusd.fnc.objects as usd_fnc_objects

        #
        rsv_scene_properties = self._rsv_scene_properties
        #
        asset = rsv_scene_properties.get('asset')
        step = rsv_scene_properties.get('step')
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        root = rsv_scene_properties.get('dcc.root')
        #
        if workspace == rsv_scene_properties.get('workspaces.source'):
            keyword_0 = 'asset-source-geometry-usd-var-file'
            keyword_1 = 'asset-source-geometry-user_property-usd-file'
        elif workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-geometry-usd-var-file'
            keyword_1 = 'asset-geometry-user_property-usd-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-geometry-usd-var-file'
            keyword_1 = 'asset-temporary-geometry-user_property-usd-file'
        else:
            raise TypeError()
        #
        var_names = ['hi', 'shape', 'hair']
        #
        s = usd_core.UsdStageOpt()
        geometry_usd_var_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        for i_var_name in var_names:
            i_geometry_usd_var_file_path = geometry_usd_var_file_rsv_unit.get_exists_result(
                version=version,
                variants_extend=dict(var=i_var_name)
            )
            if i_geometry_usd_var_file_path:
                s.append_sublayer(i_geometry_usd_var_file_path)
            else:
                bsc_log.Log.trace_method_warning(
                    'look property create',
                    'variant="{}" is not found'.format(i_var_name)
                )
        #
        geometry_user_property_usd_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        geometry_user_property_usd_file_path = geometry_user_property_usd_file_rsv_unit.get_result(
            version=version
        )
        usd_fnc_objects.GeometryLookPropertyExporter(
            option=dict(
                file=geometry_user_property_usd_file_path,
                location=root,
                #
                stage_src=s.usd_instance,
                #
                asset_name=asset,
                #
                color_seed=5,
                #
                with_object_color=True,
                with_group_color=True,
                with_asset_color=True,
                with_shell_color=True,
            )
        ).set_run()

    def create_set_asset_display_color_usd(self):
        import lxusd.core as usd_core

        import lxusd.fnc.objects as usd_fnc_exporter

        #
        rsv_scene_properties = self._rsv_scene_properties

        asset = rsv_scene_properties.get('asset')
        step = rsv_scene_properties.get('step')
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        root = rsv_scene_properties.get('dcc.root')
        #
        if workspace == rsv_scene_properties.get('workspaces.source'):
            keyword_0 = 'asset-source-geometry-usd-var-file'
            keyword_1 = 'asset-source-geometry-extra-usd-dir'
        elif workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-geometry-usd-var-file'
            keyword_1 = 'asset-geometry-extra-usd-dir'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-geometry-usd-var-file'
            keyword_1 = 'asset-temporary-geometry-extra-usd-dir'
        else:
            raise TypeError()
        #
        var_names = ['hi', 'shape', 'hair']
        #
        s = usd_core.UsdStageOpt()
        geometry_usd_var_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        for i_var_name in var_names:
            i_geometry_usd_var_file_path = geometry_usd_var_file_rsv_unit.get_exists_result(
                version=version,
                variants_extend=dict(var=i_var_name)
            )
            if i_geometry_usd_var_file_path:
                s.append_sublayer(i_geometry_usd_var_file_path)
            else:
                bsc_log.Log.trace_method_warning(
                    'geometry display-color create',
                    'file="{}" is not found'.format(i_geometry_usd_var_file_path)
                )
        #
        geometry_extra_usd_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        #
        geometry_extra_usd_directory_path = geometry_extra_usd_directory_rsv_unit.get_result(
            version=version
        )

        for i_color_scheme in self.COLOR_SCHEME:
            i_file_path = '{}/{}.usd'.format(
                geometry_extra_usd_directory_path,
                i_color_scheme
            )
            usd_fnc_exporter.GeometryDisplayColorExporter(
                option=dict(
                    file=i_file_path,
                    location=root,
                    #
                    stage_src=s.usd_instance,
                    #
                    asset_name=asset,
                    #
                    color_seed=5,
                    #
                    color_scheme=i_color_scheme
                )
            ).set_run()

    def create_set_asset_component_usd(self):
        import lxbasic.dcc.core as bsc_dcc_core

        import lxbasic.extra.methods as utl_etr_methods

        #
        rsv_scene_properties = self._rsv_scene_properties
        #
        framework_scheme = rsv_scene_properties.get('schemes.framework')
        #
        step = rsv_scene_properties.get('step')
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.source'):
            keyword = 'asset-source-component-usd-dir'
        elif workspace == rsv_scene_properties.get('workspaces.release'):
            keyword = 'asset-component-usd-dir'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword = 'asset-temporary-component-usd-dir'
        else:
            raise TypeError()
        #
        component_usd_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword
        )
        #
        component_usd_directory_path = component_usd_directory_rsv_unit.get_result(
            version=version
        )
        #
        step_mapper = dict(
            mod='usda/set/model',
            srf='usda/set/surface',
            rig='usda/set/rig',
            grm='usda/set/groom',
        )
        if step in step_mapper:
            key = step_mapper[step]
            #
            c = bsc_resource.RscExtendJinja.get_configure(key)
            #
            c.update_from(
                self._rsv_scene_properties.value
            )
            #
            c.do_flatten()
            #
            look_pass_names = self.get_asset_exists_look_pass_names()
            c.set(
                'look.passes', look_pass_names
            )
            #
            usda_dict = c.get('usdas')
            #
            for k, v in usda_dict.items():
                if isinstance(v, six.string_types):
                    i_file_base = v
                    i_replace = False
                elif isinstance(v, dict):
                    i_file_base = v['file']
                    i_replace = v['replace']
                else:
                    raise RuntimeError()

                t = bsc_resource.RscExtendJinja.get_template('{}/{}'.format(key, k))
                i_raw = t.render(
                    **c.value
                )
                i_usda_file_path = '{}/{}'.format(
                    component_usd_directory_path, i_file_base
                )
                i_file = bsc_dcc_objects.StgFile(i_usda_file_path)
                if i_file.get_is_exists() is False:
                    bsc_dcc_objects.StgFile(i_usda_file_path).set_write(
                        i_raw
                    )
                else:
                    if i_replace is True:
                        i_start_frame, i_end_frame = bsc_dcc_core.DotUsdaOpt(
                            i_usda_file_path
                        ).get_frame_range()
                        c.set('start_frame', i_start_frame)
                        c.set('end_frame', i_end_frame)
                        i_raw = t.render(
                            **c.value
                        )
                        bsc_dcc_objects.StgFile(i_usda_file_path).set_write(
                            i_raw
                        )
            #
            if workspace in [rsv_scene_properties.get('workspaces.release')]:
                bsc_log.Log.trace_method_result(
                    'register usd',
                    'framework scheme use "{}"'.format(framework_scheme)
                )
                m = utl_etr_methods.get_module(framework_scheme)
                register_file_path = '{}/registry.usda'.format(component_usd_directory_path)
                m.EtrUsd.registry_set(register_file_path)
