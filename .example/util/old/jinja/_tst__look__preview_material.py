# coding:utf-8


if __name__ == '__main__':
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxresource as bsc_resource

    data = bsc_storage.StgFileOpt(
        '/production/library/resource/all/3d_plant_proxy/tree_a001_rsc/v0001/look/json/tree_a001_rsc.preview.json'
    ).set_read()
    r = bsc_resource.RscExtendJinja.get_result(
        'usda/look/preview-material-diffuse',
        data
    )

    print r

    bsc_storage.StgFileOpt(
        '/production/library/resource/all/3d_plant_proxy/tree_a001_rsc/v0001/look/usd/tree_a001_rsc.preview.usda'
    ).set_write(r)
