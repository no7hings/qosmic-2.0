# coding:utf-8
import functools

import lxbasic.storage as bsc_storage

import lxbasic.content as bsc_content

import lxbasic.resource as bsc_resource

from .. import core as _mya_core


class NodePreset:

    @classmethod
    def generate_menu_content(cls, node_type, key_excludes=None):
        @_mya_core.Undo.execute
        def fnc_(key_, dict_):
            _ = _mya_core.Selection.get_as_nodes()
            for i_node in _:
                i_ncloth = None
                if _mya_core.Node.is_transform_type(i_node):
                    i_transform = i_node
                    i_shape = _mya_core.Transform.get_shape(i_transform)
                    if _mya_core.Node.get_type(i_shape) == 'nCloth':
                        i_ncloth = i_shape
                    elif _mya_core.Node.get_type(i_shape) == 'mesh':
                        i_ncloth = _mya_core.MeshNCloth.get_nshape(i_transform)
                else:
                    if _mya_core.Node.get_type(i_node) == 'nCloth':
                        i_ncloth = i_node
                    elif _mya_core.Node.get_type(i_node) == 'mesh':
                        i_transform = _mya_core.Shape.get_transform(i_node)
                        i_ncloth = _mya_core.MeshNCloth.get_nshape(i_transform)

                if i_ncloth:
                    _mya_core.EtrNodeOpt(i_ncloth).set_dict(dict_, key_excludes)
                    _mya_core.NodeAttribute.create_as_string(i_ncloth, 'qsm_node_preset', key_)

        ctt = bsc_content.Dict()
        yaml_path = bsc_resource.BscExtendResource.get('node_preset/maya/{}.yml'.format(node_type))
        if yaml_path:
            data = bsc_storage.StgFileOpt(yaml_path).set_read()
            if data:
                group_path = '/load_node_preset'
                ctt.set(
                    '{}.properties'.format(group_path),
                    dict(
                        type='group',
                        name='Load',
                        name_chs='加载{}预设'.format(node_type),
                        icon_name='file/folder'
                    )
                )
                for k, v in data.items():
                    i_path = '{}/{}'.format(group_path, k)
                    ctt.set(
                        '{}.properties'.format(i_path),
                        dict(
                            type='action',
                            name=v['name'],
                            name_chs=v['name_chs'],
                            icon_name='file/file',
                            execute_fnc=functools.partial(fnc_, k, v['properties'])
                        )
                    )
        return ctt
