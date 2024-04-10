# coding:utf-8
import lxuniverse.abstracts as unr_abstracts


# <stack-project>
class ProjectStack(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(ProjectStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()


# <stack-task>
class EntityStack(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(EntityStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()


# <stack-task>
class TaskStack(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(TaskStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()
