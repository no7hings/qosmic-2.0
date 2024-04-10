# coding:utf-8
import lxcontent.core as ctt_core

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import threading

import json

from . import base as bsc_ddl_base


class DdlContent(object):
    def __init__(self, obj, index, raw):
        self._obj = obj
        self._index = index
        self._raw = raw

    @property
    def index(self):
        return self._index

    @property
    def raw(self):
        return self._raw

    def get_stouts(self):
        return bsc_ddl_base.DdlLog(self._raw).get_stouts()

    def __str__(self):
        return '{}(id="{}", index={})'.format(
            self.__class__.__name__,
            self._obj.id, self._index
        )


class AbsDdlObj(object):
    DDL_PROPERTIES_CLS = None
    DDL_PROPERTY_CLS = None
    #
    DDL_CONTENT_CLS = None

    CON = None

    def __init__(self, raw):
        self._ddl_properties = self.DDL_PROPERTIES_CLS(self, raw)

    @property
    def properties(self):
        return self._ddl_properties

    def get_property(self, key):
        return self.DDL_PROPERTY_CLS(self._ddl_properties, key)


class DdlLogQuery(AbsDdlObj):
    DDL_PROPERTIES_CLS = ctt_core.Properties
    DDL_PROPERTY_CLS = ctt_core.Property

    CON = bsc_ddl_base.DdlBase.generate_connection()

    def __init__(self, obj, index, raw):
        self._obj = obj
        self._index = index
        super(DdlLogQuery, self).__init__(raw)

    @property
    def index(self):
        return self._index

    def __str__(self):
        return '{}(id="{}", index={})'.format(
            self.__class__.__name__,
            self._obj.id, self._index
        )


class DdlTaskQuery(AbsDdlObj):
    DDL_PROPERTIES_CLS = ctt_core.Properties
    DDL_PROPERTY_CLS = ctt_core.Property
    #
    DDL_CONTENT_CLS = DdlContent
    DDL_LOG_CLS = DdlLogQuery

    CON = bsc_ddl_base.DdlBase.generate_connection()

    def __init__(self, job, index, raw):
        self._job = job
        self._job_id = job.id
        self._task_index = index
        self._task_id = '{}_{}'.format(self._job.id, self._task_index)
        super(DdlTaskQuery, self).__init__(raw)

    @property
    def index(self):
        return self._task_index

    @property
    def job(self):
        return self._job

    @property
    def id(self):
        return self._task_id

    def get_contents(self):
        lis = []
        _ = self.CON.Tasks.connectionProperties.__get__(
            "/api/taskreports?JobID={}&TaskID={}&Data=allcontents".format(self._job_id, self._task_index)
        )
        raws = _
        if raws:
            for id_, raw in enumerate(raws):
                obj = self.DDL_CONTENT_CLS(self, id_, raw)
                lis.append(obj)
        return lis

    def get_logs(self):
        lis = []
        _ = self.CON.Tasks.connectionProperties.__get__(
            "/api/taskreports?JobID={}&TaskID={}&Data=log".format(self._job.id, self._task_index)
        )
        raws = _
        if raws:
            for id_, raw in enumerate(raws):
                obj = self.DDL_LOG_CLS(self, id_, raw)
                lis.append(obj)
        return lis

    def set_requeue(self):
        return self.CON.Tasks.connectionProperties.__put__(
            "/api/tasks", json.dumps({"Command": "requeue", "JobID": self.job.id, "TaskList": [self._task_index]})
        )

    def get_status(self):
        return self.get('Stat')

    def get_progress(self):
        return self.get('Prog')

    def get(self, key):
        _ = self.CON.Tasks.connectionProperties.__get__(
            "/api/tasks?JobID={}&TaskID={}".format(self._job_id, self._task_index)
        )
        if not _:
            raise RuntimeError('ddl-task-id:="{}" is Non-exists'.format(self._job_id))
        return _[key]

    def __str__(self):
        return '{}(id={})'.format(
            self.__class__.__name__,
            self.id
        )

    def __repr__(self):
        return self.__str__()


