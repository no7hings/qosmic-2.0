# coding:utf-8
import collections

import lxbasic.core as bsc_core

import lxgui.qt.core as gui_qt_core

import lxgui.proxy.widgets as prx_widgets


class TestWindow(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)

    def _test_(self):
        def add_fnc_(i_):
            def show_fnc_():
                # thumbnail_file_path = bsc_storage.ImgOiioOptForThumbnail(
                #     '/l/temp/td/dongchangbao/Arnold_Shader_Suite_for_MAYA_v2.0/09-ADVANCED/Del_Cracks_11_1_1_1.jpg'
                # ).generate_thumbnail()
                thumbnail_file_path = '/production/library/resource/all/surface/fort_damaged_floor_te3maaeg/v0001/image/preview_test.jpg'
                # self._prx_list_view.set_loading_update()
                prx_item_widget.set_image(thumbnail_file_path)
                if i_ % 2 == 0:
                    prx_item_widget.set_icons_by_pixmap(
                        [
                            gui_qt_core.GuiQtPixmap.get_by_file_ext_with_tag(
                                '.ma',
                                tag='work',
                                frame_size=(24, 24)
                            ),
                            gui_qt_core.GuiQtPixmap.get_by_file_ext_with_tag(
                                '.ma',
                                tag='work',
                                frame_size=(24, 24)
                            ),
                            gui_qt_core.GuiQtPixmap.get_by_file_ext_with_tag(
                                '.ma',
                                tag='work',
                                frame_size=(24, 24)
                            ),
                            gui_qt_core.GuiQtPixmap.get_by_file_ext_with_tag(
                                '.ma',
                                tag='work',
                                frame_size=(24, 24)
                            ),
                            gui_qt_core.GuiQtPixmap.get_by_file_ext_with_tag(
                                '.ma',
                                tag='work',
                                frame_size=(24, 24)
                            )
                        ]
                    )
                # prx_item_widget.set_image_loading_start()
                prx_item_widget.refresh_widget_force()

            prx_item_widget = self._prx_list_view.create_item()
            prx_item_widget.set_show_build_fnc(show_fnc_)
            prx_item_widget.set_check_enable(True)
            prx_item_widget.set_drag_enable(True)
            prx_item_widget.set_name_dict(
                collections.OrderedDict(
                    [
                        ('type', 'test'),
                        ('name', 'test'),
                        ('tag', 'test'),
                    ]
                )
            )
            # prx_item_widget.set_drag_data(
            #     {
            #         # 'nodegraph/nodes': 'stained_concrete_wall_vdxicg2',
            #         # 'nodegraph/noderefs': 'rootNode',
            #         # 'python/text': 'NodegraphAPI.GetNode(\'worn_painted_wall_vjyifef\')',
            #         # 'python/GetGeometryProducer': 'Nodes3DAPI.GetGeometryProducer(NodegraphAPI.GetNode(\'worn_painted_wall_vjyifef\'))',
            #         'nodegraph/fileref': '/l/resource/td/asset/scene/empty.katana',
            #         # 'application/x-maya-data': ''
            #     }
            # )
            prx_item_widget.set_drag_urls(
                ['/production/library/resource/all/surface/fort_damaged_floor_te3maaeg/v0001/image/preview_test.jpg']
            )
            prx_item_widget.connect_drag_pressed_to(
                self._drag_pressed_fnc_
            )
            prx_item_widget.connect_drag_released_to(
                self._drag_released_fnc_
            )
        #
        self._prx_list_view = prx_widgets.PrxListView()
        self._prx_list_view.get_top_tool_bar().set_expanded(True)
        self._prx_list_view.set_selection_use_multiply()
        # self._prx_list_view.set_drag_enable(True)
        self._prx_list_view.set_item_icon_frame_draw_enable(True)
        self._prx_list_view.set_item_image_frame_draw_enable(True)
        self._prx_list_view.set_item_name_frame_draw_enable(True)
        self._prx_list_view.get_check_tool_box().set_visible(True)
        self._prx_list_view.set_item_names_draw_range([None, 1])
        self._prx_list_view.get_scale_switch_tool_box().set_visible(True)
        self._prx_list_view.set_item_frame_size_basic(96, 72)
        self._prx_list_view.set_item_icon_frame_size(20, 20)
        self._prx_list_view.set_item_icon_size(20, 20)
        self._prx_list_view.set_clear()
        self.add_widget(self._prx_list_view)
        for i in range(200):
            add_fnc_(i)

    def _drag_pressed_fnc_(self, *args, **kwargs):
        print args[0]
        print 'failed'

    def _drag_released_fnc_(self, *args, **kwargs):
        flag, mime_data = args[0]
        print mime_data.data('nodegraph/noderefs').data()
        print 'completed'
        print self._prx_list_view._get_selected_items_()


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    w = TestWindow()
    #
    w.set_definition_window_size((960, 480))
    w.set_window_show()
    w._test_()
    #
    sys.exit(app.exec_())
