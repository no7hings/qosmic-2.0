# coding:utf-8
from __future__ import print_function


class Setup(object):
    def __init__(self):
        pass

    def run(self):
        print('lx-dcc menu setup: is started')
        import lxbasic.resource as bsc_resource

        import lxclarisse.startup as crs_startup

        crs_startup.MenuBuild._create_by_yaml_(
            bsc_resource.BscConfigure.get_yaml('clarisse/gui/menu')
        )
        print('lx-dcc menu setup: is completed')


if __name__ == '__main__':
    Setup().run()
