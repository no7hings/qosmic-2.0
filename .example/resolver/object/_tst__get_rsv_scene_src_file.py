# coding:utf-8
import lxresolver.core as rsv_core

r = rsv_core.RsvBase.generate_root()

rsv_project = r.get_rsv_project(
    project='nsa_dev'
)
if rsv_project is not None:
    rsv_task = rsv_project.get_rsv_task(
        asset='surface_workspace',
        step='srf',
        task='surface'
    )
    if rsv_task is not None:
        keyword = 'asset-source-katana-scene-src-file'
        rsv_unit = rsv_task.get_rsv_unit(
            keyword=keyword
        )
        # print rsv_unit.pattern
        results = rsv_unit.get_result(
            version='all',
            variants_extend=dict(task_extra='surface')
        )
        print results
        # print rsv_unit.get_result(version='new', variants_extend=dict(task_extra='surface'))


