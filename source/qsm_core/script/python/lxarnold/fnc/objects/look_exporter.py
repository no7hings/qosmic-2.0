# coding:utf-8
from lxusd.core.wrap import *

import lxbasic.fnc.abstracts as bsc_fnc_abstracts

import lxusd.core as usd_core
# arnold
from ...dcc import objects as and_dcc_objects


class LookPropertiesUsdExporter(bsc_fnc_abstracts.AbsFncOptionBase):
    OPTION = dict(
        file='',
        root='',
        location='',
        ass_file=None,
        ignore_default=False
    )

    def __init__(self, option=None):
        super(LookPropertiesUsdExporter, self).__init__(option)

        self._usd_stage = Usd.Stage.CreateInMemory()
        self._usd_stage_opt = usd_core.UsdStageOpt(self._usd_stage)
        self._usd_stage_opt.set_root_create(self.get('root'), override=True)

    def set_run(self):
        ass_file_path = self.get('ass_file')
        ignore_default = self.get('ignore_default')
        location = self.get('location')

        scene = and_dcc_objects.Scene()
        scene.load_from_dot_ass(
            ass_file_path,
            path_lstrip='/root/world/geo'
        )
        universe = scene.universe
        #
        dcc_location = universe.get_obj(location)
        if dcc_location:
            dcc_objs = dcc_location.get_descendants()
            for j_dcc_obj in dcc_objs:
                i_usd_prim = self._usd_stage_opt.set_obj_create_as_override(j_dcc_obj.path)
                if j_dcc_obj.type_name in ['mesh', 'xgen_description']:
                    i_usd_geometry_opt = usd_core.UsdGeometryOpt(i_usd_prim)
                    for j_dcc_port in j_dcc_obj.get_ports():
                        if j_dcc_port.name == 'material':
                            pass
                        else:
                            # ignore value changed
                            if ignore_default is True:
                                if j_dcc_port.get_is_value_changed() is False:
                                    continue
                            #
                            if j_dcc_port.get_is_element() is False and j_dcc_port.get_is_channel() is False:
                                j_port_path = 'arnold:{}'.format(j_dcc_port.name)
                                i_usd_geometry_opt.create_customize_port(
                                    j_port_path, j_dcc_port.type, j_dcc_port.get()
                                )
        #
        self._usd_stage_opt.do_flatten()
        self._usd_stage_opt.export_to(
            self.get('file')
        )
