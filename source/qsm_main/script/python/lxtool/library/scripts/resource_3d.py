# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.database as bsc_database


class ScpResourcesAddFor3dPlant(object):
    NAME_REPLACE = [
        ('YeCao', 'wild_grass'),
        ('YeHua', 'wild_flower'),
        ('Cao', 'grass'),
        ('GuanMu', 'shrub'),
        ('JueLei', 'fern'),
        ('Shu', 'tree'),
    ]
    TYPE_DICT = {}

    def __init__(self):
        pass

    @classmethod
    def dtb_create_type(cls, dtb_opt, type_dtb_path):
        return dtb_opt.get_type_force(type_dtb_path)

    @classmethod
    def dtb_assign_resource_types_fnc(cls, dtb_opt, resource_dtb_path, type_dtb_paths):
        for i_type_dtb_path in type_dtb_paths:
            dtb_opt.create_type_assign(
                resource_dtb_path, i_type_dtb_path, kind=dtb_opt.Kinds.ResourceType
            )

    @classmethod
    def create_resource_and_version_(cls, dtb_opt, resource_dtb_path, version_dtb_path, pattern_kwargs):
        force = True
        is_create, dtb_resource = dtb_opt.create_resource(resource_dtb_path)
        if is_create is True or force is True:
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
        if is_create is True or force is True:
            version_stg_path = cls.stg_create_version(dtb_opt, pattern_kwargs)
            # add properties
            dtb_opt.create_property(
                version_dtb_path, 'resource', resource_dtb_path, kind=dtb_opt.Kinds.Version
            )
            dtb_opt.create_property(
                version_dtb_path, 'location', version_stg_path, kind=dtb_opt.Kinds.Version
            )
            cls.dtb_create_storage_fnc(dtb_opt, version_dtb_path, version_stg_path, pattern_kwargs)

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
    def stg_copy_preview(cls, dtb_opt, file_path_src, pattern_kwargs, replace=False):
        file_path_png_src = bsc_storage.ImgOiioOptForThumbnail(file_path_src).generate_thumbnail(width=256, ext='.png')
        file_path_opt = dtb_opt.get_pattern_opt('image-preview-png-file')
        file_path = file_path_opt.update_variants_to(**pattern_kwargs).get_value()
        bsc_storage.StgFileOpt(file_path_png_src).copy_to_file(
            file_path, replace=replace
        )
        return file_path

    @classmethod
    def stg_copy_scene_src(cls, dtb_opt, file_path_src, pattern_kwargs, replace=False):
        file_path_opt = dtb_opt.get_pattern_opt('scene-maya-src-file')
        file_path = file_path_opt.update_variants_to(**pattern_kwargs).get_value()
        bsc_storage.StgFileOpt(file_path_src).copy_to_file(
            file_path, replace=replace
        )
        return file_path

    @classmethod
    def stg_copy_texture(cls, dtb_opt, file_path, pattern_kwargs, keyword):
        p_opt = dtb_opt.get_pattern_opt(keyword)
        stg_path = p_opt.update_variants_to(**pattern_kwargs).get_value()
        bsc_storage.StgFileOpt(file_path).copy_to_file(
            stg_path
        )
        return stg_path

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

    def add_3d_from(self, directory_path_src, type_dtb_path):
        type_opt = bsc_core.PthNodeOpt(type_dtb_path)
        cs = type_opt.get_components()
        category_group_opt = cs[-2]
        category_group = category_group_opt.get_name()
        dtb_opt = bsc_database.DtbOptForResource.generate(category_group)
        #
        variants = {'directory': directory_path_src}
        #
        resource_p = '{directory}/{name}_{var}/{name}_{var}_{number}_Model_{lod}'
        resource_p_opt = bsc_core.PtnParseOpt(resource_p)
        resource_p_opt.update_variants(**variants)
        #
        matches = resource_p_opt.get_matches(sort=True)
        with bsc_log.LogProcessContext.create_as_bar(maximum=len(matches), label='add any 3d') as l_p:
            for i_variants in matches:
                l_p.do_update()
                self.add_3d(
                    dtb_opt, category_group, type_dtb_path, i_variants
                )

    @classmethod
    def add_3d(cls, dtb_opt, category_group, type_dtb_path, variants):
        force = False
        #
        name = variants['name']
        for i in cls.NAME_REPLACE:
            name = name.replace(i[0], i[1])

        var = variants['var']
        var = var.lower()

        type_dtb_path = '{}_{}'.format(type_dtb_path, var)
        dtb_opt.get_type_force(type_dtb_path)

        resource_name = '{}_{}{}_rsc'.format(name, var, str(int(variants['number'])).zfill(3)).lower()

        print type_dtb_path, resource_name

        resource_dtb_path = '/{}/{}'.format(category_group, resource_name)
        version_name = 'v0001'
        version_dtb_path = '{}/{}'.format(resource_dtb_path, version_name)

        pattern_kwargs = dict(
            category_group=category_group,
            resource=resource_name,
            version=version_name,
        )
        cls.create_resource_and_version_(dtb_opt, resource_dtb_path, version_dtb_path, pattern_kwargs)
        cls.dtb_assign_resource_types_fnc(
            dtb_opt, resource_dtb_path, [type_dtb_path]
        )

        preview_p = '{directory}/{name}_{var}/{name}_{var}_{number}_Model_{lod}/{name}_{var}_{number}_Model_{lod}.jpg'
        # preview
        preview_p_opt = bsc_core.PtnParseOpt(preview_p)
        preview_p_opt.update_variants(**variants)
        preview_file_paths_src = preview_p_opt.get_match_results()
        if preview_file_paths_src:
            preview_file_path_src = preview_file_paths_src[0]
            preview_file_path = cls.stg_copy_preview(dtb_opt, preview_file_path_src, pattern_kwargs, replace=force)
            dtb_opt.create_property(
                version_dtb_path, 'image_preview_file', preview_file_path, kind=dtb_opt.Kinds.Version
            )
        # scene
        scene_p = '{directory}/{name}_{var}/{name}_{var}_{number}_Model_{lod}/{name}_{var}_{number}_Model_{lod}_Shader_Ar_Static.ma'
        scene_p_opt = bsc_core.PtnParseOpt(scene_p)
        scene_p_opt.update_variants(**variants)
        scene_file_paths_src = scene_p_opt.get_match_results()
        if scene_file_paths_src:
            scene_file_path_src = scene_file_paths_src[0]
            scene_scr_file_path = cls.stg_copy_scene_src(dtb_opt, scene_file_path_src, pattern_kwargs, replace=force)
            dtb_opt.create_property(
                version_dtb_path, 'image_preview_file', scene_scr_file_path, kind=dtb_opt.Kinds.Version
            )


if __name__ == '__main__':
    for i_d, i_t in [
        # ('/l/temp/td/lib_extract/Asrlry/Assetlibrary/Model/ZhiWu/Cao', '/3d_plant_proxy/grass/lawn'),
        ('/l/temp/td/lib_extract/Asrlry/Assetlibrary/Model/ZhiWu/GuanMu', '/3d_plant_proxy/shrub/forest'),
        ('/l/temp/td/lib_extract/Asrlry/Assetlibrary/Model/ZhiWu/JueLei', '/3d_plant_proxy/fern/forest'),
        ('/l/temp/td/lib_extract/Asrlry/Assetlibrary/Model/ZhiWu/Shu', '/3d_plant_proxy/tree/forest'),
        ('/l/temp/td/lib_extract/Asrlry/Assetlibrary/Model/ZhiWu/YeCao', '/3d_plant_proxy/grass/wild'),
        ('/l/temp/td/lib_extract/Asrlry/Assetlibrary/Model/ZhiWu/YeHua', '/3d_plant_proxy/flower/wild'),
    ]:
        ScpResourcesAddFor3dPlant().add_3d_from(
            i_d, i_t
        )
