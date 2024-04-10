# coding:utf-8
# qt widgets
from ...qt.widgets import utility as gui_qt_wgt_utility
# qt for usd
from ...qt_for_usd import core as gui_qt_usd_core
# qt usd widgets
from ...qt_for_usd.widgets import stage_view as gui_qt_usd_wgt_stage_view
# proxy abstracts
from .. import abstracts as gui_prx_abstracts

if gui_qt_usd_core.QT_USD_FLAG is True:
    QT_WIDGET_CLS = gui_qt_usd_wgt_stage_view.QtUsdStageWidget

    class PrxUsdStageView(
        gui_prx_abstracts.AbsPrxWidget,
    ):
        QT_WIDGET_CLS = gui_qt_usd_wgt_stage_view.QtUsdStageWidget

        def __init__(self, *args, **kwargs):
            super(PrxUsdStageView, self).__init__(*args, **kwargs)

        def get_usd_stage(self):
            return self._qt_widget._get_usd_stage_()

        def refresh_usd_view_draw(self):
            self._qt_widget._refresh_usd_view_draw_()

        def refresh_usd_stage_for_texture_preview(self, *args, **kwargs):
            self._qt_widget._refresh_usd_stage_for_texture_preview_(
                *args, **kwargs
            )

        def refresh_usd_stage_for_asset_preview(self, *args, **kwargs):
            self._qt_widget._refresh_usd_stage_for_asset_preview_(
                *args, **kwargs
            )

        def refresh_usd_stage_for_texture_render(self, *args, **kwargs):
            self._qt_widget._refresh_usd_stage_for_texture_render_(
                *args, **kwargs
            )

        def refresh_usd_stage_for_asset_render(self, *args, **kwargs):
            self._qt_widget._refresh_usd_stage_for_asset_render_(
                *args, **kwargs
            )

        def load_usd_file(self, *args, **kwargs):
            self._qt_widget._load_usd_file_(*args, **kwargs)

        def run_as_thread(self, cache_fnc, build_fnc, post_fnc):
            self._qt_widget._run_build_use_thread_(
                cache_fnc, build_fnc, post_fnc
            )

        def get_usd_model(self):
            return self._qt_widget._get_usd_model_()

        def restore(self):
            self._qt_widget._restore_()
else:
    class PrxUsdStageView(
        gui_prx_abstracts.AbsPrxWidget
    ):
        QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget

        def __init__(self, *args, **kwargs):
            # noinspection PySuperArguments
            super(PrxUsdStageView, self).__init__(*args, **kwargs)

        def get_usd_stage(self):
            pass

        def refresh_usd_view_draw(self):
            pass

        def refresh_usd_stage_for_texture_preview(self, *args, **kwargs):
            pass

        def refresh_usd_stage_for_asset_preview(self, *args, **kwargs):
            pass

        def refresh_usd_stage_for_texture_render(self, *args, **kwargs):
            pass

        def refresh_usd_stage_for_asset_render(self, *args, **kwargs):
            pass

        def load_usd_file(self, *args, **kwargs):
            pass

        def run_as_thread(self, cache_fnc, build_fnc, post_fnc):
            pass

        def get_usd_model(self):
            pass

        def restore(self):
            pass
