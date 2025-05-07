# coding:utf-8
import lxgui.core as gui_core

w = gui_core.GuiDialogForChooseAsBubble.create(
    ['material', 'shader', 'group', 'image'],
    'create texture in current material group, choose one scheme to continue'
)
print(w.get_result())
