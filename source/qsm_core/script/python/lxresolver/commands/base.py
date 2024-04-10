# coding:utf-8


# todo: old call, remove later, new call move to core
def get_resolver():
    from .. import core as rsv_core

    return rsv_core.RsvBase.generate_root()
