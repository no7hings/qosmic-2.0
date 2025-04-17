# coding:utf-8
import os

import cProfile

os.environ['QSM_UI_LANGUAGE'] = 'chs'


def test():
    import lxbasic.session as bsc_session

    bsc_session.Hook.execute(
        '*/qsm-lazy-workspace'
    )
    # import lxbasic.session as bsc_session; bsc_session.Hook.execute("desktop-tools/qsm-lazy-workspace")


test()
# cProfile.run('test()')
