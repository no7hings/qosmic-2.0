# coding:utf-8


class Sample(object):
    def __enter__(self):
        print "in __enter__"
        return "Foo"
    def __exit__(self, exc_type, exc_val, exc_tb):
        print "in __exit__"


def get_sample():
    return Sample()


with get_sample() as sample:
    print "Sample: ", sample
