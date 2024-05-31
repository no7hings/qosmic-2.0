# coding:utf-8

def skin_proxy_generate_fnc(option_opt):
    file_path = option_opt.get('file')
    cache_file_path = option_opt.get('cache_file')

    import qsm_maya.rig.scripts as qsm_mya_rig_scripts

    qsm_mya_rig_scripts.AdvSkinProxyProcess(
        file_path, cache_file_path
    ).execute()


def dynamic_gpu_generate_fnc(option_opt):
    file_path = option_opt.get('file')
    cache_file_path = option_opt.get('cache_file')
    namespace = option_opt.get('namespace')
    start_frame = option_opt.get_as_integer('start_frame')
    end_frame = option_opt.get_as_integer('end_frame')
    motion_file = option_opt.get('motion_file')
    use_motion = option_opt.get_as_boolean('use_motion')

    import qsm_maya.rig.scripts as qsm_mya_rig_scripts

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
    file_path = option_opt.get('file')
    movie_file_path = option_opt.get('movie')
    camera_path = option_opt.get('camera')
    start_frame = option_opt.get_as_integer('start_frame')
    end_frame = option_opt.get_as_integer('end_frame')
    frame_step = option_opt.get_as_integer('frame_step') or 1.0
    width = option_opt.get_as_integer('width')
    height = option_opt.get_as_integer('height')
    texture_enable = option_opt.get_as_boolean('texture_enable')
    light_enable = option_opt.get_as_boolean('light_enable')
    shadow_enable = option_opt.get_as_boolean('shadow_enable')

    import lxbasic.web as bsc_web

    import qsm_maya.preview.scripts as qsm_mya_prv_scripts

    qsm_mya_prv_scripts.PlayblastProcess(
        bsc_web.UrlValue.unquote(file_path),
        bsc_web.UrlValue.unquote(movie_file_path),
        camera_path, start_frame, end_frame, frame_step, width, height,
        texture_enable, light_enable, shadow_enable
    ).execute()


def main(session):
    # noinspection PyUnresolvedReferences
    from maya import cmds
    cmds.stackTrace(state=1)
    #
    option_opt = session.get_option_opt()
    key = option_opt.get('method')
    if key == 'skin-proxy-cache-generate':
        skin_proxy_generate_fnc(option_opt)
    elif key == 'dynamic-gpu-cache-generate':
        dynamic_gpu_generate_fnc(option_opt)
    elif key == 'unit-assembly-cache-generate':
        unit_assembly_generate_fnc(option_opt)
    elif key == 'gpu-instance-cache-generate':
        gpu_instance_generate_fnc(option_opt)
    elif key == 'playblast':
        playblast_fnc(option_opt)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
