# coding:utf-8
import lxgeneral.fnc.abstracts as gnl_fnc_abstracts


class GeometryUsdImporter(gnl_fnc_abstracts.AbsFncOptionBase):
    OPTION = dict(
        file='',
        root='',
        hou_location='',
    )

    def __init__(self, option):
        super(GeometryUsdImporter, self).__init__(option)

    def set_run(self):
        pass
