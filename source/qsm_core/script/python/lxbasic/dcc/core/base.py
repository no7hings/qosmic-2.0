# coding:utf-8
import lxbasic.core as bsc_core


class DccUtil(object):
    @classmethod
    def get_is_ui_mode(cls):
        if bsc_core.SysApplicationMtd.get_is_maya():
            import lxmaya.core as mya_core

            return mya_core.MyaUtil.get_is_ui_mode()
        elif bsc_core.SysApplicationMtd.get_is_katana():
            import lxkatana.core as ktn_core

            return ktn_core.KtnUtil.get_is_ui_mode()
        return False
