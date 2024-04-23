# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    hook_option_opt = session.option_opt

    cmd = '/opt/rv/bin/rvio "{image_file}" -vv -overlay frameburn .4 1.0 30.0 -dlut "{lut_directory}" -o "{video_file}" -comment "{user}" -outparams timecode={start_frame}'.format(
        **hook_option_opt.get_raw()
    )

    bsc_core.PrcBaseMtd.execute_with_result(
        cmd
    )

    user = hook_option_opt.get('user')

    file_path = hook_option_opt.get('video_file')


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
