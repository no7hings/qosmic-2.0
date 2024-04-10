# coding:utf-8
# noinspection PyUnresolvedReferences
import hou

import os

import glob

import parse


build_script = '''
kwargs["node"].hdaModule().set_build(kwargs)
'''


class Command(object):
    FMT_ABC_OPT = '/obj'
    FMT_SUBNET_DCC_PATH = '{root}/{pck_name}_pck'
    FMT_GEO_DCC_PATH = '{asset_name}'
    FMT_MERGE_DCC_PATH = '{asset_name}/{asset_name}'
    FMT_ALEMBIC_DCC_PATH = '{asset_name}/{asset_name}_{asset_index}'
    FMT_MTX_OPT = '/out'
    def __init__(self, kwargs):
        self._hou_obj = kwargs['node']
        self._subnet_dcc_path = '{}/{}_pck'.format(self._hou_obj.parent().path(), self._hou_obj.name())

    def set_build(self):
        self._set_raw_update_()
        self._set_obj_clear_()
        self._create_obj_()

    def _set_raw_update_(self):
        subnet_dcc_path = self._subnet_dcc_path
        file_path = self._hou_obj.parm('file_path').eval()
        self._build_dict = {}
        if os.path.isdir(file_path):
            abc_file_paths = glob.glob('{}/*'.format(file_path))
            for abc_file_path in abc_file_paths:
                file_name = os.path.basename(abc_file_path)
                p_format = '{asset_name}__{asset_index}.abc'
                p = parse.parse(p_format, file_name)
                if p:
                    format_dict = {}
                    extra = p.named
                    format_dict.update(extra)
                    format_dict['root'] = self._hou_obj.parent().path()
                    format_dict['pck_name'] = self._hou_obj.name()
                    #
                    asset_name, asset_index = format_dict.get('asset_name'), format_dict.get('asset_index')
                    #
                    geo_dcc_path = '{}/{}'.format(subnet_dcc_path, self.FMT_GEO_DCC_PATH.format(**format_dict))
                    merge_dcc_path = '{}/{}'.format(subnet_dcc_path, self.FMT_MERGE_DCC_PATH.format(**format_dict))
                    alembic_dcc_path = '{}/{}'.format(subnet_dcc_path, self.FMT_ALEMBIC_DCC_PATH.format(**format_dict))
                    self._build_dict.setdefault(
                        asset_name, []
                    ).append(
                        (geo_dcc_path, merge_dcc_path, alembic_dcc_path, abc_file_path)
                    )
        else:
            hou.ui.displayMessage(
                u'''error: "{}" is Non-exists'''.format(file_path)
            )

    def _set_obj_clear_(self):
        input_hou_objs = self._hou_obj.outputs()
        for i in input_hou_objs:
            i.destroy()

    def _create_obj_(self):
        root_hou_obj = self._hou_obj.parent()
        display = self._hou_obj.parm('alembic_display').eval()
        if self._build_dict:
            subnet_hou_obj = hou.node(self._subnet_dcc_path)
            if subnet_hou_obj is None:
                subnet_dcc_name = self._subnet_dcc_path.split('/')[-1]
                subnet_hou_obj = root_hou_obj.createNode('subnet', subnet_dcc_name)
                subnet_hou_obj.moveToGoodPosition()
                #
                subnet_hou_obj.setInput(0, self._hou_obj)
            #
            for k, v in self._build_dict.items():
                for seq, i in enumerate(v):
                    geo_dcc_path, merge_dcc_path, alembic_dcc_path, abc_file_path = i

                    geo_hou_obj = hou.node(geo_dcc_path)
                    if geo_hou_obj is None:
                        geo_dcc_name = geo_dcc_path.split('/')[-1]
                        geo_hou_obj = subnet_hou_obj.createNode('geo', geo_dcc_name)
                        geo_hou_obj.moveToGoodPosition()
                        #
                        geo_hou_obj.setInput(0, subnet_hou_obj.indirectInputs()[0])
                    #
                    merge_hou_obj = hou.node(merge_dcc_path)
                    if merge_hou_obj is None:
                        merge_dcc_name = merge_dcc_path.split('/')[-1]
                        merge_hou_obj = geo_hou_obj.createNode('merge', merge_dcc_name)
                        merge_hou_obj.moveToGoodPosition()
                    #
                    alembic_hou_obj = hou.node(alembic_dcc_path)
                    if alembic_hou_obj is None:
                        alembic_dcc_name = alembic_dcc_path.split('/')[-1]
                        alembic_hou_obj = geo_hou_obj.createNode('alembic', alembic_dcc_name)
                        alembic_hou_obj.moveToGoodPosition()
                        #
                        alembic_hou_obj.parm('fileName').set(abc_file_path)
                        alembic_hou_obj.parm('viewportlod').set(display)
                        #
                        merge_hou_obj.setInput(seq, alembic_hou_obj)


def set_build(kwargs):
    Command(kwargs).set_build()
