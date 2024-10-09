# coding:utf-8
from .. import _abc


class Main(_abc.AbsAdvValidationPrc):
    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)

    def execute(self):
        import qsm_maya.steps.rig.core as qsm_mya_stp_rig_core

        meshes = self.find_all_meshes()
        if not meshes:
            return

        for i_mesh in meshes:
            i_mesh_opt = qsm_mya_stp_rig_core.MeshSkinOpt(i_mesh)
            i_key_path = self.to_key_path(i_mesh)
            i_results = []
            if i_mesh_opt.is_valid() is True:
                i_vertex_names = i_mesh_opt.get_deficiency_weight_vertex_names()
                for j_vtx_name in i_vertex_names:
                    i_results.append(
                        dict(vertex=j_vtx_name)
                    )

            if i_results:
                self._result_content.append_element(
                    self._key, (i_key_path, i_results)
                )
