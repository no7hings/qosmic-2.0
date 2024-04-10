# coding:utf-8
from .. import abstracts as grh_gui_abstracts


class PnlRezGraph(grh_gui_abstracts.AbsRezGraph):
    OPTION_HOOK_KEY = 'desktop-tools/rez-graph'

    def __init__(self, hook_option=None, *args, **kwargs):
        super(PnlRezGraph, self).__init__(hook_option, *args, **kwargs)
