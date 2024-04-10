# coding:utf-8
import copy

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxresolver.core as rsv_core


class RsvAssetTextureOpt(object):
    def __init__(self, rsv_task):
        self._resolver = rsv_core.RsvBase.generate_root()

        self._rsv_task = rsv_task

        self._variant = None

        self._version = None

        self._work_texture_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-source-texture-dir'
        )

        self._work_texture_version_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-source-texture-version-dir'
        )
        self._work_texture_src_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-source-texture-src-dir'
        )
        self._work_texture_tx_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-source-texture-tx-dir'
        )

    def get_root_at(self, variant):
        return self._work_texture_directory_rsv_unit.get_result(
            version='latest',
            variants_extend=dict(variant=variant)
        )

    def get_all_directories_at(self, variant):
        return self._work_texture_version_directory_rsv_unit.get_result(
            version='all',
            variants_extend=dict(variant=variant)
        )

    def get_directory_path_at(self, variant, version):
        return self._work_texture_version_directory_rsv_unit.get_result(
            version=version,
            variants_extend=dict(variant=variant)
        )

    def get_src_directory_path_at(self, variant, version):
        return self._work_texture_src_directory_rsv_unit.get_result(
            version=version,
            variants_extend=dict(variant=variant)
        )

    def get_tx_directory_path_at(self, variant, version):
        return self._work_texture_tx_directory_rsv_unit.get_result(
            version=version,
            variants_extend=dict(variant=variant)
        )

    def get_all_variants(self):
        pass

    def set_version_create_at(self, variant, version):
        if version == 'new':
            version = self.get_new_version_at(variant)
        # base
        bsc_storage.StgPathPermissionMtd.create_directory(
            self.get_directory_path_at(variant, version)
        )
        # src
        bsc_storage.StgPathPermissionMtd.create_directory(
            self.get_src_directory_path_at(variant, version)
        )
        # tx
        bsc_storage.StgPathPermissionMtd.create_directory(
            self.get_tx_directory_path_at(variant, version)
        )
        #
        bsc_log.Log.trace_method_result(
            'version create',
            'variant="{}", version="{}"'.format(
                variant, version
            )
        )

    def lock_version_at(self, variant, version):
        directory_path = self.get_directory_path_at(variant, version)

        bsc_storage.StgPathPermissionMtd.lock(directory_path)

        bsc_log.Log.trace_method_result(
            'version lock',
            'variant="{}", version="{}"'.format(
                variant, version
            )
        )

    # todo: update this method
    @classmethod
    def lock_directory(cls, directory_path):
        pass
        # bsc_storage.StgSshOpt(
        #     directory_path
        # ).set_just_read_only_for(
        #     ['cg_group', 'coop_grp']
        # )

    def set_current_variant(self, variant):
        self._variant = variant

    def set_current_version(self, version):
        self._version = version

    def get_current_variant(self):
        return self._variant

    def get_current_version(self):
        return self._version

    def get_latest_version_at(self, variant):
        return self._work_texture_version_directory_rsv_unit.get_latest_version(
            variants_extend=dict(variant=variant)
        )

    def get_new_version_at(self, variant):
        return self._work_texture_version_directory_rsv_unit.get_new_version(
            variants_extend=dict(variant=variant)
        )

    def get_all_versions_at(self, variant):
        return self._work_texture_version_directory_rsv_unit.get_all_exists_versions(
            variants_extend=dict(variant=variant)
        )

    def get_all_locked_versions_at(self, variant):
        matches = self._work_texture_version_directory_rsv_unit.get_all_exists_matches(
            variants_extend=dict(variant=variant)
        )
        list_ = []
        for i in matches:
            i_result, i_variants = i
            if bsc_storage.StgPathMtd.get_is_writable(i_result) is False:
                list_.append(i_variants['version'])
        return list_

    def get_all_unlocked_versions_at(self, variant):
        matches = self._work_texture_version_directory_rsv_unit.get_all_exists_matches(
            variants_extend=dict(variant=variant)
        )
        list_ = []
        for i in matches:
            i_result, i_variants = i
            if bsc_storage.StgPathMtd.get_is_writable(i_result) is True:
                list_.append(i_variants['version'])
        return list_

    def get_all_directories(self, dcc_objs):
        rsv_project = self._rsv_task.get_rsv_project()

        directory_keyword = 'asset-source-texture-version-dir'

        file_keywords = [
            'asset-source-texture-src-dir',
            'asset-source-texture-tx-dir'
        ]

        directory_pattern = rsv_project.get_pattern(directory_keyword)

        check_pattern_opts = []
        for i_k in file_keywords:
            i_p = rsv_project.get_pattern(
                i_k
            )
            i_check_p = i_p+'/{extra}'
            i_check_p_opt = bsc_core.PtnParseOpt(
                i_check_p
            )
            i_check_p_opt.update_variants(**dict(root=rsv_project.get('root')))
            check_pattern_opts.append(i_check_p_opt)

        set_ = set()

        file_paths = set([i_v for i in dcc_objs for i_k, i_v in i.reference_raw.items()])
        for i_file_path in file_paths:
            for i_check_p_opt in check_pattern_opts:
                i_variants = i_check_p_opt.get_variants(i_file_path)
                if i_variants is not None and 'project' in i_variants:
                    i_directory_path = directory_pattern.format(**i_variants)
                    set_.add(i_directory_path)
                    break

        return list(set_)

    def set_all_directories_locked(self, dcc_objs):
        directory_paths = self.get_all_directories(
            dcc_objs
        )
        unlocked_directory_paths = [i for i in directory_paths if bsc_storage.StgPathMtd.get_is_writable(i) is True]
        if unlocked_directory_paths:
            with bsc_log.LogProcessContext.create_as_bar(
                    maximum=len(unlocked_directory_paths),
                    label='workspace texture lock'
            ) as g_p:
                for _i in unlocked_directory_paths:
                    self.lock_directory(_i)
                    g_p.do_update()

    def set_all_directories_locked_with_dialog(self, dcc_objs):
        pass

    def get_kwargs_by_directory_path(self, directory_path):
        for i_rsv_unit in [
            self._work_texture_src_directory_rsv_unit,
            self._work_texture_tx_directory_rsv_unit
        ]:
            i_properties = i_rsv_unit.generate_properties_by_result(directory_path)
            if i_properties:
                return i_properties.get_value()

    def get_search_directory_args(self, directory_path):
        kwargs = self.get_kwargs_by_directory_path(directory_path)
        if kwargs:
            kwargs_0, kwargs_1 = copy.copy(kwargs), copy.copy(kwargs)
            kwargs_0['keyword'], kwargs_1['keyword'] = 'asset-source-texture-src-dir', 'asset-source-texture-tx-dir'
            return self._resolver.get_result(**kwargs_0), self._resolver.get_result(**kwargs_1)


class RsvAssetBuildOpt(object):
    def __init__(self, rsv_resource):
        self._resolver = rsv_core.RsvBase.generate_root()

        self._rsv_resource = rsv_resource
        self._rsv_project = self._rsv_resource.get_rsv_project()
        # model
        self._model_rsv_task = rsv_resource.get_rsv_task(
            step=self._rsv_project.properties.get('asset_steps.model'),
            task=self._rsv_project.properties.get('asset_tasks.model')
        )

        self._model_act_rsv_task = rsv_resource.get_rsv_task(
            step=self._rsv_project.properties.get('asset_steps.model'),
            task=self._rsv_project.properties.get('asset_tasks.model_dynamic'),
        )
        # groom
        self._groom_rsv_task = rsv_resource.get_rsv_task(
            step=self._rsv_project.properties.get('asset_steps.groom'),
            task=self._rsv_project.properties.get('asset_tasks.groom')
        )
        # surface
        self._surface_rsv_task = rsv_resource.get_rsv_task(
            step=self._rsv_project.properties.get('asset_steps.surface'),
            task=self._rsv_project.properties.get('asset_tasks.surface')
        )
