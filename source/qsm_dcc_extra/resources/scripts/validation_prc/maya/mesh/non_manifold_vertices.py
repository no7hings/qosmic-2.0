# coding:utf-8


class Main(object):
    def __init__(self, task_prc):
        self._task_prc = task_prc

    def execute(self):
        import qsm_maya.core as qsm_mya_core

        import qsm_maya.handles.model.core as qsm_mya_hdl_mdl_core

        meshes = qsm_mya_core.Scene.find_all_dag_nodes(type_includes=['mesh'])
        if not meshes:
            return

        for i_mesh in meshes:
            i_mesh_opt = qsm_mya_hdl_mdl_core.MeshValidationOpt(i_mesh)
            i_vertex_names = i_mesh_opt.get_non_manifold_vertex_names()
            if i_vertex_names:
                i_results = []
                i_key_path = self._task_prc.to_node_key_path(i_mesh)
                for j_vtx_name in i_vertex_names:
                    i_results.append(
                        dict(vertex=j_vtx_name)
                    )

                self._task_prc._result_content.append_element(
                    self._task_prc._key, (i_key_path, i_results)
                )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    Main(task_prc).execute()