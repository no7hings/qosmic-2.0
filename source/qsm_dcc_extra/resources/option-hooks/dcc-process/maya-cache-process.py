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
    start_frame = int(option_opt.get('start_frame'))
    end_frame = int(option_opt.get('end_frame'))

    import qsm_maya.rig.scripts as qsm_mya_rig_scripts

    qsm_mya_rig_scripts.DynamicGpuCacheProcess(
        file_path, cache_file_path, namespace, start_frame, end_frame
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


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
