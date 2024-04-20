# coding:utf-8


def main(session):
    import lxbasic.extra.methods as bsc_exr_methods
    #
    file_path = session.rsv_unit.get_result(
        version='latest',
        variants_extend=session.rsv_unit_extend_variants
    )
    #
    if file_path:
        bsc_exr_methods.EtrRv.open_file(file_path)


# noinspection PyUnresolvedReferences
main(session)
