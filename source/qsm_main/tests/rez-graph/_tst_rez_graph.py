# coding:utf-8
import os

import cProfile

os.environ['QSM_UI_LANGUAGE'] = 'chs'


def test():
    import lxbasic.session as bsc_session

    bsc_session.OptionHook.execute(
        'option_hook_key=desktop-tools/rez-graph&packages=qsm_maya_main'
    )


test()
# cProfile.run('test()')
