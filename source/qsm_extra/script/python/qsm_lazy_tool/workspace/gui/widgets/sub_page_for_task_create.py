# coding:utf-8
import copy

from ..abstracts import sub_page_for_task_create as _sub_page_for_task_create

import qsm_wsp_task as qsm_dcc_wsp_task


class PrxSubPageForAssetCfxRigCreate(_sub_page_for_task_create.AbsPrxSubPageForAssetTaskCreate):
    GUI_KEY = 'cfx_rig'

    RESOURCE_BRANCH = 'asset'

    STEP = 'cfx'

    TASK = 'cfx_rig'

    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(PrxSubPageForAssetCfxRigCreate, self).__init__(window, session, sub_window, *args, **kwargs)

    def do_gui_refresh_all(self):
        resource_properties = self._sub_window._resource_properties
        if resource_properties:
            kwargs_new = copy.copy(resource_properties)
            kwargs_new['step'] = 'rig'
            kwargs_new['task'] = 'rigging'
            task_parse = qsm_dcc_wsp_task.TaskParse()
            rig_scene_ptn_opt = task_parse.generate_pattern_opt_for(
                'asset-disorder-rig_scene-maya-file', **kwargs_new
            )
            matches = rig_scene_ptn_opt.find_matches()
            if matches:
                rig_scene_path = matches[0]['result']
                self._prx_options_node.set('upstream_scene', rig_scene_path)


class PrxSubPageForShotCfxClothCreate(_sub_page_for_task_create.AbsPrxSubPageForAssetTaskCreate):
    GUI_KEY = 'cfx_cloth'

    RESOURCE_BRANCH = 'shot'

    STEP = 'cfx'

    TASK = 'cfx_cloth'

    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(PrxSubPageForShotCfxClothCreate, self).__init__(window, session, sub_window, *args, **kwargs)

    def do_gui_refresh_all(self):
        resource_properties = self._sub_window._resource_properties
        if resource_properties:
            kwargs_new = copy.copy(resource_properties)
            kwargs_new['step'] = 'ani'
            kwargs_new['task'] = 'animation'
            task_parse = qsm_dcc_wsp_task.TaskParse()
            animation_scene_ptn_opt = task_parse.generate_pattern_opt_for(
                'shot-disorder-animation_scene-file', **kwargs_new
            )
            matches = animation_scene_ptn_opt.find_matches()
            if matches:
                rig_scene_path = matches[0]['result']
                self._prx_options_node.set('upstream_scene', rig_scene_path)
