# coding:utf-8


def main(session):
    import lxbasic.extra.methods as bsc_exr_methods

    hook_option_opt = session.option_opt

    file_path = hook_option_opt.get('file')
    if file_path:
        bsc_exr_methods.EtrRv.open_file(file_path)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
