# coding:utf-8


class DictOpt(object):
    def __init__(self, **kwargs):
        self._dict = dict(**kwargs)

    def __getattr__(self, key):
        return self._dict[key]

    def __setattr__(self, key, value):
        if key in {'_dict'}:
            self.__dict__[key] = value
        else:
            self._dict[key] = value

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __str__(self):
        return str(self._dict)

    def __repr__(self):
        return '\n'+self.__str__()

    def get(self, *args, **kwargs):
        return self._dict.get(*args, **kwargs)

    def items(self):
        return self._dict.items()
