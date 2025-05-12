# coding:utf-8
import lxbasic.resource as bsc_resource

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

import qsm_maya.graph as qsm_mya_graph


class FxProxyRigGraph(qsm_mya_graph.GraphBase):
    @classmethod
    def test(cls):
        cls(None, 'maya/resora/fx_proxy_rig').create_all(
            image_path='Z:/libraries/lazy-resource/all/motion_splice/free_test_jump/preview/images/image.<f>.jpg',
            start_frame=1,
            end_frame=66
        )

    def __init__(self, namespace, cfg_key):
        self._namespace = namespace
        self._cfg_key = cfg_key

    def create_all(self, image_path, start_frame, end_frame):
        self._cfg = bsc_resource.BscConfigure.get_as_content(self._cfg_key)
        if self._namespace is not None:
            qsm_mya_core.Namespace.create(self._namespace)
            self._cfg.set('options.namespace', self._namespace)
        self._cfg.do_flatten()

        dag_nodes = self._create_dag_nodes_fnc(self._namespace, self._cfg)
        nodes = self._create_nodes_fnc(self._namespace, self._cfg)

        self._post_fnc(image_path, start_frame, end_frame)

    def _post_fnc(self, image_path, start_frame, end_frame):
        qsm_mya_core.NodeAttribute.set_value(
            'fx_geo', 'rotateX', 90
        )
        qsm_mya_core.Transform.freeze_transformations('fx_geo')
        qsm_mya_core.SmoothBindSkin.create(
            ['Root_M'], ['fx_geo']
        )

        # apply image sequence
        qsm_mya_core.NodeAttribute.set_as_string('fx_image', 'fileTextureName', image_path)

        # turn image sequence on
        qsm_mya_core.NodeAttribute.set_value('fx_image', 'useFrameExtension', 1)
        qsm_mya_core.NodeAttribute.set_value('Main', 'fx_image_start_frame', start_frame)
        qsm_mya_core.NodeAttribute.set_value('Main', 'fx_image_end_frame', end_frame)
