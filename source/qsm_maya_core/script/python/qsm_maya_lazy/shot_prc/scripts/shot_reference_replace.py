# coding:utf-8


class ShotReferenceReplace(object):
    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def execute(self):
        import lxbasic.log as bsc_log

        import lxbasic.storage as bsc_storage

        import qsm_maya.core as qsm_mya_core

        import qsm_maya_lazy_montage.scripts as qsm_mya_lzy_mtg_scripts

        file_path = self._kwargs.get('file_path')
        cache_path = self._kwargs.get('cache_path')

        if not file_path:
            raise RuntimeError()

        reference_replace_map = self._kwargs.get('reference_replace_map')
        if not reference_replace_map:
            raise RuntimeError()

        directory_path = bsc_storage.StgFileOpt(cache_path).directory_path

        references = qsm_mya_core.References.get_all_loaded()

        c = 4+len(references)

        with bsc_log.LogProcessContext.create(maximum=c) as l_p:
            qsm_mya_core.SceneFile.new()
            qsm_mya_core.SceneFile.open(file_path)

            l_p.do_update()

            for i in references:
                i_file_path = qsm_mya_core.Reference.get_file(i)
                if i_file_path in reference_replace_map:
                    i_file_path_tgt = reference_replace_map[i_file_path]
                    if i_file_path == i_file_path_tgt:
                        continue

                    i_namespace = qsm_mya_core.Reference.get_namespace(i)

                    i_motion_path = '{}/{}.json'.format(
                        directory_path, i_namespace.replace(':', '__')
                    )
                    if bsc_storage.StgPath.get_is_file(i_motion_path) is False:
                        qsm_mya_lzy_mtg_scripts.AdvChrMotionExportOpt(i_namespace).export(i_motion_path)

                    qsm_mya_core.SceneFile.reference_file()

                l_p.do_update()
