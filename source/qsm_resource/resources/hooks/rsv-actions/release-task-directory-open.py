# coding:utf-8

def main(session):
    import lxbasic.storage as bsc_storage

    directory_path = session.rsv_unit.get_result(
        version='latest'
    )
    if directory_path:
        bsc_storage.StgPathOpt(directory_path).open_in_system()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
