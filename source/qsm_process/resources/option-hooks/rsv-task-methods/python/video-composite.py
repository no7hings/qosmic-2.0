# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxresolver.core as rsv_core

    import qsm_prc_general.rsv.objects as gnl_rsv_objects

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if bsc_storage.StgFileMtd.get_is_exists(any_scene_file_path) is True:
            resolver = rsv_core.RsvBase.generate_root()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                with_video_mov = hook_option_opt.get('with_video_mov') or False
                if with_video_mov is True:
                    gnl_rsv_objects.RsvVedioComposite(
                        rsv_scene_properties,
                        hook_option_opt,
                    ).set_video_mov_composite()
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