class DdlJobQuery(AbsDdlObj):
    DDL_PROPERTIES_CLS = ctt_core.Properties
    DDL_PROPERTY_CLS = ctt_core.Property
    #
    DDL_CONTENT_CLS = DdlContent
    DDL_LOG_CLS = DdlLogQuery
    #
    TASK_CLS = DdlTaskQuery

    CON = bsc_ddl_base.DdlBase.generate_connection()

    def __init__(self, job_id):
        self._job_id = job_id
        _ = self.CON.Tasks.connectionProperties.__get__(
            "/api/jobs?JobID={}".format(job_id)
        )
        if not _:
            raise RuntimeError('ddl-task-id:="{}" is Non-exists'.format(self._job_id))
        #
        super(DdlJobQuery, self).__init__(_[0])

    def get_id(self):
        return self._job_id

    id = property(get_id)

    # noinspection PyUnusedLocal
    def get_tasks(self, task_indices=None):
        lis = []
        _ = self.CON.Tasks.connectionProperties.__get__(
            "/api/tasks?JobID={}".format(self._job_id)
        )
        #
        if isinstance(_, dict) is False:
            raise RuntimeError('ddl-task-id:="{}" is Non-exists'.format(self._job_id))
        #
        tasks_raw = _['Tasks']
        for task_index, task_raw in enumerate(tasks_raw):
            ddl_task = self.TASK_CLS(self, task_index, task_raw)
            lis.append(ddl_task)
        return lis

    def get_contents(self):
        lis = []
        _ = self.CON.Tasks.connectionProperties.__get__(
            "/api/jobreports?JobID={}&Data=allcontents".format(self._job_id)
        )
        raws = _
        if raws:
            for id_, raw in enumerate(raws):
                obj = self.DDL_CONTENT_CLS(self, id_, raw)
                lis.append(obj)
        return lis

    def get_logs(self):
        lis = []
        _ = self.CON.Tasks.connectionProperties.__get__(
            "/api/jobreports?JobID={}&Data=log".format(self._job_id)
        )
        raws = _
        if raws:
            for id_, raw in enumerate(raws):
                obj = self.DDL_CONTENT_CLS(self, id_, raw)
                lis.append(obj)
        return lis

    def get_status(self):
        return self.get('Stat')

    def get_name(self):
        return self.properties.get('Props.Name')

    def get(self, key):
        _ = self.CON.Tasks.connectionProperties.__get__(
            "/api/jobs?JobID={}".format(self._job_id)
        )
        if not _:
            raise RuntimeError('ddl-task-id:="{}" is Non-exists'.format(self._job_id))
        return _[0][key]

    def set_requeue(self, task_indices=None):
        return [i.set_requeue() for i in self.get_tasks(task_indices)]

    def __str__(self):
        return '{}(id="{}")'.format(
            self.__class__.__name__,
            self.id
        )

    def __repr__(self):
        return self.__str__()


class DdlSignalThread(threading.Thread):
    THREAD_MAXIMUM = threading.Semaphore(1024)

    def __init__(self, target, args, kwargs):
        threading.Thread.__init__(self)
        self._fnc = target
        self._args = args
        self._kwargs = kwargs

    def run(self):
        DdlSignalThread.THREAD_MAXIMUM.acquire()
        self._fnc(*self._args, **self._kwargs)
        DdlSignalThread.THREAD_MAXIMUM.release()


class DdlSignal(object):
    # noinspection PyUnusedLocal
    def __init__(self, *args, **kwargs):
        self._fncs = []
        self.__is_active = True

    def stop(self):
        self.__is_active = False

    def connect_to(self, method):
        self._fncs.append(method)

    def send_emit(self, *args, **kwargs):
        if self.__is_active is True:
            if self._fncs:
                ts = [DdlSignalThread(target=i_method, args=args, kwargs=kwargs) for i_method in self._fncs]
                for t in ts:
                    t.start()
                for t in ts:
                    t.join()


