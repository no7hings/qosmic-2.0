# coding:utf-8


def main(session):
    import lxbasic.dcc.core as mya_dcc_core

    mya_dcc_core.SocketConnectForMaya.create_connection()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
