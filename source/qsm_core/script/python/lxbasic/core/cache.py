# coding:utf-8
import collections


class LRUCache:
    def __init__(self, maximum=64):
        self._dict = collections.OrderedDict()
        self._maximum = maximum

    def __contains__(self, key):
        return key in self._dict

    def __str__(self):
        return "{}({})".format(
            self.__class__.__name__, self._dict.items()
        )

    def __repr__(self):
        return '\n'+self.__str__()

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def get(self, key):
        if key in self._dict:
            # move to last
            value = self._dict.pop(key)
            self._dict[key] = value
            return value
        return None

    def set(self, key, value):
        if key in self._dict:
            # move to last
            self._dict.pop(key)
        # remove first
        elif len(self._dict) >= self._maximum:
            self._dict.popitem(last=False)
        self._dict[key] = value



