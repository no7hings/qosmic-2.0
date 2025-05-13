# coding:utf-8
import sys


def skin_proxy_generate_fnc(option_opt):
    file_path = option_opt.get('file')
    cache_file_path = option_opt.get('cache_file')
    data_file_path = option_opt.get('data_file')

    import qsm_maya.handles.animation.scripts as qsm_mya_hdl_anm_scripts

    qsm_mya_hdl_anm_scripts.AdvSkinProxyProcess(
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

    import qsm_maya.handles.animation.scripts as qsm_mya_hdl_anm_scripts

    qsm_mya_hdl_anm_scripts.DynamicGpuCacheProcess(
        file_path, cache_file_path, namespace, start_frame, end_frame, motion_file, use_motion
    ).execute()


def unit_assembly_cache_generate_fnc(option_opt):
    file_path = option_opt.get('file')
    cache_file_path = option_opt.get('cache_file')

    import qsm_maya.handles.scenery.scripts as qsm_mya_hdl_scn_scripts

    qsm_mya_hdl_scn_scripts.UnitAssemblyProcess(
        file_path, cache_file_path
    ).execute()


def gpu_instance_generate_fnc(option_opt):
    file_path = option_opt.get('file')
    cache_file_path = option_opt.get('cache_file')

    import qsm_maya.handles.scenery.scripts as qsm_mya_hdl_scn_scripts

    qsm_mya_hdl_scn_scripts.GpuInstanceProcess(
        file_path, cache_file_path
    ).execute()


def playblast_fnc(option_opt):
    import qsm_general.process as qsm_gnl_process

    import qsm_maya.handles.general.scripts as qsm_mya_hdl_gnl_scripts

    qsm_mya_hdl_gnl_scripts.PlayblastProcess(
        **qsm_gnl_process.MayaCacheSubprocess.to_option_kwargs(option_opt.to_string())
    ).execute()


def cfx_cloth_cache_generate_fnc(option_opt):
    import qsm_general.process as qsm_gnl_process

    import qsm_maya.handles.cfx.scripts as qsm_mya_hdl_cfx_scripts

    qsm_mya_hdl_cfx_scripts.CfxNClothCacheProcess(
        **qsm_gnl_process.MayaCacheSubprocess.to_option_kwargs(option_opt.to_string())
    ).execute()


def shot_animation_cache_export_fnc(option_opt):
    import qsm_general.process as qsm_gnl_process

    import lnx_maya_wotrix_tasks.shot.animation.dcc_scripts as s

    s.ShotAnimationCacheProcess(
        **qsm_gnl_process.MayaCacheSubprocess.to_option_kwargs(option_opt.to_string())
    ).execute()


def shot_cfx_cloth_cache_export_fnc(option_opt):
    import qsm_general.process as qsm_gnl_process

    import lnx_maya_wotrix_tasks.shot.cfx_cloth.dcc_scripts as s

    s.ShotCfxClothCacheExportProcess(
        **qsm_gnl_process.MayaCacheSubprocess.to_option_kwargs(option_opt.to_string())
    ).execute()


def rig_validation_fnc(option_opt):
    import qsm_general.process as qsm_gnl_process

    import lnx_maya_tool_prc.validation.tasks as s

    s.RigValidationTaskSubprocess(
        **qsm_gnl_process.MayaCacheSubprocess.to_option_kwargs(option_opt.to_string())
    ).execute()


def scenery_validation_fnc(option_opt):
    import qsm_general.process as qsm_gnl_process

    import lnx_maya_tool_prc.validation.tasks as s

    s.SceneryValidationTaskSubprocess(
        **qsm_gnl_process.MayaCacheSubprocess.to_option_kwargs(option_opt.to_string())
    ).execute()


def mesh_count_generate_fnc(option_opt):
    import qsm_general.process as qsm_gnl_process

    import lnx_maya_resora.scripts as s

    s.AssetMeshCountProcess(
        **qsm_gnl_process.MayaCacheSubprocess.to_option_kwargs(option_opt.to_string())
    ).execute()


def snapshot_generate_fnc(option_opt):
    import qsm_general.process as qsm_gnl_process

    import lnx_maya_resora.scripts as s

    s.AssetSnapshotProcess(
        **qsm_gnl_process.MayaCacheSubprocess.to_option_kwargs(option_opt.to_string())
    ).execute()


def unit_assembly_generate_fnc(option_opt):
    import qsm_general.process as qsm_gnl_process

    import lnx_maya_resora.scripts as s

    s.AssetUnitAssemblyGenerateProcess(
        **qsm_gnl_process.MayaCacheSubprocess.to_option_kwargs(option_opt.to_string())
    ).execute()
    

def fx_proxy_rig_generate_fnc(option_opt):
    import qsm_general.process as qsm_gnl_process
    
    import lnx_maya_resora.scripts as s

    s.FxProxyRigGenerateProcess(
        **qsm_gnl_process.MayaCacheSubprocess.to_option_kwargs(option_opt.to_string())
    ).execute()


def shot_replace_reference_fnc(option_opt):
    import qsm_general.process as qsm_gnl_process

    import lnx_maya_tool_prc.shot_prc.scripts as s

    s.ShotReferenceReplace(
        **qsm_gnl_process.MayaCacheSubprocess.to_option_kwargs(option_opt.to_string())
    ).execute()


def motion_generate_fnc(option_opt):
    import qsm_general.process as qsm_gnl_process

    import lnx_maya_montage.scripts as s

    s.StlConvertionProcess(
        **qsm_gnl_process.MayaCacheSubprocess.to_option_kwargs(option_opt.to_string())
    ).execute()


def mocap_fbx_motion_generate_fnc(option_opt):
    import qsm_general.process as qsm_gnl_process

    import lnx_maya_montage.scripts as s

    s.MoCapDotFbxMotionGenerateProcess(
        **qsm_gnl_process.MayaCacheSubprocess.to_option_kwargs(option_opt.to_string())
    ).execute()
    

def mocap_fbx_motion_generate_auto_fnc(option_opt):
    import qsm_general.process as qsm_gnl_process

    import lnx_maya_montage.scripts as s

    s.MoCapDotFbxMotionGenerateAutoProcess(
        **qsm_gnl_process.MayaCacheSubprocess.to_option_kwargs(option_opt.to_string())
    ).execute()


def test_unicode(method, option_opt):
    pass


def test_progress(option_opt):
    import lxbasic.log as bsc_log

    import time

    tag = option_opt.get('tag')

    with bsc_log.LogProcessContext.create(
        maximum=5,
        label='test-1',
    ) as g_p:
        for i in range(5):

            if i == 3:
                if tag == 'error':
                    raise RuntimeError()

            time.sleep(2)
            g_p.do_update()

    with bsc_log.LogProcessContext.create(
        maximum=5,
        label='test-2',
    ) as g_p:
        for i in range(5):
            time.sleep(1)
            g_p.do_update()


def main(session):
    # noinspection PyUnresolvedReferences
    from maya import cmds
    cmds.stackTrace(state=1)

    option_opt = session.get_option_opt()
    method = option_opt.get('method')
    if method == 'skin-proxy-cache-generate':
        skin_proxy_generate_fnc(option_opt)
    elif method == 'dynamic-gpu-cache-generate':
        dynamic_gpu_generate_fnc(option_opt)
    elif method == 'unit-assembly-cache-generate':
        unit_assembly_cache_generate_fnc(option_opt)
    elif method == 'gpu-instance-cache-generate':
        gpu_instance_generate_fnc(option_opt)
    elif method == 'cfx-cloth-cache-generate':
        cfx_cloth_cache_generate_fnc(option_opt)
    elif method == 'playblast':
        playblast_fnc(option_opt)
    elif method == 'rig_validation':
        rig_validation_fnc(option_opt)
    elif method == 'scenery_validation':
        scenery_validation_fnc(option_opt)
    # new
    elif method == 'motion_generate':
        motion_generate_fnc(option_opt)
    elif method == 'mocap_fbx_motion_generate':
        mocap_fbx_motion_generate_fnc(option_opt)
    elif method == 'mocap_fbx_motion_generate_auto':
        mocap_fbx_motion_generate_auto_fnc(option_opt)
    #
    elif method == 'mesh_count_generate':
        mesh_count_generate_fnc(option_opt)
    elif method == 'snapshot_generate':
        snapshot_generate_fnc(option_opt)
    # new method for unit assembly generate
    elif method == 'unit_assembly_generate':
        unit_assembly_generate_fnc(option_opt)
    elif method == 'fx_proxy_rig_generate':
        fx_proxy_rig_generate_fnc(option_opt)
    #
    elif method == 'shot_replace_reference':
        shot_replace_reference_fnc(option_opt)
    # test
    elif method == 'test-unicode':
        test_unicode(method, option_opt)
    # test
    elif method == 'test-process':
        test_progress(option_opt)
    else:
        raise RuntimeError(
            sys.stderr.write(
                'method is not valid: {}.\n'.format(method)
            )
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
