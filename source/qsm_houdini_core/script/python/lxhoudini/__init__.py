# coding:utf-8


class Packages(object):
    @classmethod
    def set_reload(cls):
        set_reload()


def set_reload(modules=None):
    import lxbasic.core as bsc_core

    if isinstance(modules, (tuple, list)):
        p = bsc_core.PyReloader(modules)
    else:
        p = bsc_core.PyReloader(
            [
                'lxbasic', 'lxsession', 'lxuniverse', 'lxresolver', 'lxarnold',
                'lxusd',
                'lxgui',
                'lxshotgun',
                'lxhoudini', 'lxhoudini_tool'
            ]
        )
    p.set_reload()
