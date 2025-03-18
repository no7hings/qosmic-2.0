# coding:utf-8
import lxbasic.core as bsc_core

from .. import base as _base


# parameters
class _AbsParam(_base._ParamBase):
    def __init__(self, *args, **kwargs):
        super(_AbsParam, self).__init__(*args, **kwargs)

        self._data.options = _base._Dict(
            widget='',
            gui_name='',
            gui_name_chs=''
        )

    @property
    def options(self):
        return self._data.options

    def set_options(self, **kwargs):
        self._data.options.update(**kwargs)

    def get_options(self):
        return self._data.options

    def set_gui_name(self, text):
        self._data.options.gui_name = text

    def set_gui_name_chs(self, text):
        self._data.options.gui_name_chs = text

    def get_label(self):
        if self._gui_language == 'chs':
            return self._data.options.gui_name_chs or self._data.options.gui_name
        return self._data.options.gui_name


# group
class _Group(_AbsParam):
    def __init__(self, *args, **kwargs):
        super(_Group, self).__init__(*args, **kwargs)

        self._data.type = 'group'

        self._data.options.widget = 'group'


class _AbsTyped(_AbsParam):
    def __init__(self, *args, **kwargs):
        super(_AbsTyped, self).__init__(*args, **kwargs)

        self._data.value = None
        self._data.default = None

    @_base.EventFactory.send(_base.EventTypes.ParamSetValue)
    def set_value(self, value):
        self._data.value = value

    # for gui
    def _set_value(self, value):
        self._data.value = value

    def get_value(self):
        return self._data.value

    def set_default(self, value):
        self._data.default = value

    def get_default(self):
        return self._data.default


class _String(_AbsTyped):
    def __init__(self, *args, **kwargs):
        super(_String, self).__init__(*args, **kwargs)

        self._data.type = 'string'

        self._data.value = ''
        self._data.default = ''

        self._data.options.widget = 'string'


class _Integer(_AbsTyped):
    def __init__(self, *args, **kwargs):
        super(_Integer, self).__init__(*args, **kwargs)

        self._data.type = 'integer'

        self._data.value = 0
        self._data.default = 0

        self._data.options.widget = 'integer'


class _Float(_AbsTyped):
    def __init__(self, *args, **kwargs):
        super(_Float, self).__init__(*args, **kwargs)

        self._data.type = 'float'

        self._data.value = 0.0
        self._data.default = 0.0

        self._data.options.widget = 'float'


class _Boolean(_AbsTyped):
    def __init__(self, *args, **kwargs):
        super(_Boolean, self).__init__(*args, **kwargs)

        self._data.type = 'boolean'

        self._data.value = False
        self._data.default = False

        self._data.options.widget = 'checkbox'


class _Script(_AbsParam):
    def __init__(self, *args, **kwargs):
        super(_Script, self).__init__(*args, **kwargs)

        self._data.type = 'script'

        self._data.options.widget = 'button'
        self._data.option.script = ''


class _IntegerArray(_AbsTyped):
    def __init__(self, *args, **kwargs):
        super(_IntegerArray, self).__init__(*args, **kwargs)
        
        self._data.type = 'integer'
        self._data.value = []
        self._data.default = []

        self._data.options.widget = 'default'


class _StringArray(_AbsTyped):
    def __init__(self, *args, **kwargs):
        super(_StringArray, self).__init__(*args, **kwargs)

        self._data.type = 'string'
        self._data.value = []
        self._data.default = []

        self._data.options.widget = 'default'


