# coding:utf-8
import lxbasic.fnc.abstracts as bsc_fnc_abstracts
# katana
# katana dcc
from ...dcc import objects as ktn_dcc_objects


class FncCreatorForLookWorkspaceOld(bsc_fnc_abstracts.AbsFncOptionBase):
    OPTION = dict(
        localtion='',
        look_path='default'
    )

    def __init__(self, option=None):
        super(FncCreatorForLookWorkspaceOld, self).__init__(option)
        #
        self._ktn_workspace = ktn_dcc_objects.AssetWorkspaceOld(
            self.get('location')
        )

    @classmethod
    def _get_rsv_asset_auto_(cls):
        import lxresolver.core as rsv_core

        file_path = ktn_dcc_objects.Scene.get_current_file_path()

        if file_path:
            resolver = rsv_core.RsvBase.generate_root()
            rsv_task = resolver.get_rsv_task_by_any_file_path(file_path)
            if rsv_task:
                rsv_asset = rsv_task.get_rsv_resource()
                return rsv_asset

    def set_run(self):
        self._ktn_workspace.set_workspace_create()
        self._ktn_workspace.set_variables_registry()
        #
        # rsv_asset = self._get_rsv_asset_auto_()
        # if rsv_asset is not None:
        #     ktn_core.VariablesSetting().set_register_by_configure(
        #         {
        #             'layer': ['master', 'no_hair'],
        #             'quality': ['low', 'med', 'hi', 'custom'],
        #             'camera': ['full_body', 'upper_body', 'close_up', 'add_0', 'add_1', 'asset_free', 'shot', 'shot_free'],
        #             'light_pass': ['all'],
        #             'look_pass': ['default', 'plastic', 'ambocc', 'wire', 'white'],
        #             'variables_enable': ['on', 'off']
        #         }
        #     )
