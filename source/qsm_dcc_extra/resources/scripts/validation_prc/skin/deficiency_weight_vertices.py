# coding:utf-8


class Main(object):
    def __init__(self, task_prc):
        self._task_prc = task_prc

    def execute(self):
        import qsm_maya.steps.rig.core as qsm_mya_stp_rig_core

        meshes = self._task_prc.find_all_meshes()
        if not meshes:
            return

        for i_mesh in meshes:
            i_mesh_opt = qsm_mya_stp_rig_core.MeshSkinOpt(i_mesh)
            i_key_path = self._task_prc.to_node_key_path(i_mesh)
            i_results = []
            if i_mesh_opt.is_valid() is True:
                i_vertex_names = i_mesh_opt.get_deficiency_weight_vertex_names()
                for j_vtx_name in i_vertex_names:
                    i_results.append(
                        dict(vertex=j_vtx_name)
                    )

            if i_results:
                self._task_prc._result_content.append_element(
                    self._task_prc._key, (i_key_path, i_results)
                )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    Main(task_prc).execute()
