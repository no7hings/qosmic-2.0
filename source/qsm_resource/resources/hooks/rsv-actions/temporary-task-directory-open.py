# coding:utf-8

def main(session):
    import lxbasic.dcc.objects as bsc_dcc_objects

    dir_path = session.rsv_unit.get_result(
        version='latest'
    )
    if dir_path:
        bsc_dcc_objects.StgDirectory(dir_path).set_open()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
