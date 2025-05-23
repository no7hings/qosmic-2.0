# coding:utf-8


class Progress(object):
    def __init__(self, widget):
        self._widget = widget

        self._maximum = None
        self._value = 0

        self._running_flag = False

    def set_maximum(self, value):
        self._maximum = int(value)

    def get_maximum(self):
        return self._maximum

    def set_value(self, value):
        self._value = int(value)

    def get_value(self):
        return self._value

    def get_percent(self):
        return float(self._value)/float(self._maximum)

    def append_maximum(self, maximum):
        if self._maximum is None:
            self._maximum = int(maximum)
            self._running_flag = True
        else:
            self._maximum += int(maximum)

    def stop(self):
        self._running_flag = False

    def get_is_running(self):
        return self._running_flag

    def get_is_finished(self):
        return self._value == self._maximum

    def update(self):
        if self._running_flag is True:
            self._value += 1
            if self._value == self._maximum:
                # todo, many process
                pass
                # self.stop()
            return True
        return False
