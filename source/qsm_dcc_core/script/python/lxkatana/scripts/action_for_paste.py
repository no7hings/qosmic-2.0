# coding:utf-8
import fnmatch

import six

import lxbasic.storage as bsc_storage
# katana
from .. import core as ktn_core


class ScpActionForNodeGraphMaterialPaste(object):
    KEY = 'texture build'

    def __init__(self, ktn_obj):
        if isinstance(ktn_obj, six.string_types):
            self._ktn_obj = ktn_core.NodegraphAPI.GetNode(
                ktn_obj
            )
        else:
            self._ktn_obj = ktn_obj

        self._obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)

    def accept(self):
        import lxgui.core as gui_core

        import lxgui.qt.core as gui_qt_core

        file_path = None

        text = gui_qt_core.GuiQtUtil.get_text_from_clipboard()

        if text:
            if bsc_storage.StgFileMtd.get_is_exists(text) is True:
                if bsc_storage.StgFileMtd.get_ext(text) in {'.tx', '.png', '.jpg', '.tiff', '.exr'}:
                    file_path = text

        if file_path is not None:
            if self._obj_opt.get_is({'NetworkMaterialCreate'}):
                w = gui_core.GuiDialogForChooseAsBubble.create(
                    ['material', 'shader', 'group', 'image'],
                    'create texture in current material group, choose one scheme to continue'
                )
                scheme = w.get_result()

                if scheme is not None:
                    import lxkatana.scripts as ktn_scripts

                    if scheme == 'image':
                        ktn_scripts.ScpTextureBuildForPaste.create_one(self._obj_opt, file_path)
                    else:
                        ktn_scripts.ScpTextureBuildForPaste(
                            self._obj_opt, scheme, file_path
                        ).accept()
            elif self._obj_opt.get_is({'ShadingGroup'}):
                w = gui_core.GuiDialogForChooseAsBubble.create(
                    ['group', 'image'],
                    'create texture in current material group, choose one scheme to continue'
                )
                scheme = w.get_result()

                if scheme is not None:
                    import lxkatana.scripts as ktn_scripts

                    if scheme == 'image':
                        ktn_scripts.ScpTextureBuildForPaste.create_one(self._obj_opt, file_path)
                    else:
                        ktn_scripts.ScpTextureBuildForPaste(
                            self._obj_opt, scheme, file_path
                        ).accept()


class ScpActionForNodeGraphGroupPaste(object):
    def __init__(self, ktn_obj):
        if isinstance(ktn_obj, six.string_types):
            self._ktn_obj = ktn_core.NodegraphAPI.GetNode(
                ktn_obj
            )
        else:
            self._ktn_obj = ktn_obj

        self._obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)

    def accept(self):
        import lxgui.core as gui_core

        import lxgui.qt.core as gui_qt_core

        file_path = None

        text = gui_qt_core.GuiQtUtil.get_text_from_clipboard()

        if text:
            if bsc_storage.StgFileMtd.get_is_exists(text) is True:
                if bsc_storage.StgFileMtd.get_ext(text) in {'.tx', '.exr', '.hdr'}:
                    file_path = text

        if file_path is not None:
            if fnmatch.filter([file_path], '*/v[0-9][0-9][0-9][0-9]/hdri/*.*'):
                hdri_path = file_path
                if (
                    self._obj_opt.get_is({'Group'})
                    and self._obj_opt.get('type') in {'LightSpace_Wsp_Usr', 'LightSpace_Wsp'}
                ):
                    w = gui_core.GuiDialogForChooseAsBubble.create(
                        ['light HDRI', 'light variant'],
                        'create node in current group, choose one scheme to continue'
                    )
                    scheme = w.get_result()

                    if scheme is not None:
                        import lxkatana.scripts as ktn_scripts

                        ktn_scripts.ScpHdriBuildForPaste(
                            self._obj_opt, scheme, hdri_path
                        ).accept()
                else:
                    w = gui_core.GuiDialogForChooseAsBubble.create(
                        ['light HDRI'],
                        'create node in current group, choose one scheme to continue'
                    )
                    scheme = w.get_result()

                    if scheme is not None:
                        import lxkatana.scripts as ktn_scripts

                        ktn_scripts.ScpHdriBuildForPaste(
                            self._obj_opt, scheme, hdri_path
                        ).accept()
