# encoding=utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

from lxmaya.node_template import base as mya_node_template_base


# build by lynxi
class osl_window_box(mya_node_template_base.AbsNodeTemplate):
    def setup(self):
        self._create_dict = {}
        with self.scroll_layout():
            with self.layout('osl window box', collapse=False):
                self.addControl('up_use_z_axis')
                self.addControl('filename', useAsFileName=True)
                self.addControl('texture_flip')
                self.addControl('texture_flop')
                self.addControl('room_depth')
                self.addControl('width_overscan')
                self.addControl('height_overscan')
                self.addControl('midground_enable')
                self.addControl('midground_depth')
                self.addControl('midground_offset_x')
                self.addControl('midground_offset_y')
                self.addControl('curtains_enable')

            self.addExtraControls()