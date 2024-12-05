# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.resource as bsc_resource

import lxgui.core as gui_core

from .. import core as _mya_core


class ShelfBuild(object):
    @classmethod
    def test(cls):
        cls('maya/lazy-shelf/cfx').execute()

    def __init__(self, configure_key):
        self._c = bsc_resource.RscExtendConfigure.get_as_content(
            configure_key
        )

    def execute(self):
        language = gui_core.GuiUtil.get_language()

        if language == 'chs':
            shelf_name = self._c.get('build.name_chs')
        else:
            shelf_name = self._c.get('build.name')

        _ = bsc_core.ensure_unicode(shelf_name)
        shelf_key = _.replace(' ', '_')

        if _mya_core.Shelf.is_exists(shelf_key):
            _mya_core.Shelf.delete(shelf_key)

        shelf = _mya_core.Shelf.create(shelf_name)

        shelf_data = self._c.get('build.shelves')

        for i_k, i_v in shelf_data.items():
            i_tool_tip = gui_core.GuiUtil.choice_gui_tool_tip(
                language, i_v
            )

            _mya_core.Shelf.create_separator(
                shelf,
                annotation=i_tool_tip,
            )
            i_tools = self._c.get('build.shelves.{}.tools'.format(i_k))

            for j_k, j_v in i_tools.items():
                j_name = gui_core.GuiUtil.choice_gui_name(language, j_v)
                j_tool_tip = gui_core.GuiUtil.choice_gui_tool_tip(language, j_v)
                j_script = j_v['script']
                j_dbl_script = j_v.get('dbl_script') or ''
                i_button_style = j_v.get('button_style') or 'text_and_icon'
                if i_button_style == 'icon':
                    j_icon = gui_core.GuiIcon.get(j_v['icon'])
                    j_button = _mya_core.Shelf.create_button(
                        shelf,
                        label=j_name,
                        image=j_icon,
                        annotation=j_tool_tip,
                        command=j_script,
                        doubleClickCommand=j_dbl_script,
                        style='iconOnly',
                    )
                elif i_button_style == 'text_and_icon':
                    if language == 'chs':
                        j_button_name = j_v['button_name_chs']
                    else:
                        j_button_name = j_v['button_name']

                    j_icon = gui_core.GuiIcon.get(j_v['icon'])
                    background_rgb = bsc_core.BscTextOpt(j_name).to_hash_rgb(maximum=1.0, s_p=(32, 55), v_p=(55, 85))
                    j_button = _mya_core.Shelf.create_button(
                        shelf,
                        label=j_name,
                        image=j_icon,
                        annotation=j_tool_tip,
                        command=j_script,
                        doubleClickCommand=j_dbl_script,
                        style='textOnly',
                        imageOverlayLabel=j_button_name,
                        overlayLabelColor=(1.0, 1.0, 1.0),
                        overlayLabelBackColor=(background_rgb[0], background_rgb[1], background_rgb[2], 1.0),
                        font='boldLabelFont',
                        align='center',
                    )
                else:
                    raise RuntimeError()

                action_data = j_v.get('actions')
                if action_data:
                    for k_k, k_v in action_data.items():
                        if language == 'chs':
                            k_name = k_v['name_chs']
                        else:
                            k_name = k_v['name']
                        _mya_core.Shelf.create_button_action(
                            j_button, k_name, k_v['script']
                        )
