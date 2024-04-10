# coding:utf-8
import lxuniverse.objects as unv_objects

import lxcontent.core as ctt_core
# resolver
from .. import abstracts as rsv_abstracts

from ..objects import stack as rsv_obj_stack

from ..objects import app as rsv_obj_app


class RsvVersionKey(rsv_abstracts.AbsRsvVersionKey):
    def __init__(self, *args, **kwargs):
        super(RsvVersionKey, self).__init__(*args, **kwargs)


class RsvPattern(rsv_abstracts.AbsRsvPattern):
    def __init__(self, *args, **kwargs):
        super(RsvPattern, self).__init__(*args, **kwargs)


class RsvMatcher(rsv_abstracts.AbsRsvMatcher):
    PROPERTIES_CLS = ctt_core.Properties
    #
    RSV_PATTERN_CLS = RsvPattern
    #
    RSV_VERSION_KEY_CLS = RsvVersionKey

    def __init__(self, *args, **kwargs):
        super(RsvMatcher, self).__init__(*args, **kwargs)


class RsvUnit(rsv_abstracts.AbsRsvUnit):
    PATHSEP = '/'
    #
    PROPERTIES_CLS = ctt_core.Properties

    def __init__(self, *args, **kwargs):
        super(RsvUnit, self).__init__(*args, **kwargs)


class RsvResourceGroup(rsv_abstracts.AbsRsvResourceGroup):
    PATHSEP = '/'
    #
    PROPERTIES_CLS = ctt_core.Properties

    def __init__(self, *args, **kwargs):
        super(RsvResourceGroup, self).__init__(*args, **kwargs)


class RsvResource(rsv_abstracts.AbsRsvResource):
    PATHSEP = '/'
    #
    PROPERTIES_CLS = ctt_core.Properties

    def __init__(self, *args, **kwargs):
        super(RsvResource, self).__init__(*args, **kwargs)


class RsvStep(rsv_abstracts.AbsRsvStep):
    PATHSEP = '/'
    #
    PROPERTIES_CLS = ctt_core.Properties

    def __init__(self, *args, **kwargs):
        super(RsvStep, self).__init__(*args, **kwargs)


class RsvTask(rsv_abstracts.AbsRsvTask):
    PATHSEP = '/'
    #
    PROPERTIES_CLS = ctt_core.Properties

    def __init__(self, *args, **kwargs):
        super(RsvTask, self).__init__(*args, **kwargs)


class RsvTaskVersion(rsv_abstracts.AbsRsvTaskVersion):
    PATHSEP = '/'
    #
    PROPERTIES_CLS = ctt_core.Properties

    def __init__(self, *args, **kwargs):
        super(RsvTaskVersion, self).__init__(*args, **kwargs)


class RsvUnitVersion(rsv_abstracts.AbsRsvUnitVersion):
    PATHSEP = '/'
    #
    PROPERTIES_CLS = ctt_core.Properties

    def __init__(self, *args, **kwargs):
        super(RsvUnitVersion, self).__init__(*args, **kwargs)


class RsvProject(rsv_abstracts.AbsRsvProject):
    PATHSEP = '/'
    #
    PROPERTIES_CLS = ctt_core.Properties
    #
    RSV_MATCHER_CLS = RsvMatcher
    RSV_PATTERN_CLS = RsvPattern
    #
    RSV_OBJ_STACK_CLS = rsv_obj_stack.EntityStack
    #
    RSV_RESOURCE_GROUP_CLS = RsvResourceGroup
    RSV_RESOURCE_CLS = RsvResource
    RSV_STEP_CLS = RsvStep
    RSV_TASK_CLS = RsvTask
    RSV_TASK_VERSION_CLS = RsvTaskVersion
    #
    RSV_UNIT_CLS = RsvUnit
    RSV_UNIT_VERSION_CLS = RsvUnitVersion
    #
    RSV_APP_DEFAULT_CLS = rsv_obj_app.RsvAppDefault
    RSV_APP_NEW_CLS = rsv_obj_app.RsvAppNew

    def __init__(self, *args, **kwargs):
        super(RsvProject, self).__init__(*args, **kwargs)


class RsvRoot(rsv_abstracts.AbsRsvRoot):
    PATHSEP = '/'
    #
    OBJ_UNIVERSE_CLS = unv_objects.ObjUniverse
    #
    RSV_PROJECT_STACK_CLS = rsv_obj_stack.ProjectStack
    RSV_PROJECT_CLS = RsvProject

    RSV_VERSION_KEY_CLS = RsvVersionKey

    def __init__(self):
        super(RsvRoot, self).__init__()


if __name__ == '__main__':
    pass
