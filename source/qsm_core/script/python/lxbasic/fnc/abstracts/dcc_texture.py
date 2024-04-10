# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

import lxbasic.dcc.objects as bsc_dcc_objects


class AbsFncExporterForDccTextureDef(object):
    KEY = 'texture export'

    @classmethod
    def copy_and_repath_as_base_link_fnc(
        cls,
        directory_path_bsc, directory_path_dst,
        #
        dcc_objs,
        # file name auto replace " " to "_"
        fix_name_blank,
        #
        with_reference=False,
        ignore_missing_texture=False,
        remove_expression=False,
        use_environ_map=False,
        repath_fnc=None,
        # copy option
        #   copy source file, etc. use ".tx", auto copy ".exr"
        copy_source=False,
        copy_source_scheme='separate',
        target_extension='.tx',
    ):
        if dcc_objs:
            copy_cache = []
            index_mapper = {}
            # use for file with same name, etc. "/temp/a/a.exr", "/temp/b/a.exr"
            index_query = {}
            with bsc_log.LogProcessContext.create_as_bar(maximum=len(dcc_objs), label=cls.KEY) as l_p:
                for i_dcc_obj in dcc_objs:
                    l_p.do_update()
                    # dpt to dst, file path can be is multiply
                    for j_port_path, j_texture_path_dpt in i_dcc_obj.reference_raw.items():
                        if bsc_storage.StgPathMtd.get_is_exists(j_texture_path_dpt) is False:
                            continue
                        # map path to current platform
                        j_texture_path_dpt = bsc_storage.StgPathMapper.map_to_current(j_texture_path_dpt)
                        j_texture_dpt = bsc_dcc_objects.StgTexture(j_texture_path_dpt)
                        if j_texture_dpt.get_exists_unit_paths() is False:
                            bsc_log.Log.trace_method_warning(
                                cls.KEY,
                                'file="{}" is non exists'.format(j_texture_path_dpt)
                            )
                            continue
                        # fix name overlay
                        if j_texture_path_dpt in index_query:
                            j_index = index_query[j_texture_path_dpt]
                        else:
                            j_key = j_texture_dpt.name
                            if j_key in index_mapper:
                                j_index = index_mapper[j_key]+1
                            else:
                                j_index = 0
                            #
                            index_mapper[j_key] = j_index
                            index_query[j_texture_path_dpt] = j_index
                        #
                        index_mapper[j_key] = j_index
                        #
                        j_directory_path_dst = '{}/v{}'.format(directory_path_dst, j_index)
                        # get dst
                        if copy_source is True:
                            j_texture_path_dst_src, j_texture_path_dst_tgt = j_texture_dpt.get_target_file_path_as_src(
                                directory_path_dst=j_directory_path_dst,
                                #
                                scheme=copy_source_scheme,
                                target_extension=target_extension,
                                #
                                fix_name_blank=fix_name_blank
                            )
                            ext = j_texture_dpt.ext
                            if ext == target_extension:
                                j_texture_path_dst = j_texture_path_dst_tgt
                            else:
                                j_texture_path_dst = j_texture_path_dst_src
                        else:
                            j_texture_path_dst = j_texture_dpt.get_target_file_path(
                                j_directory_path_dst,
                                fix_name_blank=fix_name_blank
                            )
                        # ignore when dpt ( departure ) same to dst ( destination )
                        if j_texture_path_dpt != j_texture_path_dst:
                            # do copy
                            j_file_units_dpt = j_texture_dpt.get_exists_units()
                            if j_file_units_dpt:
                                for k_file_unit_dpt in j_file_units_dpt:
                                    k_file_tile_path = k_file_unit_dpt.path
                                    if k_file_tile_path not in copy_cache:
                                        copy_cache.append(k_file_tile_path)
                                        #
                                        if copy_source is True:
                                            k_file_unit_dpt.copy_unit_as_base_link_with_src(
                                                directory_path_bsc=directory_path_bsc,
                                                directory_path_dst=j_directory_path_dst,
                                                #
                                                scheme=copy_source_scheme,
                                                target_extension=target_extension,
                                                #
                                                fix_name_blank=fix_name_blank,
                                                replace=True
                                            )
                                        else:
                                            k_file_unit_dpt.copy_unit_as_base_link(
                                                directory_path_bsc=directory_path_bsc,
                                                directory_path_dst=j_directory_path_dst,
                                                #
                                                fix_name_blank=fix_name_blank,
                                                replace=True
                                            )
                            else:
                                bsc_log.Log.trace_method_warning(
                                    'texture search',
                                    u'file="{}" is Non-exists'.format(j_texture_path_dpt)
                                )
                                continue
                            # do repath
                            j_texture_dst = bsc_dcc_objects.StgTexture(j_texture_path_dst)
                            if j_texture_dst.get_exists_units():
                                # environ map
                                if use_environ_map is True:
                                    # noinspection PyArgumentEqualDefault
                                    j_texture_path_dst_new = bsc_storage.StgEnvPathMapper.map_to_env(
                                        j_texture_path_dst, pattern='[KEY]'
                                    )
                                    if j_texture_path_dst_new != j_texture_path_dst:
                                        j_texture_path_dst = j_texture_path_dst_new
                                #
                                repath_fnc(
                                    i_dcc_obj,
                                    j_port_path,
                                    j_texture_path_dst,
                                    remove_expression,
                                )
                                bsc_log.Log.trace_method_result(
                                    cls.KEY,
                                    u'"{}" >> "{}"'.format(j_texture_path_dpt, j_texture_path_dst)
                                )
                            else:
                                bsc_log.Log.trace_method_warning(
                                    cls.KEY,
                                    u'file="{}" is non-exists'.format(j_texture_path_dst)
                                )

    @classmethod
    def copy_and_repath_fnc(
        cls,
        directory_path_dst,
        #
        dcc_objs,
        # file name auto replace " " to "_"
        fix_name_blank,
        #
        with_reference=False,
        ignore_missing_texture=False,
        remove_expression=False,
        use_environ_map=False,
        repath_fnc=None,
        # copy option
        #   copy source file, etc. use ".tx", auto copy ".exr"
        copy_source=False,
        copy_source_scheme='separate',
        target_extension='.tx',
    ):
        copy_cache = []
        index_mapper = {}
        # use for file with same name, etc. "/temp/a/a.exr", "/temp/b/a.exr"
        index_query = {}
        with bsc_log.LogProcessContext.create_as_bar(maximum=len(dcc_objs), label=cls.KEY) as l_p:
            for i_dcc_obj in dcc_objs:
                l_p.do_update()
                # dpt to dst
                for j_port_path, j_texture_path_dpt in i_dcc_obj.reference_raw.items():
                    # map path to current platform
                    j_texture_path_dpt = bsc_storage.StgPathMapper.map_to_current(j_texture_path_dpt)
                    j_texture_dpt = bsc_dcc_objects.StgTexture(j_texture_path_dpt)
                    if j_texture_dpt.get_exists_units() is False:
                        bsc_log.Log.trace_method_warning(
                            cls.KEY,
                            'file="{}" is non exists'.format(j_texture_path_dpt)
                        )
                        continue
                    # fix name overlay
                    if j_texture_path_dpt in index_query:
                        j_index = index_query[j_texture_path_dpt]
                    else:
                        j_key = j_texture_dpt.name
                        if j_key in index_mapper:
                            j_index = index_mapper[j_key]+1
                        else:
                            j_index = 0
                        #
                        index_mapper[j_key] = j_index
                        index_query[j_texture_path_dpt] = j_index
                    #
                    index_mapper[j_key] = j_index
                    #
                    j_directory_path_dst = '{}/v{}'.format(directory_path_dst, j_index)
                    # get dst
                    if copy_source is True:
                        j_texture_path_dst_src, j_texture_path_dst_tgt = j_texture_dpt.get_target_file_path_as_src(
                            directory_path_dst=j_directory_path_dst,
                            #
                            scheme=copy_source_scheme,
                            target_extension=target_extension,
                            #
                            fix_name_blank=fix_name_blank
                        )
                        ext = j_texture_dpt.ext
                        if ext == target_extension:
                            j_texture_path_dst = j_texture_path_dst_tgt
                        else:
                            j_texture_path_dst = j_texture_path_dst_src
                    else:
                        j_texture_path_dst = j_texture_dpt.get_target_file_path(
                            j_directory_path_dst,
                            fix_name_blank=fix_name_blank
                        )
                    # ignore when dpt ( departure ) same to dst ( destination )
                    if j_texture_path_dpt != j_texture_path_dst:
                        # do copy
                        j_file_units_dpt = j_texture_dpt.get_exists_units()
                        if j_file_units_dpt:
                            for k_file_unit_dpt in j_file_units_dpt:
                                k_file_tile_path = k_file_unit_dpt.path
                                if k_file_tile_path not in copy_cache:
                                    copy_cache.append(k_file_tile_path)
                                    #
                                    if copy_source is True:
                                        k_file_unit_dpt.copy_unit_with_src(
                                            directory_path_dst=j_directory_path_dst,
                                            #
                                            scheme=copy_source_scheme,
                                            target_extension=target_extension,
                                            #
                                            fix_name_blank=fix_name_blank,
                                            replace=True
                                        )
                                    else:
                                        k_file_unit_dpt.copy_unit_to(
                                            directory_path_dst=j_directory_path_dst,
                                            #
                                            fix_name_blank=fix_name_blank,
                                            replace=True
                                        )
                        else:
                            bsc_log.Log.trace_method_warning(
                                'texture search',
                                'file="{}" is Non-exists'.format(j_texture_path_dpt)
                            )
                            continue
                        # do repath
                        #
                        j_texture_dst = bsc_dcc_objects.StgTexture(j_texture_path_dst)
                        if j_texture_dst.get_exists_units():
                            # environ map
                            if use_environ_map is True:
                                # noinspection PyArgumentEqualDefault
                                j_texture_path_dst_new = bsc_storage.StgEnvPathMapper.map_to_env(
                                    j_texture_path_dst, pattern='[KEY]'
                                )
                                if j_texture_path_dst_new != j_texture_path_dst:
                                    j_texture_path_dst = j_texture_path_dst_new
                            #
                            repath_fnc(
                                i_dcc_obj,
                                j_port_path,
                                j_texture_path_dst,
                                remove_expression,
                            )
                            bsc_log.Log.trace_method_result(
                                'texture export',
                                '"{}" >> "{}"'.format(j_texture_path_dpt, j_texture_path_dst)
                            )
                        else:
                            bsc_log.Log.trace_method_warning(
                                'texture export',
                                'file="{}" is non-exists'.format(j_texture_path_dst)
                            )
