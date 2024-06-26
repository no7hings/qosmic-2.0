# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    hook_option_opt = session.option_opt

    cmd = '/opt/rv/bin/rvio "{image_file}" -vv -overlay frameburn .4 1.0 30.0 -dlut "{lut_directory}" -o "{movie_file}" -comment "{user}" -outparams timecode={start_frame}'.format(
        **hook_option_opt.get_raw()
    )

    bsc_core.BscProcess.execute_with_result(
        cmd
    )

    user = hook_option_opt.get('user')

    file_path = hook_option_opt.get('movie_file')

    set_send_to_gugu(user, file_path)


def set_send_to_gugu(user, file_path):
    import urllib

    import lxbasic.storage as bsc_storage

    windows_file_path = bsc_storage.StgPathMapper.map_to_windows(file_path)

    linux_file_path = bsc_storage.StgPathMapper.map_to_linux(file_path)

    windows_cmd = '{} {}'.format('pgrv', windows_file_path)

    linux_cmd = '{} {}'.format('pgrv', linux_file_path)

    c = '{}::{}::{}'.format(
        'open movie',
        linux_cmd,
        windows_cmd
    )

    c = c.decode('utf-8')

    flag_dict = {
        'from': user,
        'to': user,
        'content': 'PG Render task is completed\nmovie is\n"{}"\n"{}'.format(
            windows_file_path, linux_file_path
        ),
        'command': c,
        'msg_type': 'command'
    }

    notify_url = 'http://cg-ark.papegames.com:61112/notify'
    flag = urllib.urlencode(flag_dict)
    url = '?'.join([notify_url, flag])

    urllib.urlopen(url)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