class ParamRootFactory:
    @staticmethod
    def add_one(scheme='parameter'):
        def decorator(fnc):
            if scheme == 'parameter':
                def wrapper(self, name=None, parent_path=None, param_path=None, *args, **kwargs):
                    prefix = name or scheme
                    param_path = self._generate_param_path(
                        name=name,
                        parent_path=parent_path,
                        param_path=param_path,
                        prefix=prefix
                    )
                    if param_path in self._dict:
                        return self._dict[param_path]

                    model = fnc(self, name, parent_path, param_path, *args, **kwargs)

                    self._dict[param_path] = model
                    path = bsc_core.BscAttributePath.join_by(self._node.get_path(), param_path)

                    port_path_opt = bsc_core.BscPortPathOpt(param_path)

                    name = port_path_opt.get_name()

                    model._set_path(path)
                    model._set_param_path(param_path)
                    model.set_name(name)
                    model.set_gui_name(bsc_core.BscText.to_prettify(name))

                    if 'value' in kwargs:
                        model.set_value(kwargs['value'])
                    return model
                return wrapper
            elif scheme == 'group':
                def wrapper(self, name=None, parent_path=None, param_path=None, *args, **kwargs):
                    prefix = name or scheme
                    param_path = self._generate_param_path(
                        name=name,
                        parent_path=parent_path,
                        param_path=param_path,
                        prefix=prefix
                    )

                    if param_path in self._dict:
                        return self._dict[param_path]

                    model = _Group(self._node)
                    self._dict[param_path] = model
                    path = bsc_core.BscAttributePath.join_by(self._node.get_path(), param_path)

                    port_path_opt = bsc_core.BscPortPathOpt(param_path)

                    name = port_path_opt.get_name()

                    model._set_path(path)
                    model._set_param_path(param_path)
                    model.set_name(name)
                    model.set_gui_name(bsc_core.BscText.to_prettify(name))

                    return model
                return wrapper
            elif scheme == 'auto':
                def wrapper(self, type_name, name=None, parent_path=None, param_path=None, *args, **kwargs):
                    prefix = name or scheme
                    param_path = self._generate_param_path(
                        name=name,
                        parent_path=parent_path,
                        param_path=param_path,
                        prefix=prefix
                    )

                    model = fnc(self, type_name, name, parent_path, param_path, *args, **kwargs)

                    self._dict[param_path] = model
                    path = bsc_core.BscAttributePath.join_by(self._node.get_path(), param_path)

                    port_path_opt = bsc_core.BscPortPathOpt(param_path)

                    name = port_path_opt.get_name()

                    model._set_path(path)
                    model._set_param_path(param_path)
                    model.set_name(name)
                    model.set_gui_name(bsc_core.BscText.to_prettify(name))

                    if 'value' in kwargs:
                        model.set_value(kwargs['value'])
                    return model
                return wrapper
            else:
                raise RuntimeError()
        return decorator


class ParamRoot(_base._Base):
    VALUE_PARAM_CLS_MAP = {
        # constant
        'string': _String,
        'integer': _Integer,
        'float': _Float,
        'boolean': _Boolean,
        'script': _Script,
        # array
        'integer_array': _IntegerArray,
    }

    def __init__(self, node, data):
        self._node = node
        self._dict = data

    def get_node_path(self):
        return self._node.get_path()

    def _generate_param_path(self, name, parent_path, param_path, prefix):
        if param_path is None:
            if name is None:
                param_path = self._find_next_param_path(self._dict, prefix, parent_path)
            else:
                if parent_path is None:
                    param_path = name
                else:
                    param_path = '{}.{}'.format(parent_path, name)
        return param_path

    @ParamRootFactory.add_one('auto')
    def add_auto(self, type_name, name=None, parent_path=None, param_path=None, *args, **kwargs):
        param_cls = self.VALUE_PARAM_CLS_MAP[type_name]
        model = param_cls(self._node)
        return model

    @ParamRootFactory.add_one('group')
    def add_group(self, name=None, parent_path=None, param_path=None, *args, **kwargs):
        model = _Group(self._node)
        return model

    @ParamRootFactory.add_one()
    def add_string(self, name=None, parent_path=None, param_path=None, *args, **kwargs):
        model = _String(self._node)
        return model

    @ParamRootFactory.add_one()
    def add_integer(self, name=None, parent_path=None, param_path=None, *args, **kwargs):
        model = _Integer(self._node)
        return model

    @ParamRootFactory.add_one()
    def add_boolean(self, name=None, parent_path=None, param_path=None, *args, **kwargs):
        model = _Boolean(self._node)
        return model

    @ParamRootFactory.add_one()
    def add_integer_array(self, name=None, parent_path=None, param_path=None, *args, **kwargs):
        model = _IntegerArray(self._node)
        return model

    @ParamRootFactory.add_one()
    def add_integer_array(self, name=None, parent_path=None, param_path=None, *args, **kwargs):
        model = _IntegerArray(self._node)
        return model

    @ParamRootFactory.add_one()
    def add_string_array(self, name=None, parent_path=None, param_path=None, *args, **kwargs):
        model = _StringArray(self._node)
        return model

    def get_parameters(self):
        return list(self._dict.values())

    def get_parameter(self, param_path):
        return self._dict.get(param_path)
    
    def _add_parameter_by_data(self, data):
        param_path = data['param_path']
        type_name = data['type']
        if type_name == 'group':
            self.add_group(
                param_path=param_path
            ).set_options(**data['options'])
        else:
            self.add_auto(
                type_name=type_name,
                param_path=param_path,
                value=data['value']
            ).set_options(**data['options'])

