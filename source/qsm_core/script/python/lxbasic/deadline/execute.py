# coding:utf-8
import lxresource as bsc_resource

import lxcontent.core as ctt_core

import lxbasic.log as bsc_log

from . import base as bsc_ddl_base


class AbsDdlSubmiter(object):
    CON = None
    CONFIGURE_FILE_PATH = None

    def __init__(self):
        self._configure = ctt_core.Content(value=self.CONFIGURE_FILE_PATH)
        #
        self._option = self._configure.get_as_content('option')
        #
        self._job_info = self._configure.get_as_content('output.info')
        self._job_plug = self._configure.get_as_content('output.plug')
        #
        self._result = None
        self._job_id = None

    def get_option(self):
        return self._option

    option = property(get_option)

    def set_option(self, **kwargs):
        for k in self._configure.get('option'):
            if k in kwargs:
                self._configure.set(
                    'option.{}'.format(k),
                    kwargs[k]
                )

    def set_option_extra(self, **kwargs):
        for k in self._configure.get('option.extra'):
            if k in kwargs:
                self._configure.set(
                    'option.extra.{}'.format(k),
                    kwargs[k]
                )

    #
    def get_job_info(self):
        return self._job_info

    job_info = property(get_job_info)

    def get_job_plug(self):
        return self._job_plug

    job_plug = property(get_job_plug)

    def set_job_info_extra(self, raw):
        if isinstance(raw, dict):
            content = ctt_core.Content(value=raw)
            for seq, k in enumerate(content.get_all_leaf_keys()):
                self.job_info.set(
                    'ExtraInfoKeyValue{}'.format(seq),
                    '{}={}'.format(k, content.get(k))
                )

    def set_job_submit(self):
        self._configure.do_flatten()
        info = self.job_info.value
        plug = self.job_plug.value
        return self.__set_job_submit_(info, plug)

    def __set_job_submit_(self, info, plug):
        bsc_log.Log.trace_method_result(
            'deadline-job submit', 'is started'
        )
        self._result = self.CON.Jobs.SubmitJob(info, plug)
        if isinstance(self._result, dict):
            if '_id' in self._result:
                self._job_id = self._result['_id']
                bsc_log.Log.trace_method_result(
                    'deadline-job submit', 'is completed, jon-id="{}"'.format(self._job_id)
                )
                return self._job_id
        #
        bsc_log.Log.trace_method_error(
            'deadline-job submit', 'is failed, {}'.format(self._result)
        )
        return None

    def get_job_is_submit(self):
        return self.get_job_id() is not None

    def get_job_group_name(self):
        return self.job_info.get('BatchName')

    def get_job_name(self):
        return self.job_info.get('Name')

    def get_job_result(self):
        return self._result

    def get_job_id(self):
        _ = self.get_job_result()
        if isinstance(_, dict):
            if '_id' in _:
                return _['_id']

    def __str__(self):
        return self._configure.get_str_as_yaml_style()


class DdlSubmiter(AbsDdlSubmiter):
    CON = bsc_ddl_base.DdlBase.generate_connection()
    CONFIGURE_FILE_PATH = bsc_resource.RscExtendConfigure.get_yaml('session/deadline/submiter')

    def __init__(self, *args, **kwargs):
        super(DdlSubmiter, self).__init__(*args, **kwargs)


class DdlSubmiterForRsvProject(AbsDdlSubmiter):
    CON = bsc_ddl_base.DdlBase.generate_connection()
    CONFIGURE_FILE_PATH = bsc_resource.RscExtendConfigure.get_yaml('session/deadline/rsv-project-submiter')

    def __init__(self, *args, **kwargs):
        super(DdlSubmiterForRsvProject, self).__init__(*args, **kwargs)


class DdlSubmiterForRsvTask(AbsDdlSubmiter):
    CON = bsc_ddl_base.DdlBase.generate_connection()
    CONFIGURE_FILE_PATH = bsc_resource.RscExtendConfigure.get_yaml('session/deadline/rsv-task-submiter')

    def __init__(self, *args, **kwargs):
        super(DdlSubmiterForRsvTask, self).__init__(*args, **kwargs)
