# coding:utf-8
# coding:utf-8
if __name__ == '__main__':
    import lxresolver.core as rsv_core

    r = rsv_core.RsvBase.generate_root()

    # rsv_project = r.get_rsv_project(project='cjd')

    rsv_task = r.get_rsv_task(project='cgm', asset='td_test', step='mod_qc', task='modeling_qc')
    version_rsv_unit = rsv_task.get_rsv_unit(
        keyword='asset-release-version-dir'
    )

    print version_rsv_unit.get_new_version()

    # print rsv_task
    # rsv_unit = rsv_task.get_rsv_unit(keyword='asset-geometry-usd-hi-file')
    # print rsv_unit.get_properties_by_result('/l/prod/cjd/publish/assets/chr/td_test/srf/surfacing/td_test.srf.surfacing.v071/cache/usd/geo/hi.usd')
    # print rsv_unit.get_result(version='latest')
    # print rsv_unit.get_latest_version()
    # print rsv_unit.get_new_version()
