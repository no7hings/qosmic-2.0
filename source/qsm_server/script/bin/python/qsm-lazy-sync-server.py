# coding:utf-8


def start_server():
    from qsm_lazy_sync_server.worker import _configure

    from qsm_lazy_sync_server.worker import server

    server.start(
        _configure.SyncServer.HOST, _configure.SyncServer.PORT,
        dbug=True,
    )


if __name__ == '__main__':
    start_server()
