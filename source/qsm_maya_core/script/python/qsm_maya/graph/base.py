# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core


class GraphBase(object):
    @classmethod
    def _create_dag_node_fnc(cls, path, data):
        type_name = data['type']
        properties = data.get('properties', {})
        create_properties = data.get('create_properties', {})
        connections = data.get('connections', [])

        is_create, path = qsm_mya_core.EtrNodeOpt.generate_dag_node_create_args(
            path, type_name
        )

        if is_create is True:
            node_opt = qsm_mya_core.EtrNodeOpt(path)
            node_opt.set_dict(properties)
            node_opt.create_properties(create_properties)
            node_opt.create_connections_by_data(connections)
        return path

    @classmethod
    def _create_dag_nodes_fnc(cls, namespace, cfg):
        results = []
        c = cfg.get_as_content('dag_nodes')
        for i_key in c.get_top_keys():
            i_path = '|'.join(['{}:{}'.format(namespace, x) if x else '' for x in i_key.split('/')])
            i_data = c.get_as_content(i_key)
            results.append(cls._create_dag_node_fnc(i_path, i_data))
        return results

    @classmethod
    def _create_node_fnc(cls, name, data):
        type_name = data['type']
        # when name in data use from data by default
        name = data.get('name') or name
        properties = data.get('properties', {})
        create_properties = data.get('create_properties', {})
        connections = data.get('connections', [])

        is_create, name = qsm_mya_core.EtrNodeOpt.generate_node_create_args(
            name, type_name
        )

        if is_create is True:
            node_opt = qsm_mya_core.EtrNodeOpt(name)
            node_opt.set_dict(properties)
            node_opt.create_properties(create_properties)
            node_opt.create_connections_by_data(connections)

        keyframes = data.get('keyframes')
        if keyframes:
            qsm_mya_core.AnmCurveNodeOpt(name).set_points(keyframes)
        return name

    @classmethod
    def _create_nodes_fnc(cls, namespace, cfg):
        results = []
        c = cfg.get_as_content('nodes')
        for i_key in c.get_top_keys():
            i_name = '{}:{}'.format(namespace, i_key)
            i_data = c.get_as_content(i_key)
            results.append(cls._create_node_fnc(i_name, i_data))
        return results

    @classmethod
    def _create_container_fnc(cls, name, data):
        type_name = data['type']
        name = data.get('name') or name
        properties = data.get('properties', {})
        create_properties = data.get('create_properties', {})
        connections = data.get('connections', [])

        is_create, path = qsm_mya_core.EtrNodeOpt.generate_container_create_args(
            name, type_name
        )

        if is_create is True:
            node_opt = qsm_mya_core.EtrNodeOpt(path)
            node_opt.set_dict(properties)
            node_opt.create_properties(create_properties)
            node_opt.create_connections_by_data(connections)
        return path
    
    @classmethod
    def _create_containers_fnc(cls, namespace, cfg):
        results = []
        c = cfg.get_as_content('containers')
        for i_key in c.get_top_keys():
            i_name = '{}:{}'.format(namespace, i_key)
            i_data = c.get_as_content(i_key)
            results.append(cls._create_container_fnc(i_name, i_data))
        return results
