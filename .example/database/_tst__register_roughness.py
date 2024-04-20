# coding:utf-8
import lxresource as bsc_resource

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.database as bsc_database

if __name__ == '__main__':

    dtb_opt = bsc_database.DtbOptForResource(
        bsc_resource.RscExtendConfigure.get_yaml('database/library/resource-basic'),
        bsc_resource.RscExtendConfigure.get_yaml('database/library/resource-imperfection')
    )

    p = '/production/library/resource/all/imperfection/{resource_name}/v0001/texture/original/src/{resource_name}.mask.jpg'

    p_o = bsc_core.PtnParseOpt(p)
    for i in p_o.get_matches():
        i_f_src = i['result']
        i_f_o_src = bsc_storage.StgFileOpt(i_f_src)
        i_n = i_f_o_src.get_name().replace('mask', 'roughness')
        i_f_tgt = '{}/{}'.format(i_f_o_src.get_directory_path(), i_n)
        i_dtb_path = '/imperfection/{}/v0001/texture_roughness_file'.format(i['resource_name'])
        bsc_storage.ImgOiioMtd.r_to_rgb(
            i_f_src,
            i_f_tgt
        )
        dtb_opt.create_storage(
            i_dtb_path, kind=dtb_opt.Kinds.File
        )
        dtb_opt.create_property(
            i_dtb_path, 'location', i_f_tgt, kind=dtb_opt.Kinds.File
        )
