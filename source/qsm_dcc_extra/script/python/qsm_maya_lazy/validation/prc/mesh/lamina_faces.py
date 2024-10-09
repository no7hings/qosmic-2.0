# coding:utf-8
from .. import _abc


class Main(_abc.AbsValidationPrc):
    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)

    def execute(self):
        import qsm_maya.core as qsm_mya_core

        import qsm_maya.steps.model.core as qsm_mya_stp_mdl_core

        meshes = qsm_mya_core.Scene.find_all_dag_nodes(type_includes=['mesh'])
        if not meshes:
            return

        for i_mesh in meshes:
            i_mesh_opt = qsm_mya_stp_mdl_core.MeshValidationOpt(i_mesh)
            i_face_names = i_mesh_opt.get_lamina_face_names()
            if i_face_names:
                i_results = []
                i_key_path = self.to_key_path(i_mesh)
                for j_face_name in i_face_names:
                    i_results.append(
                        dict(face=j_face_name)
                    )

                self._result_content.append_element(
                    self._key, (i_key_path, i_results)
                )
