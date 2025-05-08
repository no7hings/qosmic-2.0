# coding:utf-8
import lxbasic.resource as bsc_resource

import qsm_maya.core as qsm_mya_core

import qsm_maya.graph as qsm_mya_graph


class FxProxyGraph(qsm_mya_graph.GraphBase):
    @classmethod
    def test(cls):
        cls(None, 'maya/resora/fx_proxy_rig').create_all()

    def __init__(self, namespace, cfg_key):
        self._namespace = namespace
        self._cfg_key = cfg_key

    def create_all(self):
        self._cfg = bsc_resource.BscConfigure.get_as_content(self._cfg_key)
        if self._namespace is not None:
            qsm_mya_core.Namespace.create(self._namespace)
            self._cfg.set('options.namespace', self._namespace)
        self._cfg.do_flatten()

        dag_nodes = self._create_dag_nodes_fnc(self._namespace, self._cfg)
        nodes = self._create_nodes_fnc(self._namespace, self._cfg)

        self._post_fnc()

    def _post_fnc(self):
        qsm_mya_core.NodeAttribute.set_value(
            'geo', 'rotateX', 90
        )
        qsm_mya_core.Transform.freeze_transformations('geo')
        qsm_mya_core.SmoothBindSkin.create(
            ['Root_M'], ['geo']
        )
