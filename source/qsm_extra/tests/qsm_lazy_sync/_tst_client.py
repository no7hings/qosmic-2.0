# coding:utf-8
import qsm_lazy_sync.client as c

c.TaskClient.requeue_tasks()

# # symlink
# for i in range(10):
#     c.TaskClient.new_task(
#         'symlink',
#         source='X:/QSM_TST/QSM/release/assets/chr/lily/cfx.cfx_rig/lily.cfx.cfx_rig.v005',
#         target='Z:/temporaries/copy_test/symlink/lily.cfx.cfx_rig.v{}'.format(str(i).zfill(3)),
#         replace=True
#     )
#
# copytree
# for i in range(50):
#     c.TaskClient.new_task(
#         'copytree',
#         source='X:/QSM_TST/QSM/release/assets/chr/lily/cfx.cfx_rig/lily.cfx.cfx_rig.v005',
#         target='Z:/temporaries/copy_test/copytree/lily.cfx.cfx_rig.v{}'.format(str(i).zfill(3)),
#         replace=False
#     )

# print c.TaskClient.check_status()

# c.TaskClient.new_task(
#     'sync',
#     source='X:/QSM_TST/QSM/release/assets/chr/lily/cfx.cfx_rig/lily.cfx.cfx_rig.v005',
#     targets=[
#         'Z:/temporaries/copy_test/sync/a/lily.cfx.cfx_rig.v005',
#         'Z:/temporaries/copy_test/sync/b/lily.cfx.cfx_rig.v005'
#     ],
#     replace=False
# )
