# coding:utf-8


def main(session):
    import lxbasic.extra.methods as bsc_exr_methods
    #
    file_path = session.rsv_unit.get_result(
        version='latest'
    )
    #
    if file_path:
        bsc_exr_methods.EtrRv.open_file(file_path)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
