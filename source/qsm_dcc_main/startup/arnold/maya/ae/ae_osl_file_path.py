# encoding=utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

from lxmaya.node_template import base as mya_node_template_base


# build by lynxi
class osl_file_path(mya_node_template_base.AbsNodeTemplate):
    def setup(self):
        self._create_dict = {}
        with self.scroll_layout():
            with self.layout('osl file path', collapse=False):
                self.addControl('filename', useAsFileName=True)
                self.addControl('udim_enable')
                self.addControl('sequence_enable')

            self.addExtraControls()
