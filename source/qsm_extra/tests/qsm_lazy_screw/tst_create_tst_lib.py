import random

import time

import datetime

import qsm_lazy.screw.core as qsm_lzy_scr_core

import lxbasic.resource as bsc_resource

video_paths = [
    'Z:/temeporaries/dongchangbao/playblast_tool/test.v014.mov',
    'Z:/temeporaries/dongchangbao/playblast_tool/test.v017.mov',
    # 'Z:/temeporaries/dongchangbao/playblast_tool/test.export.v006.mov'
]


if __name__ == '__main__':

    stage = qsm_lzy_scr_core.Stage(
        'test'
    )
    #
    # stage.connect()
    stage.build()

    random.seed(0)
    type_paths = [
        x.path for x in stage.find_all(
            stage.EntityTypes.Type,
            filters=[
                ('type', 'is', 'node'),
                ('kind', 'is not', 'unavailable')
            ]
        )
    ]
    tag_paths = [
        x.path for x in stage.find_all(
            stage.EntityTypes.Tag,
            filters=[
                ('type', 'is', 'node'),
                ('kind', 'is not', 'unavailable')
            ]
        )
    ]

    today = datetime.datetime.today()
    maximum = int(time.mktime(today.timetuple()))
    start_of_year = today.replace(month=1, day=1)
    minimum = int(time.mktime(start_of_year.timetuple()))

    ctimes = range(minimum, maximum)

    for i in range(100):
        i_node_path = '/test_{}'.format(i)

        stage.create_node(i_node_path, ctime=random.choice(ctimes))
        if i%3:
            for j in range(2):
                j_type_path = random.choice(type_paths)
                stage.create_assign(i_node_path, j_type_path, type='type_assign')

        if i%2:
            for j in range(2):
                j_tag_path = random.choice(tag_paths)
                stage.create_assign(i_node_path, j_tag_path, type='tag_assign')

        stage.upload_node_preview(
            i_node_path, random.choice(video_paths)
        )
