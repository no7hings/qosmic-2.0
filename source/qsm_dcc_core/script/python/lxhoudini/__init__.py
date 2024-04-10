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
                'lxresource', 'lxcontent', 'lxbasic', 'lxsession', 'lxuniverse', 'lxresolver', 'lxarnold',
                'lxusd',
                'lxutil', 'lxgui',
                'lxshotgun',
                'lxhoudini', 'lxhoudini_gui'
            ]
        )
    p.set_reload()
