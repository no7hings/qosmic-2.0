# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.resource as bsc_resource

import qsm_maya.core as qsm_mya_core

import qsm_maya.graph as qsm_mya_graph


class MtgTimeGraph(qsm_mya_graph.GraphBase):
    """
    """

    def __init__(self, namespace):
        self._namespace = namespace

    # @qsm_mya_core.Undo.execute
    def create_all(self, add_to_container=True):
        fps = qsm_mya_core.Frame.get_fps()
        qsm_mya_core.Namespace.create(self._namespace)
        self._cfg = bsc_resource.BscConfigure.get_as_content('maya/montage/mtg_time')
        self._cfg.set('options.namespace', self._namespace)

        # set options
        output_factor = 6000/fps
        input_factor = 1.0/output_factor
        self._cfg.set('options.time_input_factor', input_factor)
        self._cfg.set('options.time_output_factor', output_factor)
        self._cfg.do_flatten()

        nodes = self._create_nodes_fnc(self._namespace, self._cfg)
        containers = self._create_containers_fnc(self._namespace, self._cfg)
        if add_to_container is True:
            qsm_mya_core.Container.add_nodes(
                containers[0], nodes
            )
        return containers[0]

    @classmethod
    def test(cls):
        cls('test').create_all()

    @classmethod
    def test_1(cls):
        cls('test').create_all(False)
        qsm_mya_core.Namespace.remove('test')


class MtgLayerGraph(qsm_mya_graph.GraphBase):
    def __init__(self, namespace, cfg_key):
        self._namespace = namespace
        self._cfg_key = cfg_key

    def create_all(self):
        qsm_mya_core.Namespace.create(self._namespace)
        self._cfg = bsc_resource.BscConfigure.get_as_content(self._cfg_key)
        self._cfg.set('options.namespace', self._namespace)
        self._cfg.do_flatten()

        dag_nodes = self._create_dag_nodes_fnc(self._namespace, self._cfg)
        nodes = self._create_nodes_fnc(self._namespace, self._cfg)
        dag_roots = qsm_mya_core.DagNode.find_roots(dag_nodes)
        containers = self._create_containers_fnc(self._namespace, self._cfg)
        qsm_mya_core.Container.add_nodes(
            containers[0], nodes
        )
        qsm_mya_core.Container.add_dag_nodes(
            containers[0], dag_roots
        )
        return containers[0]

    @classmethod
    def test(cls):
        cls('test', 'maya/montage/mtg_layer').create_all()
