# coding:utf-8
import cProfile

import lxbasic.dcc.objects as bsc_dcc_objects


def test():
    print len(bsc_dcc_objects.StgFile._get_exists_file_paths_('/l/temp/td/dongchangbao/tx_convert_test/exr/jiguang_cloth_mask.<udim>.####.exr'))


def test_1():
    print len(bsc_dcc_objects.StgFile._get_exists_file_paths__('/l/temp/td/dongchangbao/tx_convert_test/exr/jiguang_cloth_mask.<udim>.####.exr'))


def test_2():
    print len(bsc_dcc_objects.StgFile.get_exists_unit_paths_fnc('/l/temp/td/dongchangbao/tx_convert_test/exr/jiguang_cloth_mask.<udim>.####.exr'))


# cProfile.run("test()")
# cProfile.run("test_1()")
cProfile.run("test_2()")

