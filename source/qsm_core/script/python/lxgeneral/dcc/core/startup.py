# coding:utf-8
from .. import abstracts as gnl_dcc_abstracts


class OcioSetup(gnl_dcc_abstracts.AbsDccSetup):
    def __init__(self, root):
        super(OcioSetup, self).__init__(root)

    def set_run(self):
        self.set_environ_fnc(
            'OCIO', '{}/config.ocio'.format(self._root)
        )