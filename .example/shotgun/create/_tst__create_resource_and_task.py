# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.shotgun as bsc_shotgun

bsc_log.Log.RESULT_ENABLE = False

c = bsc_shotgun.StgConnector()

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

    # c.create_stg_resource(
    #     project='nsa_dev', role='env', asset=i_asset
    # )

    # modeling
    # c.create_stg_task(
    #     project='nsa_dev', role='env', asset=i_asset, step='mod', task='modeling'
    # )
    # i_modeling_task_q = c.get_stg_task_query(
    #     project='nsa_dev', role='env', asset=i_asset, step='mod', task='modeling'
    # )
    # i_modeling_task_o = bsc_shotgun.StgTaskOpt(
    #     i_modeling_task_q
    # )
    #
    # for j_user in [
    #     'dongchangbao',
    #     'qiuhua'
    # ]:
    #     i_modeling_task_o.append_assign_stg_user(
    #         c.get_stg_user(
    #             user=j_user
    #         )
    #     )
    # surfacing
    # c.create_stg_task(
    #     project='nsa_dev', role='env', asset=i_asset, step='srf', task='surfacing'
    # )
    i_surfacing_task_q = c.get_stg_task_query(
        project='nsa_dev', role='env', asset=i_asset, step='srf', task='surfacing'
    )
    i_surfacing_task_o = bsc_shotgun.StgTaskOpt(
        i_surfacing_task_q
    )

    for j_user in [
        'dongchangbao',
        'qiuhua'
    ]:
        i_surfacing_task_o.append_assign_stg_user(
            c.get_stg_user(
                user=j_user
            )
        )


