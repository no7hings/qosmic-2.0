# coding:utf-8
# qt widgets
from ...qt.widgets import chart as gui_qt_wgt_chart
# proxy abstracts
from .. import abstracts as gui_prx_abstracts


class PrxSectorChart(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_chart.QtChartAsSector

    def __init__(self, *args, **kwargs):
        super(PrxSectorChart, self).__init__(*args, **kwargs)

    def set_chart_data(self, data, mode=0):
        self.widget._set_chart_data_(data, mode)


class PrxRadarChart(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_chart.QtChartAsRadar

    def __init__(self, *args, **kwargs):
        super(PrxRadarChart, self).__init__(*args, **kwargs)

    def set_chart_data(self, data, mode=0):
        self.widget._set_chart_data_(data, mode)


class PrxPieChart(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_chart.QtChartAsPie

    def __init__(self, *args, **kwargs):
        super(PrxPieChart, self).__init__(*args, **kwargs)

    def set_chart_data(self, data, mode=0):
        self.widget._set_chart_data_(data, mode)


class PrxHistogramChart(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_chart.QtChartAsHistogram

    def __init__(self, *args, **kwargs):
        super(PrxHistogramChart, self).__init__(*args, **kwargs)

    def set_chart_data(self, data, mode=0):
        self.widget._set_chart_data_(data, mode)

    def set_labels(self, labels):
        self.widget._set_labels_(labels)


class PrxSequenceChart(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_chart.QtChartAsSequence

    def __init__(self, *args, **kwargs):
        super(PrxSequenceChart, self).__init__(*args, **kwargs)

    def set_chart_data(self, data, mode=0):
        self.widget._set_chart_data_(data, mode)

    def set_name(self, labels):
        self.widget._set_name_text_(labels)

    def set_name_width(self, w):
        self.widget._set_name_width_(w)

    def set_height(self, h):
        self.widget._set_height_(h)

    def set_menu_data(self, raw):
        self.widget._set_menu_data_(raw)

    def get_status(self):
        return self.widget._get_status_()

    def get_index_range(self):
        return self.widget._get_index_range_()
