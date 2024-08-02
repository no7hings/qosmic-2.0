# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.resource as bsc_resource

import qsm_maya.core as qsm_mya_core


class _GraphBase(object):
    @classmethod
    def _create_dag_node(cls, path, data):
        type_name = data['type']
        properties = data.get('properties', {})
        create_properties = data.get('create_properties', {})
        connections = data.get('connections', [])
        is_create, path = qsm_mya_core.EtrNodeOpt.generate_dag_node_create_args(
            path, type_name
        )
        if is_create is True:
            node_opt = qsm_mya_core.EtrNodeOpt(path)
            node_opt.apply_properties(properties)
            node_opt.create_properties(create_properties)
            node_opt.create_connections_by_data(connections)
        return path

    @classmethod
    def _create_node(cls, data):
        type_name = data['type']
        name = data['name']
        properties = data.get('properties', {})
        create_properties = data.get('create_properties', {})
        connections = data.get('connections', [])
        is_create, name = qsm_mya_core.EtrNodeOpt.generate_node_create_args(
            name, type_name
        )
        if is_create is True:
            node_opt = qsm_mya_core.EtrNodeOpt(name)
            node_opt.apply_properties(properties)
            node_opt.create_properties(create_properties)
            node_opt.create_connections_by_data(connections)
        keyframes = data.get('keyframes')
        if keyframes:
            qsm_mya_core.AnmCurveOpt(name).set_points(keyframes)
        return name

    @classmethod
    def _create_container(cls, data):
        type_name = data['type']
        name = data['name']
        properties = data.get('properties', {})
        create_properties = data.get('create_properties', {})
        connections = data.get('connections', [])
        is_create, path = qsm_mya_core.EtrNodeOpt.generate_container_create_args(
            name, type_name
        )
        if is_create is True:
            node_opt = qsm_mya_core.EtrNodeOpt(path)
            node_opt.apply_properties(properties)
            node_opt.create_properties(create_properties)
            node_opt.create_connections_by_data(connections)
        return path


class MotionClipGraph(_GraphBase):
    """
# coding:utf-8
import qsm_maya_adv
reload(qsm_maya_adv)
qsm_maya_adv.do_reload()

import qsm_maya_adv.core as c

c.MotionClipGraph.test()

    """

    def __init__(self, namespace):
        self._namespace = namespace

    # @qsm_mya_core.Undo.execute
    def create_all(self, add_to_container=True):
        qsm_mya_core.Namespace.create(self._namespace)
        self._cfg = bsc_resource.RscExtendConfigure.get_as_content('motion/motion_time')
        self._cfg.set('options.namespace', self._namespace)
        self._cfg.do_flatten()
        nodes = self._create_nodes()
        containers = self._create_containers()
        if add_to_container is True:
            qsm_mya_core.Container.add_nodes(
                containers[0], nodes
            )
        return containers[0]

    def _create_containers(self):
        results = []
        c = self._cfg.get_as_content('containers')
        for i_key in c.get_top_keys():
            i_data = c.get_as_content(i_key)
            results.append(self._create_container(i_data))
        return results

    def _create_nodes(self):
        results = []
        c = self._cfg.get_as_content('nodes')
        for i_key in c.get_top_keys():
            i_data = c.get_as_content(i_key)
            results.append(self._create_node(i_data))
        return results

    @classmethod
    def test(cls):
        cls('test').create_all()

    @classmethod
    def test_1(cls):
        cls('test').create_all(False)
        qsm_mya_core.Namespace.remove('test')


class MotionBlendGraph(MotionClipGraph):
    def __init__(self, namespace):
        super(MotionBlendGraph, self).__init__(namespace)

    def create_all(self, *args, **kwargs):
        qsm_mya_core.Namespace.create(self._namespace)
        self._cfg = bsc_resource.RscExtendConfigure.get_as_content('motion/motion_blend')
        self._cfg.set('options.namespace', self._namespace)
        self._cfg.do_flatten()
        nodes = self._create_nodes()
        containers = self._create_containers()
        # qsm_mya_core.Container.add_nodes(
        #     containers[0], nodes
        # )
        return containers[0]

    @classmethod
    def test(cls):
        cls('test').create_all()


class MotionLayerGraph(_GraphBase):
    def __init__(self, namespace, cfg_key):
        self._namespace = namespace
        self._cfg_key = cfg_key

    def create_all(self):
        qsm_mya_core.Namespace.create(self._namespace)
        self._cfg = bsc_resource.RscExtendConfigure.get_as_content(self._cfg_key)
        self._cfg.set('options.namespace', self._namespace)
        self._cfg.do_flatten()
        dag_nodes = self._create_dag_nodes()
        nodes = self._create_nodes()
        dag_roots = qsm_mya_core.DagNode.find_roots(dag_nodes)
        containers = self._create_containers()
        qsm_mya_core.Container.add_nodes(
            containers[0], nodes
        )
        qsm_mya_core.Container.add_dag_nodes(
            containers[0], dag_roots
        )
        return containers[0]

    def _create_containers(self):
        results = []
        c = self._cfg.get_as_content('containers')
        for i_key in c.get_top_keys():
            i_data = c.get_as_content(i_key)
            results.append(self._create_container(i_data))
        return results

    def _create_nodes(self):
        results = []
        c = self._cfg.get_as_content('nodes')
        for i_key in c.get_top_keys():
            i_data = c.get_as_content(i_key)
            results.append(self._create_node(i_data))
        return results

    def _create_dag_nodes(self):
        results = []
        c = self._cfg.get_as_content('dag_nodes')
        for i_key in c.get_top_keys():
            i_data = c.get_as_content(i_key)
            i_path = '|'.join(['{}:{}'.format(self._namespace, x) if x else '' for x in i_key.split('/')])
            results.append(self._create_dag_node(i_path, i_data))
        return results

    def _create_curves(self):
        pass

    @classmethod
    def test(cls):
        cls('test', 'motion/motion_layer').create_all()
