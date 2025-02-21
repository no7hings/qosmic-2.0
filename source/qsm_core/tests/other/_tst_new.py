# coding:utf-8
class Configure(object):
    INSTANCE = None
    initialized = False

    def __init__(self):
        if not self.initialized:
            print('AAA')
            self.initialized = True

    def __new__(cls, *args, **kwargs):
        if cls.INSTANCE is not None:
            return cls.INSTANCE

        instance = super(Configure, cls).__new__(cls)
        cls.INSTANCE = instance
        return instance

# 测试
a = Configure()  # 打印 AAA
b = Configure()  # 不打印 AAA
print(a is b)  # True
