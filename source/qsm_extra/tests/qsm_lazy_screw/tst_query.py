import qsm_lazy.screw.core as qsm_lzy_scr_core

import lxbasic.resource as bsc_resource

import lxbasic.core as bsc_core


if __name__ == '__main__':
    print qsm_lzy_scr_core.Stage.get_all_keys()

    # stage = qsm_lzy_scr_core.Stage(
    #     'maya_cfx'
    # )
    #
    # stage.connect()



    # stage.update_entity(
    #     stage.EntityTypes.Property,
    #     '/node/piao_dai_A.thumbnail',
    #     value='Z:/libraries/lazy-resource/all/node/piao_dai_A/thumbnail/piao_dai_A.png'
    # )

    # stage.upload_node_preview(
    #     '/node/piao_dai_A', 'C:/Users/nothings/screenshot/untitled-SEYM9Z.jpg'
    # )
    #
    # stage.upload_node_preview(
    #     '/node/piao_dai_B', 'Z:/temeporaries/dongchangbao/playblast_tool/test.v008.mov'
    # )

    # print stage.find_all_by_ctime_tag('Node', 'yesterday')

    # print stage.find_one(
    #     'Node', filters=[
    #         ('path', 'is', '/video/100_yen_love')
    #     ]
    # ).ctime