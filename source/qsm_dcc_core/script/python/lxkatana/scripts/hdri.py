# coding:utf-8
import six

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# katana
from .. import core as ktn_core


class ScpHdriBuildForPaste(object):
    """
# coding:utf-8
import lxkatana

lxkatana.set_reload()

import lxkatana.scripts as ktn_scripts


ktn_scripts.ScpHdriBuildForPaste(
    'light_space__2B59M',
    'light variant',
    '/production/library/resource/all/hdri/mall_parking_lot_4k/v0001/hdri/acescg/tx/mall_parking_lot_4k.tx'
).accept()
    """
    def __init__(self, node_arg, scheme, hdri_path):
        if isinstance(node_arg, six.string_types):
            self._obj_opt = ktn_core.NGNodeOpt(node_arg)
        else:
            self._obj_opt = node_arg

        self._scheme = scheme
        self._hdri_path = hdri_path

    def accept(self):
        if self._scheme == 'light HDRI':
            file_opt = bsc_storage.StgFileOpt(self._hdri_path)

            name = file_opt.get_name_base()

            time_tag = bsc_core.TimeExtraMtd.generate_time_tag_36_(multiply=100)

            ktn_obj, is_create = ktn_core.NGNodeOpt._generate_node_create_args(
                '{}/hdri_light__{}__{}'.format(self._obj_opt.get_path(), name, time_tag),
                'UtilityLight_Wsp'
            )
            if is_create is True:
                hdri_opt = ktn_core.NGNodeOpt(ktn_obj)
                hdri_opt.set('parameters.setting.skydome_light.image', file_opt.get_path())

                ktn_core.GuiNodeGraphOpt.drop_nodes(
                    [ktn_obj]
                )
        elif self._scheme == 'light variant':
            file_opt = bsc_storage.StgFileOpt(self._hdri_path)

            name = file_opt.get_name_base()

            time_tag = bsc_core.TimeExtraMtd.generate_time_tag_36_(multiply=100)

            ktn_obj, is_create = ktn_core.NGNodeOpt._generate_node_create_args(
                '{}/hdri_light__{}__{}'.format(self._obj_opt.get_path(), name, time_tag),
                'UtilityLight_Wsp'
            )
            if is_create is True:
                hdri_opt = ktn_core.NGNodeOpt(ktn_obj)
                hdri_opt.set('parameters.setting.skydome_light.image', file_opt.get_path())

                variant_register_nodes = self._obj_opt.filter_children([('node_type', 'is', 'VariableSwitch'), ('user.type', 'is', 'VariantRegister_Wsp')])
                upstream_merge_nodes = self._obj_opt.filter_children([('node_type', 'is', 'Merge'), ('user.type', 'is', 'UpstreamMerge_Wsp')])
                if variant_register_nodes and upstream_merge_nodes:
                    from . import macro_for_wsp as ktn_scp_macro_for_wsp

                    variant_register_node = variant_register_nodes[0]
                    upstream_merge_node = upstream_merge_nodes[0]

                    ktn_scp_macro_for_wsp.ScpWspVariantRegister(
                        variant_register_node
                    ).register_one(name, hdri_opt)

                    hdri_opt.connect_input_from(
                        'join_upstream', (ktn_core.NGNodeOpt(upstream_merge_node).get_path(), 'out')
                    )

                    ktn_core.GuiNodeGraphOpt.drop_nodes(
                        [ktn_obj]
                    )