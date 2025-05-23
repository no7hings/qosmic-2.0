# coding:utf-8
import lxbasic.resource as bsc_resource

import lxbasic.core as bsc_core

import qsm_lazy_sync.client as qsm_snc_client


class SyncFnc:

    @staticmethod
    def sync_version_directory(version_dir_path):
        studio = Sync().studio.get_current()

        symlink_kwargs = Sync().generate_sync_kwargs(
            studio, version_dir_path
        )
        if symlink_kwargs:
            return qsm_snc_client.TaskClient.new_task(
                'sync', **symlink_kwargs
            )


class SyncFactory:
    @staticmethod
    def run(fnc):
        def wrapper(*args, **kwargs):
            task_session = fnc(*args, **kwargs)
            version_dir_path = task_session.get_file_or_dir_for('asset-release-version-dir')

            # sync version folder
            SyncFnc.sync_version_directory(version_dir_path)

            # fixme: cannot use for production, server not support.
            # link current version to no version
            no_version_dir_path = task_session.get_file_or_dir_for('asset-release-no_version-dir')
            # c.TaskClient.new_task('symlink', source=version_dir_path, target=no_version_dir_path, replace=True)
        return wrapper


class Sync(object):
    INSTANCE = None

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if cls.INSTANCE is not None:
            return cls.INSTANCE

        self = super(Sync, cls).__new__(cls)
        self._configure = bsc_resource.BscConfigure.get_as_content('lazy/sync')
        cls.INSTANCE = self
        return self

    @property
    def configure(self):
        return self._configure

    @property
    def studio(self):
        return _Studio()

    @property
    def driver_map(self):
        return _DriverMap()

    def generate_sync_kwargs(self, studio, path):
        target_studios = self._configure.get('studio_targets_map.{}'.format(studio))
        kwargs = dict(
            source=self.driver_map.convert_path(studio, path),
            targets=[],
            # todo: maybe use replace mode?
            replace=True,
        )
        if target_studios:
            for i_studio in target_studios:
                i_target = self.driver_map.convert_path(i_studio, path)
                if i_target:
                    kwargs['targets'].append(i_target)
        return kwargs

    @classmethod
    def sever_is_available(cls):
        import qsm_lazy_sync

        flag = qsm_lazy_sync.TaskClient.check_status()
        if flag is True:
            return True

        import lxgui.core as gui_core

        if gui_core.GuiUtil.language_is_chs():
            gui_core.GuiApplication.exec_message_dialog(
                '无法连接到同步服务器，请联系TD。',
                title='请求同步服务',
                size=(320, 120),
                status='error',
            )
        else:
            gui_core.GuiApplication.exec_message_dialog(
                'Unable to connect to the sync server, please contact TD.',
                title='Sync Server',
                size=(320, 120),
                status='warning',
            )
        return False


class _Studio(object):
    """
    support windows only.
    """
    INSTANCE = None

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if cls.INSTANCE is not None:
            return cls.INSTANCE

        self = super(_Studio, cls).__new__(cls)
        self._map = Sync().configure.get('studio')
        self._map_reverse = {v: k for k, v in self._map.items()}
        cls.INSTANCE = self
        return self

    def get_current(self):
        driver_source = bsc_core.BscStorage.get_driver_source(
            'Y:'
        )
        return self._map_reverse.get(driver_source, 'UNKNOWN')


class _DriverMap(object):
    INSTANCE = None

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if cls.INSTANCE is not None:
            return cls.INSTANCE

        self = super(_DriverMap, cls).__new__(cls)
        self._map = Sync().configure.get('driver_map')
        cls.INSTANCE = self
        return self

    def convert_path(self, studio, path):
        path = bsc_core.ensure_unicode(path)
        driver_letter = path[:2]
        if not driver_letter.endswith(':'):
            raise RuntimeError()

        map_s = self._map.get(studio)
        path_source = map_s[driver_letter[0]]
        if path_source:
            return path_source+path[2:]
