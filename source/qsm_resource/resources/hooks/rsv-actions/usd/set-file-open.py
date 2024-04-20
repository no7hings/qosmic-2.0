# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    file_path = session.rsv_unit.get_result(
        version='latest'
    )
    #
    if file_path:
        project = session.variants['project']
        #
        cmd = 'rez-env arnold_usd-6.1.0.1 arnold-6.1.0.1 aces pyside2 pgusd usd-20.11 -- usdview "{}"'.format(
            file_path
        )

        bsc_core.PrcBaseMtd.execute_with_result_use_thread(cmd)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
