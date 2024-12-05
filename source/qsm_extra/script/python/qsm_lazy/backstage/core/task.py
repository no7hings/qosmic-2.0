# coding:utf-8
import os

import lxbasic.content as bsc_content

import lxbasic.core as bsc_core

import lxbasic.web as bsc_web

import lxbasic.storage as bsc_storage

import qsm_lazy.backstage.worker as lzy_bks_worker

from . import base as _base


class Task(_base.AbsEntity):
    class PropertyKeys(object):
        ID = 'id'
        Group = 'group'
        Name = 'name'
        Time = 'time'
        UtcTime = 'utc_time'

        HostName = 'host_name'
        UserName = 'user_name'

        CmdScript = 'cmd_script'

    class ProcessKeys(object):
        Status = 'status'
        SubmitTime = 'submit_time'
        StartTime = 'start_time'
        FinishTime = 'finish_time'

        Progress = 'progress'

        Priority = 'priority'
        CompletedNotice = 'completed_notice'

    Status = bsc_core.BasProcessStatus

    def __init__(self, entities_cache, entity_id):
        super(Task, self).__init__(entities_cache, entity_id)
        self._log_location = '{}/entity.log'.format(
            self._location
        )

        self._thread = None

    def __str__(self):
        return '{}(id="{}")'.format(
            self.__class__.__name__,
            self._entity_id
        )

    def __repr__(self):
        return self.__str__()

    @classmethod
    def create(cls, entities_cache, entity_id, entity_index, **kwargs):
        location = '{}/{}.entity'.format(
            entities_cache.location, entity_id
        )
        json_location = '{}/entity.json'.format(
            location
        )
        time_ = _base.Util.get_time()
        if os.path.isfile(json_location) is False:
            properties = dict(
                id=entity_id,
                index=entity_index,
                #
                time=_base.Util.get_time(),
                utc_time=_base.Util.get_utc_time(),
                #
                host=_base.Util.get_host_name(),
                user=_base.Util.get_user_name(),
            )
            properties.update(**kwargs)
            bsc_content.ContentFile(
                json_location
            ).write(
                {
                    'properties': properties,
                    'process': {
                        cls.ProcessKeys.Status: int(bsc_core.BasProcessStatus.Waiting),
                        cls.ProcessKeys.SubmitTime: time_,
                        cls.ProcessKeys.StartTime: '',
                        cls.ProcessKeys.FinishTime: '',
                        cls.ProcessKeys.Priority: 50,
                    }
                }

            )
        return cls(entities_cache, entity_id)

    def set_completed_notice(self, options):
        self._json_content.set(
            'properties.completed_notice', options
        )
        self.accept()

    def get_completed_notice(self):
        return self._json_content.get(
            'properties.completed_notice'
        )

    def get_status(self):
        return self._json_content.get('process.status')

    def get_progress(self):
        return self._json_content.get('process.progress')

    def get_start_time(self):
        return self._json_content.get('process.start_time')

    def get_finish_time(self):
        return self._json_content.get('process.finish_time')

    def set_status(self, status):
        self._json_content.set('process.status', int(status))
        self.accept()

    def update_by_start(self):
        self._json_content.set('process.start_time', _base.Util.get_time())
        self._json_content.set('process.progress', 0)
        self.accept()

    def update_by_finish(self):
        self._json_content.set('process.finish_time', _base.Util.get_time())
        self._json_content.set('process.progress', 100)
        self.accept()

    def accept(self):
        self._json_content.save()

    def save_process_log(self, text):
        if isinstance(text, list):
            text = '\n'.join(text)

        text = text.replace('\n\n', '\n')

        bsc_storage.StgFileOpt(
            self._log_location
        ).set_write(text)

    def read_result_log(self):
        if bsc_storage.StgPath.get_is_file(
            self._log_location
        ):
            return bsc_storage.StgFileOpt(self._log_location).set_read()

    def save_exception_log(self, text):
        pass

    def do_wait_for_start(self):

        def on_status_changed_(task_, status_):
            task_.set_status(status_)

        def on_started_(task_):
            task_.update_by_start()

        def on_completed_(task_, results_):
            _completed_notice = task_.get_completed_notice()
            if _completed_notice:
                # noinspection PyBroadException
                try:
                    skt = bsc_web.WebSocket(
                        lzy_bks_worker.NoticeWebServerBase.HOST, lzy_bks_worker.NoticeWebServerBase.PORT
                    )
                    if skt.connect() is True:
                        skt.send(_completed_notice)
                except Exception:
                    bsc_core.BscException.print_stack()

        def on_finished_(task_, status_, results_):
            task_.update_by_finish()
            task_.save_process_log(results_)

        cmd_script = self._json_content.get('process.cmd_script')
        self._thread = bsc_core.TrdCommandPool.generate(cmd_script, self)
        self._thread.status_changed.connect_to(on_status_changed_)
        self._thread.started.connect_to(on_started_)
        self._thread.completed.connect_to(on_completed_)
        self._thread.finished.connect_to(on_finished_)

        self._thread.do_wait_for_start()

    def get_thread(self):
        return self._thread


class TasksCacheOpt(_base.AbsEntitiesCacheOpt):
    ENTITY_CLS = Task

    def __init__(self, entity_pool):
        super(TasksCacheOpt, self).__init__(entity_pool)
