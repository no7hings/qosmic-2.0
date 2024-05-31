# coding:utf-8
import copy

import glob

import lxbasic.content as bsc_content

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.database as bsc_database


class ScpResourcesAddByQuixel(object):
    """
    import lxbasic.process as bsc_core

    import lxbasic.database as bsc_database
    scp = ScpResourcesAddByQuixel()
    scp.add_resource_by_json(
        '/l/temp/zeqi/lib/atlas/plant_ferns_pjvef2/pjvef2.json'
    )

    scp.add_resources_from(
        '/l/temp/zeqi/lib/atlas'
    )
    """
    TEXTURE_CATEGORY_GROUPS = [
        'surface',
        'atlas',
        'displacement',
        'imperfection'
    ]
    ASSET_CATEGORY_GROUPS = [
        '3d_asset',
        '3d_plant'
    ]
    #
    ALL_CATEGORY_GROUPS = TEXTURE_CATEGORY_GROUPS+ASSET_CATEGORY_GROUPS
    #
    TEXTURE_PATTERN = '{texture_key}_{texture_size_tag}K_{texture_type_tag}.{format}'
    TEXTURE_LOD_PATTERN = '{texture_key}_{texture_size_tag}K_{texture_type_tag}_LOD{lod_level}.{format}'
    #
    TEXTURE_EXTRA_KEYS = [
        'Atlas',
        'Billboard'
    ]
    #
    TEXTURE_EXTRA_PATTERN = TEXTURE_PATTERN
    TEXTURE_EXTRA_LOD_PATTERN = TEXTURE_LOD_PATTERN
    #
    GEOMETRY_LOD_PATTERN = '{geometry_key}_LOD{lod_level}.{format}'
    GEOMETRY_VAR_KEY = 'Var{var_index}'
    GEOMETRY_VAR_PATTERN = ''
    GEOMETRY_VAR_LOD_PATTERN = '{key_extra}_LOD{lod_level}.{format}'

    CATEGORY_GROUP_MAPPER = {
        '3d_asset': 'asset',
        '3d_plant': 'plant'
    }

    KEY = 'add to quixel'

    def __init__(self):
        self._resource_dict = dict()

    def add_resources_from(self, directory_path_src):
        json_files = bsc_storage.StgDirectoryOpt(
            directory_path_src
        ).get_all_file_paths(
            ext_includes=['.json']
        )

        self._resource_dict = dict()

        with bsc_log.LogProcessContext.create_as_bar(maximum=len(json_files), label='add resource') as l_p:
            for i_json_file_path in json_files:
                l_p.do_update()
                self.add_resource_by_any_json(i_json_file_path)

    @classmethod
    def _check_resource_exists(cls, file_path):
        quixel_json_file_opt = bsc_storage.StgFileOpt(file_path)
        json_content = bsc_content.Content(
            value=file_path
        )

        # break when category group is not found
        category_group = json_content.get('semanticTags.asset_type')
        if category_group is None:
            bsc_log.Log.trace_method_error(cls.KEY, 'file: {} is not available'.format(file_path))
            return None

        category_group = bsc_core.RawTextMtd.clear_up_to(category_group).strip().lower()

        resource_id = quixel_json_file_opt.name_base
        resource_key = bsc_core.RawTextMtd.clear_up_to(json_content.get('name').strip()).lower()

        resource_name = '{}_{}'.format(resource_key, resource_id)

        if category_group in cls.ALL_CATEGORY_GROUPS:
            if category_group in cls.CATEGORY_GROUP_MAPPER:
                category_group = cls.CATEGORY_GROUP_MAPPER[category_group]

            dtb_opt = bsc_database.DtbOptForResource.generate(category_group)
            resource_dtb_path = '/{}/{}'.format(category_group, resource_name)
            dtb_resource = dtb_opt.get_resource(resource_dtb_path)
            if dtb_resource:
                return True

        return False

    def add_resource_by_any_json(self, file_path):
        bsc_log.Log.trace_method_result(
            'add resource',
            'json="{}"'.format(file_path)
        )
        quixel_json_file_opt = bsc_storage.StgFileOpt(file_path)
        json_content = bsc_content.Content(
            value=file_path
        )
        directory_path_src = quixel_json_file_opt.directory_path

        # break when category group is not found
        category_group = json_content.get('semanticTags.asset_type')
        if category_group is None:
            return

        category_group = bsc_core.RawTextMtd.clear_up_to(category_group).strip().lower()

        resource_id = quixel_json_file_opt.name_base
        resource_key = bsc_core.RawTextMtd.clear_up_to(json_content.get('name').strip()).lower()

        resource_name = '{}_{}'.format(resource_key, resource_id)
        version_name = 'v0001'

        if category_group in self.ALL_CATEGORY_GROUPS:
            if category_group in self.CATEGORY_GROUP_MAPPER:
                category_group = self.CATEGORY_GROUP_MAPPER[category_group]
            dtb_opt = bsc_database.DtbOptForResource.generate(category_group)

            resource_dtb_path = '/{}/{}'.format(category_group, resource_name)
            version_dtb_path = '{}/{}'.format(resource_dtb_path, version_name)

            pattern_kwargs = dict(
                category_group=category_group,
                resource=resource_name,
                version=version_name
            )
            # resource
            resource_directory_path_tgt = self.stg_create_resource_directory_tgt_fnc(
                dtb_opt,
                pattern_kwargs
            )
            self.dtb_create_resource_fnc(
                dtb_opt,
                resource_dtb_path,
                version_dtb_path,
                resource_directory_path_tgt,
                json_content
            )
            # version
            version_stg_path_tgt = self.stg_create_version_directory_tgt_fnc(
                dtb_opt,
                pattern_kwargs
            )
            metadata_file_path_tgt = self.stg_create_metadata_tgt_fnc(
                dtb_opt,
                pattern_kwargs, quixel_json_file_opt
            )
            preview_file_path_tgt = self.stg_create_preview_tgt_fnc(
                dtb_opt,
                pattern_kwargs, directory_path_src
            )
            self.dtb_create_version_fnc(
                dtb_opt,
                resource_dtb_path, version_dtb_path,
                version_stg_path_tgt,
                metadata_file_path_tgt, preview_file_path_tgt,
            )
            self.dtb_create_storage_fnc(
                dtb_opt,
                pattern_kwargs,
                version_dtb_path,
                version_stg_path_tgt
            )
            # texture
            self.stg_and_dtb_add_textures_fnc(
                dtb_opt,
                pattern_kwargs,
                resource_dtb_path, version_dtb_path,
                directory_path_src
            )
            self.stg_and_dtb_add_textures_extra_fnc(
                dtb_opt,
                pattern_kwargs,
                resource_dtb_path, version_dtb_path,
                '{}/Textures'.format(directory_path_src)
            )
            # geometry
            self.stg_and_dtb_add_geometries_fnc(
                dtb_opt,
                pattern_kwargs,
                resource_dtb_path, version_dtb_path,
                directory_path_src
            )
            self.stg_and_dtb_add_geometries_var_fnc(
                dtb_opt,
                pattern_kwargs,
                resource_dtb_path, version_dtb_path,
                directory_path_src
            )
        else:
            bsc_log.Log.trace_method_warning(
                'resource add', 'category group: {} is not available'.format(category_group)
            )

    @classmethod
    def stg_create_resource_directory_tgt_fnc(cls, dtb_opt, pattern_kwargs):
        pattern_opt = dtb_opt.get_pattern_opt('resource-dir')
        directory_path = pattern_opt.update_variants_to(**pattern_kwargs).get_value()
        path_opt = bsc_storage.StgDirectoryOpt(directory_path)
        path_opt.set_create()
        return directory_path

    @classmethod
    def stg_create_version_directory_tgt_fnc(cls, dtb_opt, pattern_kwargs):
        pattern_opt = dtb_opt.get_pattern_opt('version-dir')
        directory_path = pattern_opt.update_variants_to(**pattern_kwargs).get_value()
        path_opt = bsc_storage.StgDirectoryOpt(directory_path)
        path_opt.set_create()
        return directory_path

    @classmethod
    def stg_create_metadata_tgt_fnc(cls, dtb_opt, pattern_kwargs, file_opt_src):
        pattern_opt = dtb_opt.get_pattern_opt('quixel-metadata-json-file')
        path = pattern_opt.update_variants_to(**pattern_kwargs).get_value()
        file_opt_src.copy_to_file(path)
        return path

    @classmethod
    def stg_create_preview_tgt_fnc(cls, dtb_opt, pattern_kwargs, directory_path_src):
        quixel_image_png_file_pattern_opt = dtb_opt.get_pattern_opt('quixel-image-png-file')
        quixel_image_png_file_path = quixel_image_png_file_pattern_opt.update_variants_to(**pattern_kwargs).get_value()
        image_preview_png_file_pattern_opt = dtb_opt.get_pattern_opt('image-preview-png-file')
        file_path = image_preview_png_file_pattern_opt.update_variants_to(**pattern_kwargs).get_value()
        file_path_glog_pattern_src = '{}/*_Preview.png'.format(directory_path_src)
        file_paths_src = glob.glob(file_path_glog_pattern_src)
        if file_paths_src:
            file_path_src = file_paths_src[0]
            file_opt_src = bsc_storage.StgFileOpt(file_path_src)
            file_opt_src.copy_to_file(quixel_image_png_file_path)
            file_opt_src.copy_to_file(file_path)
        return file_path

    @classmethod
    def dtb_create_resource_fnc(
            cls, dtb_opt, resource_dtb_path, version_dtb_path, resource_directory_path_tgt, json_content
            ):
        is_create, dtb_resource = dtb_opt.create_resource(resource_dtb_path, gui_name=json_content.get('name'))
        if is_create is True:
            # add properties
            dtb_opt.create_property(
                resource_dtb_path, 'version', version_dtb_path, kind=dtb_opt.Kinds.Resource
            )
            dtb_opt.create_property(
                resource_dtb_path, 'location', resource_directory_path_tgt, kind=dtb_opt.Kinds.Resource
            )
            # types
            cls.dtb_assign_resource_types_fnc(
                dtb_opt,
                resource_dtb_path, json_content
            )
            # tags
            cls.dtb_assign_resource_tags_fnc(
                dtb_opt,
                resource_dtb_path, json_content
            )

    @classmethod
    def dtb_assign_resource_types_fnc(cls, dtb_opt, resource_dtb_path, json_content):
        c_c = json_content.get_as_content('assetCategories')
        keys = c_c.get_all_leaf_keys()
        c = 4
        for i_key in keys:
            i_keys = i_key.split('.')
            i_key_args = i_keys[1:]
            i_c = len(i_key_args)
            if i_c < 3:
                i_key_args += ['other']*(c-i_c-1)
            elif i_c > 3:
                i_key_args = i_key_args[:2]+['_'.join(i_key_args[2:])]
            #
            i_key_args = [bsc_core.RawTextMtd.clear_up_to(i).lower() for i in i_key_args]
            #
            i_type_path = '/'+'/'.join(i_key_args)

            i_dtb_type = dtb_opt.get_type_force(i_type_path)
            if i_dtb_type is not None:
                # resource types
                dtb_opt.create_type_assign(
                    resource_dtb_path, i_type_path, kind=dtb_opt.Kinds.ResourceType
                )
            else:
                bsc_log.Log.trace_method_warning(
                    'add resource', 'type="{}" is not register in database'.format(i_type_path)
                )

    @classmethod
    def dtb_assign_resource_tags_fnc(cls, dtb_opt, resource_dtb_path, json_content):
        # add semantic tags
        semantic_tag_groups = dtb_opt.get_entities(
            entity_type=dtb_opt.EntityTypes.TagGroup,
            filters=[
                ('kind', 'is', dtb_opt.Kinds.ResourceSemanticTagGroup)
            ]
        )
        for i in semantic_tag_groups:
            j_tag_group_name = i.name
            j_ = json_content.get('semanticTags.{}'.format(j_tag_group_name)) or ['other']
            if j_:
                if isinstance(j_, list):
                    j_tags = map(lambda x: bsc_core.RawTextMtd.clear_up_to(x.strip()).lower(), j_)
                    for k_tag in j_tags:
                        if k_tag:
                            if j_tag_group_name in {'color', 'environment', 'state'}:
                                k_kind = dtb_opt.Kinds.ResourcePrimarySemanticTag
                            else:
                                k_kind = dtb_opt.Kinds.ResourceSecondarySemanticTag
                            #
                            k_tag_path = '/{}/{}'.format(j_tag_group_name, k_tag)
                            dtb_opt.create_tag_assign(
                                resource_dtb_path, k_tag_path, kind=k_kind
                            )
                else:
                    pass
        # add other tags

    @classmethod
    def dtb_create_version_fnc(
            cls, dtb_opt, resource_dtb_path, version_dtb_path, version_stg_path_tgt, metadata_file_path_tgt,
            preview_file_path_tgt
            ):
        is_create, dtb_version = dtb_opt.create_version(
            version_dtb_path
        )
        if is_create is True:
            # add properties
            dtb_opt.create_property(
                version_dtb_path, 'resource', resource_dtb_path, kind=dtb_opt.Kinds.Version
            )
            dtb_opt.create_property(
                version_dtb_path, 'location', version_stg_path_tgt, kind=dtb_opt.Kinds.Version
            )
            dtb_opt.create_property(
                version_dtb_path, 'quixel_metadata_file', metadata_file_path_tgt, kind=dtb_opt.Kinds.Version
            )
            dtb_opt.create_property(
                version_dtb_path, 'image_preview_file', preview_file_path_tgt, kind=dtb_opt.Kinds.Version
            )

    @classmethod
    def dtb_create_storage_fnc(cls, dtb_opt, pattern_kwargs, version_dtb_path, version_stg_path):
        dtb_cfg_opt = dtb_opt.get_database_configure_opt()
        data = dtb_cfg_opt.get('storages')
        for i_k, i_v in data.items():
            i_kind = i_v['kind']
            i_keyword = i_v['keyword']
            i_pattern_opt = dtb_opt.get_pattern_opt(i_keyword)
            i_storage_stg_path = i_pattern_opt.update_variants_to(**pattern_kwargs).get_value()
            if i_storage_stg_path.startswith(version_stg_path):
                i_storage_dtb_path = '{}/{}'.format(version_dtb_path, i_k)
                i_is_create, i_dtb_storage = dtb_opt.create_storage(
                    i_storage_dtb_path, i_kind
                )
                if i_is_create is True:
                    # version property
                    dtb_opt.create_property(
                        version_dtb_path, i_k, i_storage_dtb_path, kind=dtb_opt.Kinds.Version
                    )
                    # storage property
                    dtb_opt.create_property(
                        i_storage_dtb_path, 'keyword', i_keyword, kind=i_kind
                    )
                    dtb_opt.create_property(
                        i_storage_dtb_path, 'location', i_storage_stg_path, kind=i_kind
                    )
                    dtb_opt.create_property(
                        i_storage_dtb_path, 'version', version_dtb_path, kind=i_kind
                    )
            else:
                raise RuntimeError()

    # texture
    @classmethod
    def stg_and_dtb_add_textures_fnc(
        cls, dtb_opt, pattern_kwargs, resource_dtb_path, version_dtb_path, directory_path_src
    ):
        quixel_directory_p_opt_tgt = dtb_opt.get_pattern_opt('quixel-texture-dir')
        #
        quixel_directory_path_tgt = quixel_directory_p_opt_tgt.update_variants_to(**pattern_kwargs).get_value()
        #
        file_paths = bsc_storage.StgDirectoryOpt(directory_path_src).get_file_paths(
            ext_includes=['.jpg', '.png', '.tga', '.exr']
            )
        for i_file_path_src in file_paths:
            # copy to quixel
            bsc_storage.StgFileOpt(i_file_path_src).copy_to_directory(
                quixel_directory_path_tgt
            )
            # lod texture
            i_lod_pattern_opt_src = bsc_core.PtnStgParseOpt(
                '{}/{}'.format(directory_path_src, cls.TEXTURE_LOD_PATTERN),
                variants=dict(texture_key='*', texture_size_tag='[0-9]')
            )
            if i_lod_pattern_opt_src.get_is_matched(i_file_path_src) is True:
                cls.stg_and_dtb_add_any_texture_fnc(
                    dtb_opt,
                    pattern_kwargs, i_lod_pattern_opt_src,
                    resource_dtb_path, version_dtb_path,
                    i_file_path_src,
                    'texture-original-src-lod-file',
                    is_lod=True
                )
                # copy lod 0 to default
                i_lod_variants_src = i_lod_pattern_opt_src.get_variants(i_file_path_src)
                if i_lod_variants_src['lod_level'] == '0':
                    cls.stg_and_dtb_add_any_texture_fnc(
                        dtb_opt,
                        pattern_kwargs, i_lod_pattern_opt_src,
                        resource_dtb_path, version_dtb_path,
                        i_file_path_src,
                        'texture-original-src-file',
                        is_lod=False
                    )
            # texture
            else:
                pattern_opt_src = bsc_core.PtnStgParseOpt(
                    '{}/{}'.format(directory_path_src, cls.TEXTURE_PATTERN),
                    variants=dict(texture_key='*', texture_size_tag='[0-9]')
                )
                if pattern_opt_src.get_is_matched(i_file_path_src) is True:
                    cls.stg_and_dtb_add_any_texture_fnc(
                        dtb_opt,
                        pattern_kwargs, pattern_opt_src,
                        resource_dtb_path, version_dtb_path,
                        i_file_path_src,
                        'texture-original-src-file',
                        is_lod=False
                    )

    @classmethod
    def stg_and_dtb_add_any_texture_fnc(
        cls, dtb_opt, pattern_kwargs, pattern_opt_src, resource_dtb_path, version_dtb_path, file_path_src, keyword,
        is_lod
    ):
        pattern_opt_tgt = dtb_opt.get_pattern_opt(keyword)
        pattern_kwargs_src = copy.copy(pattern_kwargs)
        variants_src = pattern_opt_src.get_variants(file_path_src)
        pattern_kwargs_src.update(variants_src)
        # fix texture tag
        texture_type_tag = pattern_kwargs_src['texture_type_tag']
        texture_type_tag = bsc_core.RawTextMtd.clear_up_to(texture_type_tag).strip().lower()
        pattern_kwargs_src['texture_type_tag'] = texture_type_tag
        #
        texture_stg_path = pattern_opt_tgt.update_variants_to(
            **pattern_kwargs_src
        ).get_value()
        #
        bsc_storage.StgFileOpt(file_path_src).copy_to_file(
            texture_stg_path
        )
        #
        if is_lod is False:
            cls.dtb_create_any_texture_fnc(
                dtb_opt,
                resource_dtb_path, version_dtb_path,
                texture_stg_path, texture_type_tag,
                keyword
            )

    @classmethod
    def dtb_create_any_texture_fnc(
        cls, dtb_opt, resource_dtb_path, version_dtb_path, file_stg_path, texture_type_tag, keyword
    ):
        key = 'texture_{}_file'.format(texture_type_tag)
        # texture
        file_dtb_path = '{}/{}'.format(version_dtb_path, key)
        dtb_opt.create_storage(
            file_dtb_path, kind=dtb_opt.Kinds.File
        )
        # version property
        dtb_opt.create_property(
            version_dtb_path, key, file_dtb_path, kind=dtb_opt.Kinds.Version
        )
        # storage property
        dtb_opt.create_property(
            file_dtb_path, 'keyword', keyword, kind=dtb_opt.Kinds.File
        )
        dtb_opt.create_property(
            file_dtb_path, 'location', file_stg_path, kind=dtb_opt.Kinds.File
        )
        dtb_opt.create_property(
            file_dtb_path, 'version', version_dtb_path, kind=dtb_opt.Kinds.File
        )
        # texture type tag
        texture_type_tag_dtb_path = '/texture/{}'.format(texture_type_tag)
        dtb_opt.create_tag_assign(
            resource_dtb_path, texture_type_tag_dtb_path, kind=dtb_opt.Kinds.ResourceFileTag
        )
        # texture size tag
        texture_size = bsc_storage.ImgOiioOpt(file_stg_path).get_size()
        texture_size_tag = '{}x{}'.format(*texture_size)
        texture_size_tag_dtb_path = '/resolution/{}'.format(texture_size_tag)
        dtb_opt.create_tag_assign(
            resource_dtb_path, texture_size_tag_dtb_path, kind=dtb_opt.Kinds.ResourcePropertyTag
        )
        #
        bsc_log.Log.trace_method_result(
            'database register',
            'entity="{}"'.format(file_dtb_path)
        )

    # texture extra
    @classmethod
    def stg_and_dtb_add_textures_extra_fnc(
        cls, dtb_opt, pattern_kwargs, resource_dtb_path, version_dtb_path, directory_path_src
    ):
        quixel_directory_p_opt_tgt = dtb_opt.get_pattern_opt('quixel-texture-dir')
        #
        quixel_directory_path_tgt = quixel_directory_p_opt_tgt.update_variants_to(**pattern_kwargs).get_value()
        for i_index, i_key_extra in enumerate(cls.TEXTURE_EXTRA_KEYS):
            i_directory_path_extra = '{}/{}'.format(directory_path_src, i_key_extra)
            if bsc_storage.StgDirectoryOpt(i_directory_path_extra).get_is_exists() is True:
                bsc_storage.StgDirectoryOpt(i_directory_path_extra).copy_to_directory(
                    '{}/{}'.format(quixel_directory_path_tgt, i_key_extra)
                )
                i_file_paths_src = bsc_storage.StgDirectoryOpt(i_directory_path_extra).get_file_paths()
                if i_file_paths_src:
                    i_pattern_opt_extra_src = bsc_core.PtnStgParseOpt(
                        '{}/{}'.format(i_directory_path_extra, cls.TEXTURE_EXTRA_PATTERN),
                        variants=dict(texture_key='*', texture_size_tag='[0-9]')
                    )
                    for j_file_path_src in i_file_paths_src:
                        if i_pattern_opt_extra_src.get_is_matched(j_file_path_src) is True:
                            if i_index == 0:
                                cls.stg_and_dtb_add_any_texture_fnc(
                                    dtb_opt,
                                    pattern_kwargs, i_pattern_opt_extra_src,
                                    resource_dtb_path, version_dtb_path,
                                    j_file_path_src,
                                    'texture-original-src-file',
                                    is_lod=False
                                )
                            else:
                                cls.stg_and_dtb_add_any_texture_extra_fnc(
                                    dtb_opt,
                                    pattern_kwargs, i_pattern_opt_extra_src,
                                    resource_dtb_path, version_dtb_path,
                                    j_file_path_src,
                                    i_key_extra, 'texture-original-extra-src-file'
                                )

    @classmethod
    def stg_and_dtb_add_any_texture_extra_fnc(
        cls, dtb_opt, pattern_kwargs, pattern_opt_src, resource_dtb_path, version_dtb_path, file_path_src,
        key_extra, keyword
    ):
        key_extra = key_extra.lower()
        #
        pattern_opt_tgt = dtb_opt.get_pattern_opt(keyword)
        pattern_kwargs_src = copy.copy(pattern_kwargs)
        variants_src = pattern_opt_src.get_variants(file_path_src)
        pattern_kwargs_src.update(variants_src)
        # fix texture tag
        texture_type_tag = pattern_kwargs_src['texture_type_tag']
        texture_type_tag = bsc_core.RawTextMtd.clear_up_to(texture_type_tag).strip().lower()
        pattern_kwargs_src['texture_type_tag'] = texture_type_tag
        # over texture key
        pattern_kwargs_src['key_extra'] = key_extra
        #
        file_stg_path = pattern_opt_tgt.update_variants_to(
            **pattern_kwargs_src
        ).get_value()
        #
        bsc_storage.StgFileOpt(file_path_src).copy_to_file(
            file_stg_path
        )
        cls.dtb_create_any_texture_extra_fnc(
            dtb_opt,
            resource_dtb_path, version_dtb_path,
            texture_type_tag, file_stg_path,
            key_extra, keyword
        )

    @classmethod
    def dtb_create_any_texture_extra_fnc(
        cls, dtb_opt, resource_dtb_path, version_dtb_path, texture_type_tag, file_stg_path, key_extra, keyword
    ):
        key = '{}/texture_{}_file'.format(key_extra, texture_type_tag)
        # file
        file_dtb_path = '{}/{}'.format(version_dtb_path, key)
        dtb_opt.create_storage(
            file_dtb_path, kind=dtb_opt.Kinds.File
        )
        # version property
        dtb_opt.create_property(
            version_dtb_path, key, file_dtb_path, kind=dtb_opt.Kinds.Version
        )
        # storage property
        dtb_opt.create_property(
            file_dtb_path, 'keyword', keyword, kind=dtb_opt.Kinds.File
        )
        dtb_opt.create_property(
            file_dtb_path, 'location', file_stg_path, kind=dtb_opt.Kinds.File
        )
        dtb_opt.create_property(
            file_dtb_path, 'version', version_dtb_path, kind=dtb_opt.Kinds.File
        )
        # texture type tag
        texture_type_tag_dtb_path = '/texture/{}'.format(texture_type_tag)
        dtb_opt.create_tag_assign(
            resource_dtb_path, texture_type_tag_dtb_path, kind=dtb_opt.Kinds.ResourceFileTag
        )
        # texture size tag
        texture_size = bsc_storage.ImgOiioOpt(file_stg_path).get_size()
        texture_size_tag = '{}x{}'.format(*texture_size)
        texture_size_tag_dtb_path = '/resolution/{}'.format(texture_size_tag)
        dtb_opt.create_tag_assign(
            resource_dtb_path, texture_size_tag_dtb_path, kind=dtb_opt.Kinds.ResourcePropertyTag
        )
        #
        bsc_log.Log.trace_method_result(
            'database register',
            'entity="{}"'.format(file_dtb_path)
        )

    # geometry
    @classmethod
    def stg_and_dtb_add_geometries_fnc(
        cls, dtb_opt, pattern_kwargs, resource_dtb_path, version_dtb_path, directory_path_src
    ):
        quixel_directory_p_opt_tgt = dtb_opt.get_pattern_opt('quixel-geometry-dir')
        #
        quixel_directory_path_tgt = quixel_directory_p_opt_tgt.update_variants_to(**pattern_kwargs).get_value()
        #
        file_paths = bsc_storage.StgDirectoryOpt(directory_path_src).get_file_paths(
            ext_includes=['.fbx', '.abc', '.obj', '.usd']
            )
        for i_file_path_src in file_paths:
            # copy to quixel
            bsc_storage.StgFileOpt(i_file_path_src).copy_to_directory(
                quixel_directory_path_tgt
            )
            #
            i_lod_pattern_opt_src = bsc_core.PtnStgParseOpt(
                '{}/{}'.format(directory_path_src, cls.GEOMETRY_LOD_PATTERN)
            )
            if i_lod_pattern_opt_src.get_is_matched(i_file_path_src) is True:
                i_file_opt = bsc_storage.StgFileOpt(i_file_path_src)
                i_file_format = i_file_opt.get_format()
                i_keyword = 'geometry-{}-lod-file'.format(i_file_format)
                cls.stg_and_dtb_add_any_geometry_fnc(
                    dtb_opt,
                    pattern_kwargs, i_lod_pattern_opt_src,
                    resource_dtb_path, version_dtb_path,
                    i_file_path_src,
                    i_file_format, i_keyword,
                    is_lod=True
                )
                #
                i_lod_variants_src = i_lod_pattern_opt_src.get_variants(i_file_path_src)
                if i_lod_variants_src['lod_level'] == '0':
                    i_keyword = 'geometry-{}-file'.format(i_file_format)
                    cls.stg_and_dtb_add_any_geometry_fnc(
                        dtb_opt,
                        pattern_kwargs, i_lod_pattern_opt_src,
                        resource_dtb_path, version_dtb_path,
                        i_file_path_src,
                        i_file_format, i_keyword,
                        is_lod=False,
                    )

    @classmethod
    def stg_and_dtb_add_any_geometry_fnc(
        cls, dtb_opt, pattern_kwargs, pattern_opt_src, resource_dtb_path, version_dtb_path, file_path_src, file_format,
        keyword, is_lod
    ):
        pattern_opt_tgt = dtb_opt.get_pattern_opt(keyword)
        pattern_kwargs_src = copy.copy(pattern_kwargs)
        variants_src = pattern_opt_src.get_variants(file_path_src)
        pattern_kwargs_src.update(variants_src)
        #
        file_stg_path = pattern_opt_tgt.update_variants_to(
            **pattern_kwargs_src
        ).get_value()
        #
        bsc_storage.StgFileOpt(file_path_src).copy_to_file(
            file_stg_path
        )
        if is_lod is False:
            cls.dtb_create_any_geometry_fnc(
                dtb_opt,
                resource_dtb_path, version_dtb_path,
                file_stg_path,
                file_format, keyword
            )

    @classmethod
    def dtb_create_any_geometry_fnc(cls, dtb_opt, resource_dtb_path, version_dtb_path, file_stg_path, file_format, keyword):
        key = 'geometry_{}_file'.format(file_format)
        # file
        file_dtb_path = '{}/{}'.format(version_dtb_path, key)
        dtb_opt.create_storage(
            file_dtb_path, kind=dtb_opt.Kinds.File
        )
        # version property
        dtb_opt.create_property(
            version_dtb_path, key, file_dtb_path, kind=dtb_opt.Kinds.Version
        )
        # storage property
        dtb_opt.create_property(
            file_dtb_path, 'keyword', keyword, kind=dtb_opt.Kinds.File
        )
        dtb_opt.create_property(
            file_dtb_path, 'location', file_stg_path, kind=dtb_opt.Kinds.File
        )
        dtb_opt.create_property(
            file_dtb_path, 'version', version_dtb_path, kind=dtb_opt.Kinds.File
        )
        # file format
        texture_type_tag_dtb_path = '/geometry/{}'.format(file_format)
        dtb_opt.create_tag_assign(
            resource_dtb_path, texture_type_tag_dtb_path, kind=dtb_opt.Kinds.ResourceFileTag
        )
        #
        bsc_log.Log.trace_method_result(
            'database register',
            'entity="{}"'.format(file_dtb_path)
        )

    # geometry variable
    @classmethod
    def stg_and_dtb_add_geometries_var_fnc(
            cls, dtb_opt, pattern_kwargs, resource_dtb_path, version_dtb_path, directory_path_src
            ):
        quixel_directory_p_opt_tgt = dtb_opt.get_pattern_opt('quixel-geometry-dir')
        #
        quixel_directory_path_tgt = quixel_directory_p_opt_tgt.update_variants_to(**pattern_kwargs).get_value()
        for i_var_index in range(20):
            i_var_index = str(i_var_index)
            i_key_extra = cls.GEOMETRY_VAR_KEY.format(
                **dict(var_index=i_var_index)
            )
            i_directory_path_extra = '{}/{}'.format(directory_path_src, i_key_extra)
            if bsc_storage.StgDirectoryOpt(i_directory_path_extra).get_is_exists() is True:
                bsc_storage.StgDirectoryOpt(i_directory_path_extra).copy_to_directory(
                    '{}/{}'.format(quixel_directory_path_tgt, i_key_extra)
                )
                i_file_paths_src = bsc_storage.StgDirectoryOpt(i_directory_path_extra).get_file_paths()
                if i_file_paths_src:
                    i_var_pattern_opt_extra_src = bsc_core.PtnStgParseOpt(
                        '{}/{}'.format(i_directory_path_extra, cls.GEOMETRY_VAR_LOD_PATTERN)
                    )
                    for j_file_path_src in i_file_paths_src:
                        j_file_opt = bsc_storage.StgFileOpt(j_file_path_src)
                        if i_var_pattern_opt_extra_src.get_is_matched(j_file_path_src):
                            j_file_format = j_file_opt.get_format()
                            j_keyword = 'geometry-{}-var-lod-file'.format(j_file_format)
                            cls.stg_and_dtb_add_any_geometry_var_fnc(
                                dtb_opt,
                                pattern_kwargs, i_var_pattern_opt_extra_src,
                                resource_dtb_path, version_dtb_path,
                                j_file_path_src,
                                i_var_index,
                                j_file_format, j_keyword,
                                is_var=True, is_lod=True
                            )
                            j_lod_variants_src = i_var_pattern_opt_extra_src.get_variants(j_file_path_src)
                            #
                            if j_lod_variants_src['lod_level'] == '0':
                                j_keyword = 'geometry-{}-var-file'.format(j_file_format)
                                cls.stg_and_dtb_add_any_geometry_var_fnc(
                                    dtb_opt,
                                    pattern_kwargs, i_var_pattern_opt_extra_src,
                                    resource_dtb_path, version_dtb_path,
                                    j_file_path_src,
                                    i_var_index,
                                    j_file_format, j_keyword,
                                    is_var=True, is_lod=False
                                )
                            # default
                            if j_lod_variants_src['lod_level'] == '0' and i_var_index == '1':
                                j_keyword = 'geometry-{}-file'.format(j_file_format)
                                #
                                cls.stg_and_dtb_add_any_geometry_var_fnc(
                                    dtb_opt,
                                    pattern_kwargs, i_var_pattern_opt_extra_src,
                                    resource_dtb_path, version_dtb_path,
                                    j_file_path_src,
                                    i_var_index,
                                    j_file_format, j_keyword,
                                    is_var=False, is_lod=False
                                )

    @classmethod
    def stg_and_dtb_add_any_geometry_var_fnc(
        cls, dtb_opt, pattern_kwargs, pattern_opt_src, resource_dtb_path, version_dtb_path, file_path_src,
        var_index, file_format, keyword, is_var, is_lod
    ):
        pattern_opt_tgt = dtb_opt.get_pattern_opt(keyword)
        #
        pattern_kwargs_src = copy.copy(pattern_kwargs)
        variants_src = pattern_opt_src.get_variants(file_path_src)
        pattern_kwargs_src.update(variants_src)
        # over texture key
        pattern_kwargs_src['var_index'] = var_index
        #
        file_stg_path = pattern_opt_tgt.update_variants_to(
            **pattern_kwargs_src
        ).get_value()

        bsc_storage.StgFileOpt(file_path_src).copy_to_file(
            file_stg_path
        )
        if is_var is False and is_lod is False:
            cls.dtb_create_any_geometry_fnc(
                dtb_opt,
                resource_dtb_path, version_dtb_path,
                file_stg_path,
                file_format, keyword
            )


