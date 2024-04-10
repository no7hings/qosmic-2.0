# coding:utf-8
import lxbasic.core as bsc_core


class GuiPrxModForProgress(object):
    FORMAT_0 = '{percent}% {costed_time}'
    FORMAT_1 = '{percent}% {costed_time} / {estimated_time}'

    def __init__(self, proxy, qt_progress, maximum, label=None):
        self._proxy = proxy
        self._qt_progress = qt_progress
        self._maximum = maximum
        self._value = 0
        self._label = label
        # time
        self._timestamp_started = bsc_core.SysBaseMtd.get_timestamp()
        self._timestamp_costed = 0
        #
        self._timestamp_estimated = 0
        # all value map to low
        self._map_maximum = min(maximum, 100)
        self._map_value = 0
        #
        self._parent = None
        #
        self._sub_start = None
        self._sub_end = None
        #
        self._children = []
        #
        self._is_stop = False
        #
        self._is_raise = False
        #
        self._depth = 0

        self._qt_progress.show()

    @property
    def label(self):
        return self._label

    @property
    def value(self):
        return self._value

    @property
    def maximum(self):
        return self._maximum

    @property
    def percent(self):
        return self._get_percent_()

    def get_qt_progress(self):
        return self._qt_progress

    def get_maximum(self):
        return self._maximum

    def set_maximum(self, v):
        self._maximum = v

    def get_value(self):
        return self._value

    def set_value(self, v):
        self._value = v

    #
    def get_depth(self):
        return self._depth

    #
    def set_start(self):
        pass

    def do_update(self, *args, **kwargs):
        if self._is_stop is False:
            self._value += 1
            #
            if self._maximum > 1:
                map_value = int(
                    bsc_core.RawValueRangeMtd.set_map_to(
                        (1, self._maximum), (1, self._map_maximum), self._value
                    )
                )
                if map_value != self._map_value:
                    self._map_value = map_value
                    #
                    self._timestamp_costed = bsc_core.SysBaseMtd.get_timestamp()-self._timestamp_started
                    if self._value > 1:
                        self._timestamp_estimated = (self._timestamp_costed/(self._value-1))*self._maximum
                    else:
                        self._timestamp_estimated = 0
                    #
                    root = self.get_root()
                    root.update_qt_process()

    def set_stop(self):
        if self.get_is_root():
            self._qt_progress._stop_progress_()
            self._value = 0
            self._maximum = 0
            self._map_value = 0
            self._map_maximum = 0
            self._is_stop = True
            self._qt_progress.hide()

    def get_is_stop(self):
        return self._is_stop

    def set_raise(self):
        self._is_raise = True

    def get_parent(self):
        return self._parent

    def get_is_root(self):
        return self._parent is None

    def _get_percent_(self):
        if self._maximum > 0:
            return round(float(self._value)/float(self._maximum), 4)
        else:
            return 0

    def _get_span_(self):
        if self.maximum > 0:
            return round(float(1)/float(self.maximum), 4)
        return 0

    def add_child(self, progress_fnc):
        self._children.append(progress_fnc)
        progress_fnc._parent = self
        #
        progress_fnc._sub_end = self._get_percent_()
        progress_fnc._sub_start = max(min(round(progress_fnc._sub_end-self._get_span_(), 4), 1.0), 0.0)

    def get_show_percent(self):
        kwargs = dict(
            percent=('%3d'%(int(self._get_percent_()*100))),
            value=self._value,
            maximum=self._maximum,
            costed_time=bsc_core.RawIntegerMtd.second_to_time_prettify(
                self._timestamp_costed,
                mode=1
            ),
            estimated_time=bsc_core.RawIntegerMtd.second_to_time_prettify(
                self._timestamp_estimated,
                mode=1
            ),
        )
        if int(self._timestamp_estimated) > 0:
            return self.FORMAT_1.format(
                **kwargs
            )
        return self.FORMAT_0.format(
            **kwargs
        )

    def update_qt_process(self):
        if self._qt_progress is not None:
            if self.get_is_root() is True:
                descendants = self.get_descendants()
                #
                raw = [(self._get_percent_(), (0, 1), self._label, self.get_show_percent())]
                maximums, values = [self._maximum], [self._value]
                map_maximums, map_values = [self._map_maximum], [self._map_value]
                for i_index, i_descendant in enumerate(descendants):
                    maximums.append(i_descendant._maximum)
                    values.append(i_descendant._value)
                    #
                    map_maximums.append(i_descendant._map_maximum)
                    map_values.append(i_descendant._map_value)
                    #
                    i_percent_start = i_descendant._sub_start
                    i_percent_end = i_descendant._sub_end
                    i_percent = i_descendant._get_percent_()
                    #
                    i_label = i_descendant._label
                    i_show_percent = i_descendant.get_show_percent()
                    if i_percent < 1:
                        raw.append(
                            (i_percent, (i_percent_start, i_percent_end), i_label, i_show_percent)
                        )
                #
                maximum, value = sum(maximums), sum(values)
                map_maximum, map_value = sum(map_maximums), sum(map_values)
                #
                self._qt_progress._set_progress_raw_(raw)
                #
                self._qt_progress._set_progress_maximum_(maximum)
                self._qt_progress._set_progress_map_maximum_(map_maximum)
                self._qt_progress._set_progress_value_(value)

    def get_root(self):
        def rcs_fnc_(obj_):
            _parent = obj_.get_parent()
            if _parent is None:
                return obj_
            else:
                return rcs_fnc_(_parent)

        #
        return rcs_fnc_(self)

    def get_descendants(self):
        def rcs_fnc_(lis_, obj_):
            _children = obj_.get_children()
            if _children:
                for _child in _children:
                    lis_.append(_child)
                    rcs_fnc_(lis_, _child)

        #
        lis = []
        rcs_fnc_(lis, self)
        return lis

    def get_children(self):
        return self._children

    def get_descendant_args(self):
        def rcs_fnc_(lis_, obj_, depth_):
            _children = obj_.get_children()
            if _children:
                for _i_child in _children:
                    lis_.append((depth_, _i_child))
                    #
                    rcs_fnc_(lis_, _i_child, depth_+1)

        #
        lis = []
        rcs_fnc_(lis, self, 0)
        return lis

    def __str__(self):
        return '{}(label="{}", maximum={}, value={})'.format(
            self.__class__.__name__,
            self._label,
            self.maximum,
            self.value
        )

    def __repr__(self):
        return self.__str__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.set_stop()