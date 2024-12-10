# coding:utf-8
import qsm_general.core as qsm_gnl_core

import qsm_lazy_sync as qsm_lzy_sync

version_path = 'X:/QSM_TST/QSM/release/assets/chr/lily/cfx.cfx_rig/lily.cfx.cfx_rig.v011'


studio = 'XSH'

symlink_kwargs = qsm_gnl_core.Sync().generate_sync_kwargs(
    studio, version_path
)

print symlink_kwargs

# if symlink_kwargs:
#     qsm_lzy_sync.TaskClient.new_task(
#         'sync', **symlink_kwargs
#     )
