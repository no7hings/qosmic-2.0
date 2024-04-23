# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxmaya.dcc.objects as mya_dcc_objects

    import qsm_prc_general.rsv.objects as gnl_rsv_objects

    import qsm_prc_maya.rsv.objects as mya_rsv_objects
    # noinspection PyUnresolvedReferences
    import maya.cmds as cmds
    cmds.stackTrace(state=1)

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')
    if any_scene_file_path is not None:
        maya_rsv_scene_properties = gnl_rsv_objects.RsvUtilityOpt.get_dcc_args(
            any_scene_file_path, application='maya'
        )
        if maya_rsv_scene_properties:
            # get scene src file path as current application
            maya_scene_file_path = maya_rsv_scene_properties.get('extra.file')
            if bsc_storage.StgFileMtd.get_is_exists(maya_scene_file_path) is True:
                # open file
                mya_dcc_objects.Scene.open_file(maya_scene_file_path)
                #
                with_proxy_xarc = hook_option_opt.get_as_boolean('with_proxy_xarc')
                if with_proxy_xarc is True:
                    mya_rsv_objects.RsvDccProxyHookOpt(
                        maya_rsv_scene_properties,
                        hook_option_opt
                    ).set_proxy_xarc_export()
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
