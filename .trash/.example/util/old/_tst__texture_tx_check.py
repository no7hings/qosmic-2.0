# coding:utf-8
import lxgeneral.dcc.objects as gnl_dcc_objects


def test():
    t = gnl_dcc_objects.StgTexture(
        '/data/f/tx_create_debug/test_1/jiguang_cloth_mask.<udim>.%04d.tx'
        # '/data/f/tx_create_debug/test_1//jiguang_cloth_mask.1001.1001.tx'
    )
    print t.get_is_exists_as_tx()


test()

# cProfile.run(test())
