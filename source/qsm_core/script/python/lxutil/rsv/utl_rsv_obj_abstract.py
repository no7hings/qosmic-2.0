# coding:utf-8
import lxresolver.core as rsv_core


class AbsRsvObjHookOpt(object):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        self._rsv_scene_properties = rsv_scene_properties
        self._resolver = rsv_core.RsvBase.generate_root()
        self._rsv_task = self._resolver.get_rsv_task(
            **self._rsv_scene_properties.value
        )
        self._hook_option_opt = hook_option_opt

    @classmethod
    def generate_resolver(cls):
        return rsv_core.RsvBase.generate_root()

    def get_asset_katana_render_file(self):
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-katana-scene-file'
            keyword_1 = 'asset-katana-scene-src-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-katana-scene-file'
            keyword_1 = 'asset-temporary-katana-scene-src-file'
        else:
            raise TypeError()

        render_use_scene = self._hook_option_opt.get_as_boolean('render_use_scene')
        if render_use_scene is True:
            scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_0
            )
            scene_file_path = scene_file_rsv_unit.get_result(version=version)
            return scene_file_path
        else:
            render_us_scene_src = self._hook_option_opt.get_as_boolean('render_us_scene_src')
            if render_us_scene_src is True:
                scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
                    keyword=keyword_1
                )
                scene_src_file_path = scene_src_file_rsv_unit.get_result(version=version)
                return scene_src_file_path

    def get_asset_katana_render_output_directory(self):
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-katana-render-output-dir'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-katana-render-output-dir'
        else:
            raise TypeError()

        render_output_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        rsv_render_output_directory_path = render_output_directory_rsv_unit.get_result(
            version=version
        )
        return rsv_render_output_directory_path

    def get_asset_katana_video_all_mov_file(self):
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-katana-render-video-all-mov-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-katana-render-video-all-mov-file'
        else:
            raise TypeError()

        render_output_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        rsv_render_output_directory_path = render_output_directory_rsv_unit.get_result(
            version=version, variants_extend=dict(variant='main')
        )
        return rsv_render_output_directory_path

    def get_exists_asset_review_mov_file(self):
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword = 'asset-review-mov-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword = 'asset-temporary-review-mov-file'
        else:
            raise TypeError()
        #
        review_mov_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword
        )
        return review_mov_file_rsv_unit.get_exists_result(
            version=version
        )

    @classmethod
    def get_dcc_args(cls, any_scene_file_path, application):
        resolver = rsv_core.RsvBase.generate_root()
        rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(
            any_scene_file_path
        )
        if rsv_scene_properties:
            if rsv_scene_properties.get('application') == application:
                return rsv_scene_properties
            #
            workspace = rsv_scene_properties.get('workspace')
            version = rsv_scene_properties.get('version')
            #
            if workspace == rsv_scene_properties.get('workspaces.release'):
                keyword = 'asset-{application}-scene-src-file'
            elif workspace == rsv_scene_properties.get('workspaces.temporary'):
                keyword = 'asset-temporary-{application}-scene-src-file'
            else:
                raise TypeError()

            keyword = keyword.format(**dict(application=application))

            rsv_task = resolver.get_rsv_task(
                **rsv_scene_properties.value
            )

            scene_src_file_rsv_unit = rsv_task.get_rsv_unit(
                keyword=keyword
            )
            scene_src_file_path = scene_src_file_rsv_unit.get_exists_result(
                version=version
            )
            if scene_src_file_path is not None:
                return resolver.get_rsv_scene_properties_by_any_scene_file_path(
                    scene_src_file_path
                )

    def get_asset_exists_look_pass_names(self):
        import os

        import fnmatch

        import lxbasic.storage as bsc_storage

        rsv_scene_properties = self._rsv_scene_properties
        #
        step = rsv_scene_properties.get('step')
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.source'):
            return ['default']
        elif workspace == rsv_scene_properties.get('workspaces.release'):
            keyword = 'asset-look-klf-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword = 'asset-temporary-look-klf-file'
        else:
            raise TypeError()
        #
        file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword
        )
        file_path = file_rsv_unit.get_exists_result(
            version=version
        )

        if file_path:
            element_names = bsc_storage.StgZipFileOpt(file_path).get_element_names()
            look_pass_names = [os.path.splitext(i)[0] for i in fnmatch.filter(element_names, '*.klf')]
            return look_pass_names
        return ['default']

    def get_asset_exists_geometry_variant_names(self):
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.source'):
            keyword = 'asset-source-geometry-usd-var-file'
        elif workspace == rsv_scene_properties.get('workspaces.release'):
            keyword = 'asset-geometry-usd-var-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword = 'asset-temporary-geometry-usd-var-file'
        else:
            raise TypeError()
        #
        var_names = ['hi', 'shape', 'hair']
        #
        geometry_usd_var_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword
        )
        list_ = []
        for i_var_name in var_names:
            i_geometry_usd_var_file_path = geometry_usd_var_file_rsv_unit.get_exists_result(
                version=version,
                variants_extend=dict(var=i_var_name)
            )
            if i_geometry_usd_var_file_path:
                list_.append(i_var_name)
        return list_

    def get_asset_model_act_frame_range(self):
        import lxbasic.dcc.core as bsc_dcc_core

        rsv_asset = self._rsv_task.get_rsv_resource()
        model_act_rsv_task = rsv_asset.get_rsv_task(
            step='mod',
            task='mod_dynamic'
        )
        if model_act_rsv_task is not None:
            keyword = 'asset-component-usd-file'
            cmp_usd_file_rsv_unit = model_act_rsv_task.get_rsv_unit(keyword=keyword)
            cmp_usd_file_path = cmp_usd_file_rsv_unit.get_exists_result(version='latest')
            if cmp_usd_file_path:
                return bsc_dcc_core.DotUsdaOpt(cmp_usd_file_path).get_frame_range()

    def get_asset_model_act_cmp_usd_file(self):
        rsv_asset = self._rsv_task.get_rsv_resource()
        model_act_rsv_task = rsv_asset.get_rsv_task(
            step='mod',
            task='mod_dynamic'
        )
        if model_act_rsv_task is not None:
            keyword = 'asset-component-usd-file'
            cmp_usd_file_rsv_unit = model_act_rsv_task.get_rsv_unit(keyword=keyword)
            return cmp_usd_file_rsv_unit.get_exists_result(version='latest')