class DdlJobMonitor(object):
    Status = bsc_core.BscStatus
    # Unknown = 0
    # Active = 1
    # Suspended = 2
    # Completed = 3
    # Failed = 4
    # Pending = 6
    JOB_STATUS = [
        Status.Unknown,
        Status.Started,
        Status.Suspended,
        Status.Completed,
        Status.Failed,
        Status.Unknown,
        Status.Waiting,
    ]
    # Unknown = 1
    # Queued = 2
    # Suspended = 3
    # Rendering = 4
    # Completed = 5
    # Failed = 6
    # 7
    # Pending = 8
    TASK_STATUS = [
        Status.Unknown,
        Status.Unknown,
        Status.Waiting,
        Status.Suspended,
        Status.Running,
        Status.Completed,
        Status.Failed,
        Status.Unknown,
        Status.Waiting
    ]

    #
    def __init__(self, job_id):
        self._job_query = DdlJobQuery(job_id)
        self._job_id = self._job_query.get_id()
        self._job_name = self._job_query.get_name()
        self._task_queries = self._job_query.get_tasks()

        self._timestamp_start = 0

        self.__is_active = True

        c = len(self._task_queries)
        self._job_status = self.Status.Started
        self._task_statuses = [self.Status.Started]*c
        self._task_progress = ['0 %']*c

        self.__timer = None
        self._timer_interval = 1

        self.running = DdlSignal(int)
        self.job_status_changed = DdlSignal(int)
        self.job_finished = DdlSignal(int)
        self.task_status_changed_at = DdlSignal(int, int)
        self.task_progress_changed_at = DdlSignal(int, str)
        self.task_finished_at = DdlSignal(int, int)
        self.logging = DdlSignal(str)

    def __set_loop_running_(self):
        if self.__is_active is True:
            # job
            pre_job_status = self._job_status
            self._job_status = self.JOB_STATUS[self._job_query.get_status()]
            if pre_job_status != self._job_status:
                self.__set_job_status_changed_(self._job_status)
            # task
            for index, i_task_query in enumerate(self._task_queries):
                # progress
                i_task_progress_pre = self._task_progress[index]
                i_task_progress = i_task_query.get_progress()
                if i_task_progress != i_task_progress_pre:
                    self._task_progress[index] = i_task_progress
                    self.__set_task_progress_at_(index, i_task_progress)
                # status
                i_task_status_pre = self._task_statuses[index]
                i_task_status = self.TASK_STATUS[i_task_query.get_status()]
                if i_task_status != i_task_status_pre:
                    self._task_statuses[index] = i_task_status
                    self.__set_task_status_changed_at_(index, i_task_status)
                    if i_task_status in [
                        self.Status.Completed,
                        self.Status.Failed,
                    ]:
                        self.__set_task_finished_at_(index, i_task_status)
            # check is finished
            if self._job_status not in [
                self.Status.Completed,
                self.Status.Failed,
            ]:
                self.__set_running_()
            else:
                self.__set_job_finished_(self._job_status)

    def __set_running_(self):
        self.__timer = threading.Timer(self._timer_interval, self.__set_loop_running_)
        self.__timer.setDaemon(True)
        self.__timer.start()

    def __set_logging_(self, text):
        result = bsc_log.Log.get_result(text)
        self.logging.send_emit(
            result
        )
        print result

    def __set_job_status_changed_(self, status):
        if self.__is_active is True:
            self.job_status_changed.send_emit(status)
            self.__set_logging_(u'job status is change to "{}"'.format(str(status)))

    def __set_task_status_changed_at_(self, index, status):
        if self.__is_active is True:
            self.task_status_changed_at.send_emit(index, status)
            self.__set_logging_(u'task {} status is change to "{}"'.format(index, str(status)))

    def __set_task_progress_at_(self, index, progress):
        if self.__is_active is True:
            self.task_progress_changed_at.send_emit(index, progress)
            self.__set_logging_(u'task {} progress is changed to "{}"'.format(index, str(progress)))

    def __set_job_finished_(self, status):
        self.__is_active = False
        self.job_finished.send_emit(status)
        self.__set_logging_(u'job is finished')

    def __set_task_finished_at_(self, index, status):
        if self.__is_active is True:
            self.task_finished_at.send_emit(index, status)
            self.__set_logging_(u'task {} is finished'.format(index))

    def get_task_count(self):
        return len(self._task_queries)

    def get_task_statuses(self):
        return self._task_statuses

    def get_job_status(self):
        return self._job_status

    def set_start(self):
        self.__set_logging_(u'job id is "{}"'.format(self._job_id))
        self.__set_logging_(u'job is started')
        #
        self.__set_running_()

    def set_stop(self):
        if self.__is_active is True:
            self.__set_logging_(u'job is stopped')
            #
            if self.__timer is not None:
                self.__timer.cancel()
            #
            self.__is_active = False
            #
            self.running.stop()
            self.job_status_changed.stop()
            self.job_finished.stop()
            self.task_status_changed_at.stop()
            self.task_progress_changed_at.stop()
            self.task_finished_at.stop()
            self.logging.stop()
