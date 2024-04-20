# coding:utf-8
import lxbasic.dcc.objects as bsc_dcc_objects


def test():
    t = bsc_dcc_objects.StgTexture(
        '/data/f/tx_create_debug/test_1/jiguang_cloth_mask.<udim>.%04d.tx'
        # '/data/f/tx_create_debug/test_1//jiguang_cloth_mask.1001.1001.tx'
    )
    print t.get_is_exists_as_tx()


test()

# cProfile.run(test())
