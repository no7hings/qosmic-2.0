# coding:utf-8
from .. import abstracts as ldr_gui_abstracts


class PnlLoaderForRsvTask(ldr_gui_abstracts.AbsPnlLoaderForRsvTask):
    def __init__(self, session, *args, **kwargs):
        super(PnlLoaderForRsvTask, self).__init__(session, *args, **kwargs)
