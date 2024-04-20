# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.dcc.core as bsc_dcc_core

import lxbasic.storage as bsc_storage

import lxbasic.dcc.objects as bsc_dcc_objects


def setup_fnc_():
    bsc_dcc_core.OcioSetup(
        bsc_storage.StgPathMapper.map_to_current(
            '/l/packages/pg/third_party/ocio/aces/1.2'
        )
    ).set_run()

    import lxarnold.startup as and_startup

    and_startup.MtoaSetup(
        '/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019'
    ).set_run()


setup_fnc_()

d = bsc_dcc_objects.StgDirectory('/l/temp/td/dongchangbao/tx_convert_test/exr_1')

output_directory_path = '/l/temp/td/dongchangbao/tx_convert_test/tx_17'

file_paths = d.get_all_file_paths(ext_includes=['.exr'])

if output_directory_path:
    bsc_dcc_objects.StgDirectory(
        output_directory_path
    ).set_create()


def finished_fnc_(index, status, results):
    print index, status


def status_changed_fnc_(index, status):
    print index, status


with bsc_log.LogProcessContext.create_as_bar(maximum=len(file_paths), label='test') as l_p:
    for i_index, i_file_path in enumerate(file_paths):
        l_p.do_update()
        i_cmd = bsc_dcc_objects.StgTexture._get_unit_tx_create_cmd_by_src_(
            i_file_path,
            search_directory_path=output_directory_path,
        )
        if i_cmd:
            bsc_core.TrdCommandPool.set_wait()
            i_t = bsc_core.TrdCommandPool.set_start(i_cmd, index=i_index)
            i_t.finished.connect_to(
                finished_fnc_
            )
            i_t.status_changed.connect_to(
                status_changed_fnc_
            )
