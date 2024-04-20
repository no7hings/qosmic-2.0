# coding:utf-8
from random import choice

import lxbasic.core as bsc_core


o = bsc_core.RectLayoutOpt(
    [(0, 0, choice(range(1, 100)), choice(range(1, 100))) for i in range(100)]
)

# o.take_one_by_w_maximum()

o.center = 0, 0

o.next()


# while o.get_is_finished():
#
#     print rect
