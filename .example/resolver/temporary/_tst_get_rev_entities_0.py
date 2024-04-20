# coding:utf-8
if __name__ == '__main__':
    import lxresolver.core as rsv_core

    r = rsv_core.RsvBase.generate_root()

    src_rsv_project = r.get_rsv_project(project='shl')
    tgt_rsv_project = r.get_rsv_project(project='cjd')

    assets = [
        'cao_a',
        'cao_b',
        'cao_c',
        'cao_d'
    ]

    task_args = [
        ('mod', 'modeling'),
        ('mod', 'mod_dynamic'),
        ('rig', 'rigging'),
        ('srf', 'surfacing')
    ]

    for src_asset in assets:
        src_rsv_asset = src_rsv_project.get_rsv_resource(asset=src_asset)
        if src_rsv_asset is not None:
            for step, task in task_args:
                src_rsv_task = src_rsv_asset.get_rsv_task(step=step, task=task)
                src_rsv_unit = src_rsv_task.get_rsv_unit(keyword='asset-geometry-abc-hi-file')
                print src_rsv_unit.get_result(version='v001')
