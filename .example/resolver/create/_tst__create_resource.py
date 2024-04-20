# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

import lxresolver.core as rsv_core

import lxbasic.shotgun as bsc_shotgun

bsc_log.Log.RESULT_ENABLE = False

r = rsv_core.RsvBase.generate_root()

rsv_project = r.get_rsv_project(project='nsa_dev')

c = bsc_shotgun.StgConnector()

dict_ = {}

for i in [
    u'master_cabinet',
    u'master_chair',
    u'master_clothes_drying_rack',
    u'master_desk',
    u'master_fan',
    u'master_potted_plant_a',
    u'master_potted_plant_b',
    u'master_rain_boots',
    u'master_room',
    u'master_wall'
]:
    i_asset = 'tst' + i[len('master'):]

    i_kwargs = dict(
        root=rsv_project.properties.get('root'),
        workspace=rsv_project.to_workspace('source'),
        project='nsa_dev',
        role='env',
        asset=i_asset,
        step='mod',
        task='modeling',
        task_extra='modeling',
        version='v000_000'
    )

    print i_kwargs

    p_o = rsv_project.get_pattern_opt('asset-source-maya-scene-src-file')

    i_file_path = p_o.update_variants_to(**i_kwargs).get_value()

    i_file_opt = bsc_storage.StgFileOpt(i_file_path)

    print i_file_opt

    dict_[i] = i_file_path

    # bsc_storage.StgPathPermissionMtd.create_directory(
    #     i_file_opt.get_directory_path()
    # )

    # i_rsv_resource = rsv_project.get_rsv_resource(
    #     role='env', asset=i_asset
    # )
    # if i_rsv_resource is not None:
    #     pass

    # print c.get_stg_resource(
    #     project='nsa_dev', role='env', asset=i_asset
    # )

    # rsv_project.create_resource_directory(
    #     role='env', asset=i_asset
    # )

print dict_
