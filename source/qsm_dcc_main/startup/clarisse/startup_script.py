# coding:utf-8


class Setup(object):
    def __init__(self):
        pass

    def run(self):
        print 'lx-dcc menu setup: is started'
        import lxresource as bsc_resource

        import lxclarisse.startup as crs_startup

        crs_startup.MenuBuild._create_by_yaml_(
            bsc_resource.RscExtendConfigure.get_yaml('clarisse/gui/menu')
        )
        print 'lx-dcc menu setup: is completed'


if __name__ == '__main__':
    Setup().run()
