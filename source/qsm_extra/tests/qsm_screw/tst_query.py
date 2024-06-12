import qsm_screw.core as qsm_scr_core

import lxbasic.resource as bsc_resource

import lxbasic.core as bsc_core

print bsc_core.TimestampOpt(1718000000).get_as_tag()


if __name__ == '__main__':
    stage = qsm_scr_core.Stage(
        # 'Z:/libraries/screw/.database/node.db'
        'Z:/libraries/media/.database/video.db'
    )

    stage.connect()

    print stage.find_all_by_ctime_tag('Node', 'yesterday')

    # print stage.find_one(
    #     'Node', filters=[
    #         ('path', 'is', '/video/100_yen_love')
    #     ]
    # ).ctime
