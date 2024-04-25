# coding:utf-8

def main(session):
    import lxgeneral.dcc.objects as gnl_dcc_objects

    dir_path = session.rsv_unit.get_result(
        version='latest'
    )
    if dir_path:
        gnl_dcc_objects.StgDirectory(dir_path).set_open()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
