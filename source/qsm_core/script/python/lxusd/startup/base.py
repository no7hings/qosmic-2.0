# coding:utf-8
import lxbasic.storage as bsc_storage

import lxgeneral.dcc.abstracts as gnl_dcc_abstracts


class UsdSetup(gnl_dcc_abstracts.AbsDccSetup):
    def __init__(self, root):
        super(UsdSetup, self).__init__(root)

    def set_run(self):
        self.add_bin_fnc(
            '{}/bin'.format(self._root)
        )
        self.add_libraries(
            '{}/lib'.format(self._root),
            '{}/lib64'.format(self._root)
        )
        self.add_pythons(
            '{}/lib/python'.format(self._root)
        )

    @classmethod
    def build_environ(cls):
        cls.add_environ_fnc(
            'PXR_AR_DEFAULT_SEARCH_PATH',
            bsc_storage.StgPathMapper.map_to_current('/l/prod')
        )
        cls.add_environ_fnc(
            'PXR_AR_DEFAULT_SEARCH_PATH',
            bsc_storage.StgPathMapper.map_to_current('/t/prod')
        )


class UsdArnoldSetup(gnl_dcc_abstracts.AbsDccSetup):
    def __init__(self, root):
        super(UsdArnoldSetup, self).__init__(root)

    def set_run(self):
        self.add_libraries(
            '{root}/lib', '{root}/bin'
        )
