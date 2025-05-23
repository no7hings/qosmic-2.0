# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.resource as bsc_resource

import lxgui.core as gui_core

from .. import core as _mya_core


class ShelfBuild(object):
    @classmethod
    def test(cls):
        cls('maya/shelves/animation').execute()

    def __init__(self, cfg_key):
        self._c = bsc_resource.BscConfigure.get_as_content(cfg_key)
        self._language = gui_core.GuiUtil.get_language()

    def create_shelf(self, data):
        if self._language == 'chs':
            shelf_name = data.get('name_chs')
        else:
            shelf_name = data.get('name')

        _ = bsc_core.ensure_unicode(shelf_name)
        shelf_key = _.replace(' ', '_')

        if _mya_core.Shelf.is_exists(shelf_key):
            _mya_core.Shelf.delete(shelf_key)

        shelf = _mya_core.Shelf.create(shelf_name)
        return shelf

    def create_separator(self, shelf, data):
        tool_tip = gui_core.GuiUtil.choice_gui_tool_tip(
            self._language, data
        )

        _mya_core.Shelf.create_separator(
            shelf,
            annotation=tool_tip,
        )

    def create_button(self, shelf, data):
        j_name = gui_core.GuiUtil.choice_gui_name(self._language, data)
        j_tool_tip = gui_core.GuiUtil.choice_gui_tool_tip(self._language, data)
        j_annotation = u'{}\n{}'.format(j_name, j_tool_tip)

        j_auto_label_color = data.get('auto_label_color', True)
        j_script = data['script']
        j_dbl_script = data.get('dbl_script') or ''
        i_button_style = data.get('button_style') or 'text_and_icon'
        if i_button_style == 'icon':
            j_icon = gui_core.GuiIcon.get(data['icon'])
            j_button = _mya_core.Shelf.create_button(
                shelf,
                label=j_name,
                image=j_icon,
                annotation=j_annotation,
                command=j_script,
                doubleClickCommand=j_dbl_script,
                style='iconOnly',
            )
        elif i_button_style == 'text_and_icon':
            if self._language == 'chs':
                j_button_name = data['button_name_chs']
            else:
                j_button_name = data['button_name']

            j_icon = gui_core.GuiIcon.get(data['icon'])
            background_rgb = bsc_core.BscTextOpt(j_name).to_hash_rgb(maximum=1.0, s_p=(32, 55), v_p=(55, 85))
            j_kwargs = dict(
                label=j_name,
                image=j_icon,
                annotation=j_annotation,
                command=j_script,
                doubleClickCommand=j_dbl_script,
                style='textOnly',
                imageOverlayLabel=j_button_name,
                overlayLabelColor=(1.0, 1.0, 1.0),
                overlayLabelBackColor=(.25, .25, .25, .5),
                font='fixedWidthFont',
                align='center',
            )
            if j_auto_label_color is True:
                j_kwargs.update(
                    dict(
                        overlayLabelBackColor=(background_rgb[0], background_rgb[1], background_rgb[2], 1.0),
                    )
                )

            j_button = _mya_core.Shelf.create_button(
                shelf,
                **j_kwargs
            )
        else:
            raise RuntimeError()

        action_data = data.get('actions')
        if action_data:
            for k_k, k_v in action_data.items():
                if self._language == 'chs':
                    k_name = k_v['name_chs']
                else:
                    k_name = k_v['name']
                _mya_core.Shelf.create_button_action(
                    j_button, k_name, k_v['script']
                )

    def execute(self):
        shelf_data = self._c.get('build.options')

        shelf = None
        for k, v in shelf_data.items():
            i_type = v['type']
            if i_type in {'tab', 'shelf'}:
                shelf = self.create_shelf(v)
            elif i_type == 'separator':
                self.create_separator(shelf, v)
            elif i_type == 'button':
                self.create_button(shelf, v)
