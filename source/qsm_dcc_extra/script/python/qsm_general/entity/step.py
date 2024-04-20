# coding:utf-8
from . import base as _base


class Step(_base.AbsStep):
    def __init__(self, *args, **kwargs):
        super(Step, self).__init__(*args, **kwargs)


class StepQuery(_base.AbsStepQuery):
    StepClass = Step

    def __init__(self, *args, **kwargs):
        super(StepQuery, self).__init__(*args, **kwargs)
