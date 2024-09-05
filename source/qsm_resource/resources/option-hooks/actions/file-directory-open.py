# coding:utf-8


def main(session):
    import lxbasic.storage as bsc_storage

    hook_option_opt = session.option_opt

    file_path = hook_option_opt.get('file')
    if file_path:
        bsc_storage.StgFileOpt(
            file_path
        ).show_in_system()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
