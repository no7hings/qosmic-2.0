# coding:utf-8


def skin_proxy_generate_fnc(option_opt):
    file_path = option_opt.get('file')
    cache_file_path = option_opt.get('cache_file')
    data_file_path = option_opt.get('data_file')

    import qsm_maya.animation.scripts as qsm_mya_rig_scripts

    qsm_mya_rig_scripts.AdvSkinProxyProcess(
        file_path, cache_file_path, data_file_path
    ).execute()


def dynamic_gpu_generate_fnc(option_opt):
    file_path = option_opt.get('file')
    cache_file_path = option_opt.get('cache_file')
    namespace = option_opt.get('namespace')
    start_frame = option_opt.get_as_integer('start_frame')
    end_frame = option_opt.get_as_integer('end_frame')
    motion_file = option_opt.get('motion_file')
    use_motion = option_opt.get_as_boolean('use_motion')

    import qsm_maya.animation.scripts as qsm_mya_rig_scripts

    qsm_mya_rig_scripts.DynamicGpuCacheProcess(
        file_path, cache_file_path, namespace, start_frame, end_frame, motion_file, use_motion
    ).execute()


def unit_assembly_generate_fnc(option_opt):
    file_path = option_opt.get('file')
    cache_file_path = option_opt.get('cache_file')

    import qsm_maya.scenery.scripts as qsm_mya_scn_scripts

    qsm_mya_scn_scripts.UnitAssemblyProcess(
        file_path, cache_file_path
    ).execute()


def gpu_instance_generate_fnc(option_opt):
    file_path = option_opt.get('file')
    cache_file_path = option_opt.get('cache_file')

    import qsm_maya.scenery.scripts as qsm_mya_scn_scripts

    qsm_mya_scn_scripts.GpuInstanceProcess(
        file_path, cache_file_path
    ).execute()


def playblast_fnc(option_opt):
    import qsm_general.core as qsm_gnl_core

    import qsm_maya.preview.scripts as qsm_mya_prv_scripts

    dict_ = qsm_gnl_core.MayaCacheProcess.to_option_dict(
        option_opt.to_string()
    )

    file_path = dict_.get('file')
    movie_file_path = dict_.get('movie')
    camera_path = dict_.get('camera')
    start_frame = dict_.get('start_frame')
    end_frame = dict_.get('end_frame')
    frame_step = dict_.get('frame_step') or 1.0
    width = dict_.get('width')
    height = dict_.get('height')
    texture_enable = dict_.get('texture_enable')
    light_enable = dict_.get('light_enable')
    shadow_enable = dict_.get('shadow_enable')

    qsm_mya_prv_scripts.PlayblastProcess(
        file_path,
        movie_file_path,
        camera_path, start_frame, end_frame, frame_step, width, height,
        texture_enable, light_enable, shadow_enable
    ).execute()


def cfx_cloth_cache_generate_fnc(option_opt):
    import qsm_general.core as qsm_gnl_core

    import qsm_maya.cfx.scripts as qsm_mya_cfx_scripts

    kwargs = qsm_gnl_core.MayaCacheProcess.to_option_dict(
        option_opt.to_string()
    )

    qsm_mya_cfx_scripts.CfxNClothCacheProcess(
        **kwargs
    ).execute()


def test_unicode(method, option_opt):
    pass


def main(session):
    # noinspection PyUnresolvedReferences
    from maya import cmds
    cmds.stackTrace(state=1)
    #
    option_opt = session.get_option_opt()
    method = option_opt.get('method')
    if method == 'skin-proxy-cache-generate':
        skin_proxy_generate_fnc(option_opt)
    elif method == 'dynamic-gpu-cache-generate':
        dynamic_gpu_generate_fnc(option_opt)
    elif method == 'unit-assembly-cache-generate':
        unit_assembly_generate_fnc(option_opt)
    elif method == 'gpu-instance-cache-generate':
        gpu_instance_generate_fnc(option_opt)
    elif method == 'cfx-cloth-cache-generate':
        cfx_cloth_cache_generate_fnc(option_opt)
    elif method == 'playblast':
        playblast_fnc(option_opt)
    # test
    elif method == 'test-unicode':
        test_unicode(method, option_opt)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
