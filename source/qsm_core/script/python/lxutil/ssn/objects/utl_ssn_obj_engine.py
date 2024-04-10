# coding:utf-8
import lxbasic.core as bsc_core

import lxutil.ssn.abstracts as utl_ssn_abstracts


class SsnRsvApplication(utl_ssn_abstracts.AbsSsnRsvApplication):
    def __init__(self):
        super(SsnRsvApplication, self).__init__()

    def _get_any_scene_file_path_(self):
        return bsc_core.EnvBaseMtd.get(
            'RSV_SCENE_FILE'
        )