if __name__ == '__main__':
    scp = ScpResourcesAddByQuixel()
    # scp.add_resource_by_any_json(
    #     '/l/temp/zeqi/lib/3d/rock_granite_ohlx3/ohlx3.json'
    # )
    # scp.add_resource_by_any_json(
    #     '/l/temp/zeqi/lib/surface/rock_mossy_ulsnabyn/ulsnabyn.json'
    # )
    # scp.add_resource_by_any_json(
    #     '/l/temp/zeqi/lib/3d/3d_rock_udxlcb1fa/udxlcb1fa.json'
    # )
    # scp.add_resource_by_any_json(
    #     '/l/temp/zeqi/lib/3dplant/3dplant_ground cover_xdjmfeqqx/xdjmfeqqx.json'
    # )
    # scp.add_resource_by_any_json(
    #     '/l/temp/zeqi/lib/atlas/plant_ferns_pjvef2/pjvef2.json'
    # )
    # scp.add_resources_from(
    #     '/l/resource/srf/tex_lib/surfaces'
    # )
    # scp.add_resources_from(
    #     '/l/temp/zeqi/lib/surface'
    # )
    # scp.add_resources_from(
    #     '/l/temp/zeqi/lib/3d'
    # )
    scp.add_resources_from(
        '/l/temp/zeqi/lib/3dplant'
    )
    # scp.add_resources_from(
    #     '/l/temp/zeqi/lib/atlas'
    # )
