# coding:utf-8

def main(session):
    import lxgeneral.dcc.objects as gnl_dcc_objects

    variants_extend = session.rsv_unit_extend_variants

    dir_path = session.rsv_unit.get_result(
        version='latest',
        variants_extend=variants_extend
    )
    if dir_path:
        gnl_dcc_objects.StgDirectory(dir_path).set_open()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
