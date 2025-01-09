# coding:utf-8
import cProfile

import glob

import fnmatch

import os

import scandir


def get_all_directory_paths(directory_path):
    def rcs_fnc_(d_):
        for _i in scandir.scandir(d_):
            if _i.is_dir():
                _i_path = _i.path
                list_.append(_i_path)
                rcs_fnc_(_i_path)
    # noinspection PyUnresolvedReferences
    import scandir

    list_ = []
    if os.path.isdir(directory_path):
        rcs_fnc_(directory_path)
    return list_


def test():
    return glob.glob(
        '/l/temp/td/dongchangbao/tx_convert_test/tx_22/jiguang_cloth_mask.[0-9][0-9][0-9][0-9].[0-9][0-9][0-9][0-9].exr'
    )


def test_1():
    f = '/l/temp/td/dongchangbao/tx_convert_test/tx_22/jiguang_cloth_mask.[0-9][0-9][0-9][0-9].[0-9][0-9][0-9][0-9].tx'
    return fnmatch.filter(
        [i.path for i in scandir.scandir(os.path.dirname(f))], f
    )


# cProfile.run("test()")
cProfile.run("test_1()")
