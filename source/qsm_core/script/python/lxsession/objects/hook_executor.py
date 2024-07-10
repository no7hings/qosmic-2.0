# coding:utf-8
import lxbasic.deadline as bsc_deadline
# session
from .. import abstracts as ssn_abstracts


class HookExecutor(ssn_abstracts.AbsHookExecutor):
    DDL_JOB_SUBMITTER_CLS = bsc_deadline.DdlJobSubmiter

    def __init__(self, *args, **kwargs):
        super(HookExecutor, self).__init__(*args, **kwargs)


class HookExecutorForRsvProject(ssn_abstracts.AbsRsvProjectMethodHookExecutor):
    DDL_JOB_SUBMITTER_CLS = bsc_deadline.DdlJobSubmiterForRsvProject

    def __init__(self, *args, **kwargs):
        super(HookExecutorForRsvProject, self).__init__(*args, **kwargs)


class HookExecutorForRsvTask(ssn_abstracts.AbsRsvTaskMethodHookExecutor):
    DDL_JOB_SUBMITTER_CLS = bsc_deadline.DdlJobSubmiterForRsvTask

    def __init__(self, *args, **kwargs):
        super(HookExecutorForRsvTask, self).__init__(*args, **kwargs)
