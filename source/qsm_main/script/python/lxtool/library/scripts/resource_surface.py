# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.database as bsc_database


class TextureOpt(object):
    def __init__(self):
        pass


class ScpResourcesAddForSurface(object):
    def __init__(self):
        pass

    def add_texture_from(self, directory_path_src, type_dtb_path, texture_type_tag):
        type_opt = bsc_core.PthNodeOpt(type_dtb_path)
        cs = type_opt.get_components()
        category_group_opt = cs[-2]
        category_group = category_group_opt.get_name()
        dtb_opt = bsc_database.DtbOptForResource.generate(category_group)
        #
        dtb_opt.get_type_force(type_dtb_path)
        ext_includes = ['.png', '.jpg', '.tga', '.exr']
        file_name_pattern = '{name} seamless 0{number}-png'
        resource_name_pattern = '{name}_vol3_{number.zfill(3)}'

        all_file_path = bsc_storage.StgDirectoryOpt(directory_path_src).get_all_file_paths(
            ext_includes=ext_includes
        )
        with bsc_log.LogProcessContext.create_as_bar(maximum=len(all_file_path), label='add resource') as l_p:
            for i_file_path in all_file_path:
                l_p.do_update()
                self.add_texture(
                    dtb_opt, i_file_path, category_group, [type_dtb_path], file_name_pattern, resource_name_pattern,
                    texture_type_tag
                )

    @classmethod
    def add_texture(
            cls, dtb_opt, file_path, category_group, type_dtb_paths, file_name_pattern, resource_name_pattern,
            texture_type_tag
            ):
        file_opt = bsc_storage.StgFileOpt(file_path)
        file_name_p_opt = bsc_core.PtnParseOpt(
            file_name_pattern
        )
        var = file_name_p_opt.get_variants(file_opt.get_name_base())
        if var:
            resource_name_p_opt = bsc_core.PtnParseOpt(resource_name_pattern)
            resource_name_p_opt.update_variants(**var)
            if not resource_name_p_opt.get_keys():
                resource_name = resource_name_p_opt.get_value()
                resource_name = bsc_core.RawTextMtd.clear_up_to(resource_name).strip().lower()
                resource_dtb_path = '/{}/{}'.format(category_group, resource_name)
                version_name = 'v0001'
                version_dtb_path = '{}/{}'.format(resource_dtb_path, version_name)
                pattern_kwargs = dict(
                    category_group=category_group,
                    resource=resource_name,
                    version=version_name,
                    texture_type_tag=texture_type_tag,
                    format=file_opt.get_format()
                )
                cls.create_resource_and_version(
                    dtb_opt, file_path, resource_dtb_path, version_dtb_path, texture_type_tag, pattern_kwargs
                )
                cls.dtb_assign_resource_types_fnc(
                    dtb_opt, resource_dtb_path, type_dtb_paths
                )

    @classmethod
    def dtb_create_type(cls, dtb_opt, type_dtb_path):
        return dtb_opt.get_type_force(type_dtb_path)

    @classmethod
    def create_resource_and_version(
            cls, dtb_opt, file_path, resource_dtb_path, version_dtb_path, texture_type_tag, pattern_kwargs
            ):
        is_create, dtb_resource = dtb_opt.create_resource(resource_dtb_path)
        if is_create is True:
            resource_stg_path = cls.stg_create_resource(dtb_opt, pattern_kwargs)
            # add properties
            dtb_opt.create_property(
                resource_dtb_path, 'version', version_dtb_path, kind=dtb_opt.Kinds.Resource
            )
            dtb_opt.create_property(
                resource_dtb_path, 'location', resource_stg_path, kind=dtb_opt.Kinds.Resource
            )
        #
        is_create, dtb_version = dtb_opt.create_version(version_dtb_path)
        if is_create is True:
            version_stg_path = cls.stg_create_version(dtb_opt, pattern_kwargs)
            # add properties
            dtb_opt.create_property(
                version_dtb_path, 'resource', resource_dtb_path, kind=dtb_opt.Kinds.Version
            )
            dtb_opt.create_property(
                version_dtb_path, 'location', version_stg_path, kind=dtb_opt.Kinds.Version
            )
            cls.dtb_create_storage_fnc(dtb_opt, version_dtb_path, version_stg_path, pattern_kwargs)

            preview_file_path = cls.stg_create_preview(dtb_opt, file_path, pattern_kwargs)
            dtb_opt.create_property(
                version_dtb_path, 'image_preview_file', preview_file_path, kind=dtb_opt.Kinds.Version
            )

            keyword = 'texture-original-src-file'
            file_stg_path = cls.stg_copy_texture(dtb_opt, file_path, pattern_kwargs, keyword)
            key = 'texture_{}_file'.format(texture_type_tag)
            file_dtb_path = '{}/{}'.format(version_dtb_path, key)
            dtb_opt.create_storage(
                file_dtb_path, kind=dtb_opt.Kinds.File
            )
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

    @classmethod
    def dtb_assign_resource_types_fnc(cls, dtb_opt, resource_dtb_path, type_dtb_paths):
        for i_type_dtb_path in type_dtb_paths:
            dtb_opt.create_type_assign(
                resource_dtb_path, i_type_dtb_path, kind=dtb_opt.Kinds.ResourceType
            )

    @classmethod
    def stg_create_resource(cls, dtb_opt, pattern_kwargs):
        p_opt = dtb_opt.get_pattern_opt('resource-dir')
        stg_path = p_opt.update_variants_to(**pattern_kwargs).get_value()
        path_opt = bsc_storage.StgDirectoryOpt(stg_path)
        path_opt.set_create()
        return stg_path

    @classmethod
    def stg_create_version(cls, dtb_opt, pattern_kwargs):
        p_opt = dtb_opt.get_pattern_opt('version-dir')
        stg_path = p_opt.update_variants_to(**pattern_kwargs).get_value()
        path_opt = bsc_storage.StgDirectoryOpt(stg_path)
        path_opt.set_create()
        return stg_path

    @classmethod
    def stg_copy_texture(cls, dtb_opt, file_path, pattern_kwargs, keyword):
        p_opt = dtb_opt.get_pattern_opt(keyword)
        stg_path = p_opt.update_variants_to(**pattern_kwargs).get_value()
        bsc_storage.StgFileOpt(file_path).copy_to_file(
            stg_path
        )
        return stg_path

    @classmethod
    def stg_create_preview(cls, dtb_opt, file_path, pattern_kwargs):
        preview_file_path_ = bsc_storage.ImgOiioOptForThumbnail(file_path).generate_thumbnail(width=256, ext='.png')
        preview_file_p_opt = dtb_opt.get_pattern_opt('image-preview-png-file')
        preview_file_path = preview_file_p_opt.update_variants_to(**pattern_kwargs).get_value()
        bsc_storage.StgFileOpt(preview_file_path_).copy_to_file(
            preview_file_path
        )
        return preview_file_path

    @classmethod
    def dtb_create_storage_fnc(cls, dtb_opt, version_dtb_path, version_stg_path, pattern_kwargs):
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


if __name__ == '__main__':
    ScpResourcesAddForSurface().add_texture_from(
        '/l/temp/zeqi/tex/82 Stain Imperfection seamless pack 2-vol3/82 Stain Imperfection seamless pack 2-vol3',
        type_dtb_path='/texture/imperfection/stain',
        texture_type_tag='roughness'
    )
    # print bsc_core.ImgOiioOptForThumbnail('/l/temp/zeqi/tex/82 Stain Imperfection seamless pack 1-vol3/82 Stain Imperfection seamless pack 1-vol3/Stain Imperfection seamless 01-png.png').generate_thumbnail(ext='.png')
