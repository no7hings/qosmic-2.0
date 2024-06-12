# coding:utf-8
import datetime

import parse

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import qsm_screw.core as qsm_scr_core

import lxbasic.media.core as bsc_mda_core

import os

asset_type = 'video'

d = 'F:/video/film'

location = 'Z:/libraries/media/all'

stage = qsm_scr_core.Stage(
    'Z:/libraries/media/.database/video.db'
)
stage.connect()

ps = [
    '{gui_name}[{gui_name_chs}]',
    '{gui_name}[{gui_name_chs}]({year})',
    '{gui_name}[{gui_name_chs}][｛special_tag｝]',
    '{gui_name}[{gui_name_chs}][｛special_tag｝]({year})',
]

ps.reverse()

for i_directory in bsc_storage.StgDirectoryOpt(
    d
).get_directories():
    i_files = i_directory.get_files(ext_includes=['.mkv', '.mp4', '.mov', '.rmvb'])
    if i_files:
        i_file = i_files[0]
        for j in ps:
            j_r = parse.parse(
                j, i_directory.name
            )
            if j_r:
                i_data = dict(
                    gui_name='',
                    gui_name_chs='',
                    year='',
                    special_tag=''
                )
                i_data.update(j_r.named)

                i_name = bsc_core.RawTextMtd.clear_up_to(i_data['gui_name']).lower()

                i_gui_name = bsc_core.RawTextMtd.to_prettify(i_name)

                i_node_path = '/{}/{}'.format(asset_type, i_name)

                try:
                    ctime = i_file.get_creation_timestamp()
                    stage.create_node(
                        i_node_path,
                        gui_name=i_gui_name,
                        gui_name_chs=i_data['gui_name_chs'],
                        ctime=ctime,
                    )
                except:
                    stage.create_node(
                        i_node_path,
                        gui_name=i_gui_name,
                        gui_name_chs=i_data['gui_name_chs'],
                    )

                i_node_directory_path = '{}{}'.format(location, i_node_path)

                bsc_storage.StgDirectoryOpt(i_node_directory_path).do_create()

                i_type_path = '/video/movies/unspecified'
                stage.create_assign(i_node_path, i_type_path, type='type_assign')

                i_tag_path = '/years/{}'.format(i_data['year'])
                stage.create_entity(
                    stage.EntityTypes.Tag, i_tag_path, gui_name=i_data['year'], gui_name_chs=i_data['year'],
                    category='node', type='node'
                )
                stage.create_assign(i_node_path, i_tag_path, type='tag_assign')

                stage.create_property(
                    i_node_path, 'directory', i_directory.path, type='parameter'
                )
                stage.create_property(
                    i_node_path, 'video', i_file.path, type='parameter'
                )

                i_thumbnail_path = '{}/image/{}.jpg'.format(i_node_directory_path, i_name)

                if os.path.isfile(i_thumbnail_path) is False:
                    print i_thumbnail_path
                    try:
                        bsc_mda_core.FrameExtractor(
                            i_file.path, i_thumbnail_path
                        ).run()
                    except Exception:
                        print i_file.path

                if os.path.isfile(i_thumbnail_path):
                    if os.path.isfile(i_thumbnail_path):
                        stage.create_property(
                            i_node_path, 'thumbnail', i_thumbnail_path, type='parameter'
                        )

                break
    else:
        print i_directory
