# coding:utf-8
from . import _base


class MayaTaskSubprocess(_base.DccProcess):
    OPTION_HOOK_KEY = 'maya-task-process'

    class TaskKeys:
        ShotAnimationCacheExport = 'shot_animation_cache_export'
        ShotCfxClothCacheExport = 'shot_cfx_cloth_cache_export'

        AssetCfxRigRelease = 'asset_cfx_rig_release'
        ShotCfxDressingRelease = 'shot_cfx_dressing_release'
