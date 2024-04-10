# coding:utf-8
# universe
from .. import abstracts as unr_abstracts


# category
class CategoryStack(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(CategoryStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()


# type
class TypeStack(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(TypeStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()


# port channel
class PortChannelStack(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(PortChannelStack, self).__init__()

    def get_key(self, obj):
        return obj.name


# port element
class PortElementStack(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(PortElementStack, self).__init__()

    def get_key(self, obj):
        return obj.index


class PortQueryStack(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(PortQueryStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()


# port
class PrxPortStack(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(PrxPortStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()


# connection
class ObjConnectionStack(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(ObjConnectionStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()


class ObjBindStack(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(ObjBindStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()


# node type
class ObjCategoryStack(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(ObjCategoryStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()


# type
class ObjTypeStack(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(ObjTypeStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()


# obj
class ObjStack(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(ObjStack, self).__init__()

    def get_key(self, obj):
        return obj._get_stack_key_()


# obj
class ObjStackTest(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(ObjStackTest, self).__init__()

    def get_key(self, obj):
        return obj.get_path()
