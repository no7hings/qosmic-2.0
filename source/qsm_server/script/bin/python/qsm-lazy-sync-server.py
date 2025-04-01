# coding:utf-8


# main server
def start_main_server():
    from qsm_lazy_sync_server.worker import _configure

    from qsm_lazy_sync_server.worker import server

    server.start(
        _configure.SyncServer.HOST, _configure.SyncServer.PORT,
        dbug=True,
    )


# backup server
def start_backup_server():
    from qsm_lazy_sync_server.worker import _configure

    from qsm_lazy_sync_server.worker import server

    server.start(
        _configure.SyncServer.HOST, _configure.SyncServer.PORT_BACKUP,
        dbug=True,
    )


if __name__ == '__main__':
    start_main_server()
