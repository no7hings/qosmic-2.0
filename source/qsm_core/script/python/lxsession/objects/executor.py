# coding:utf-8
import lxbasic.deadline as bsc_deadline
# session
from .. import abstracts as ssn_abstracts


class HookExecutor(ssn_abstracts.AbsHookExecutor):
    SUBMITTER_CLS = bsc_deadline.DdlSubmiter

    def __init__(self, *args, **kwargs):
        super(HookExecutor, self).__init__(*args, **kwargs)


class RsvProjectHookExecutor(ssn_abstracts.AbsRsvProjectMethodHookExecutor):
    SUBMITTER_CLS = bsc_deadline.DdlSubmiterForRsvProject

    def __init__(self, *args, **kwargs):
        super(RsvProjectHookExecutor, self).__init__(*args, **kwargs)


class RsvTaskHookExecutor(ssn_abstracts.AbsRsvTaskMethodHookExecutor):
    SUBMITTER_CLS = bsc_deadline.DdlSubmiterForRsvTask

    def __init__(self, *args, **kwargs):
        super(RsvTaskHookExecutor, self).__init__(*args, **kwargs)
