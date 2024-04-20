# coding:utf-8
if __name__ == '__main__':
    import lxresolver.core as rsv_core

    r = rsv_core.RsvBase.generate_root()

    rsv_project = r.get_rsv_project(project='cjd')

    print rsv_project.get_rsv_resource(asset='sce_td_test')
