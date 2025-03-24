# coding:utf-8
import lxbasic.core as bsc_core

from ...core import base as _scn_cor_base

from ..core import event as _cor_event

from ..core import undo as _cor_undo


# parameters
class _AbsParam(_scn_cor_base._ParamBase):
    def __init__(self, *args, **kwargs):
        super(_AbsParam, self).__init__(*args, **kwargs)

        self._data.options = _scn_cor_base._Dict(
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
class GroupParam(_AbsParam):
    PARAM_TYPE = _scn_cor_base.ParamTypes.Group

    def __init__(self, *args, **kwargs):
        super(GroupParam, self).__init__(*args, **kwargs)

        self._data.type = self.PARAM_TYPE

        self._data.options.widget = 'group'


class CustomParam(_AbsParam):
    PARAM_TYPE = _scn_cor_base.ParamTypes.Custom

    def __init__(self, *args, **kwargs):
        super(CustomParam, self).__init__(*args, **kwargs)

        self._data.type = self.PARAM_TYPE

        self._data.options.widget = 'button'

    def set_value(self, value):
        pass

    def get_value(self):
        pass

    def _exec_script(self):
        script = self.options.get('script')
        if script:
            # noinspection PyUnusedLocal
            node = self.node
            # noinspection PyRedundantParentheses
            exec (script)


class _AbsTypedParam(_AbsParam):
    def __init__(self, *args, **kwargs):
        super(_AbsTypedParam, self).__init__(*args, **kwargs)

        self._data.category = None
        self._data.value = None
        self._data.default = None

    @_cor_event.EventFactory.send(_cor_event.EventTypes.ParamSetValue)
    def set_value(self, value):
        return self._set_value(value)
    
    @_cor_undo.GuiUndoFactory.push(_cor_undo.UndoActions.ParamSetValue)
    def set_value(self, value):
        def _redo_fnc():
            self._set_value_evt(value)
        
        def _undo_fnc():
            self._set_value_evt(value_old)

        value_old = self._data.value

        return self.get_node().root_model.undo_stack, _redo_fnc, _undo_fnc
    
    @_cor_event.EventFactory.send(_cor_event.EventTypes.ParamSetValue)
    def _set_value_evt(self, value):
        return self._set_value(value)

    # for gui
    def _set_value(self, value):
        if value != self._data.value:
            self._data.value = value
            return True
        return False

    def get_value(self):
        return self._data.value

    def set_default(self, value):
        self._data.default = value

    def get_default(self):
        return self._data.default


class StringParam(_AbsTypedParam):
    PARAM_TYPE = _scn_cor_base.ParamTypes.String

    def __init__(self, *args, **kwargs):
        super(StringParam, self).__init__(*args, **kwargs)

        self._data.category = 'constant'
        self._data.type = self.PARAM_TYPE

        self._data.value = ''
        self._data.default = ''

        self._data.options.widget = 'string'


class IntegerParam(_AbsTypedParam):
    PARAM_TYPE = _scn_cor_base.ParamTypes.Integer

    def __init__(self, *args, **kwargs):
        super(IntegerParam, self).__init__(*args, **kwargs)

        self._data.category = 'constant'
        self._data.type = self.PARAM_TYPE

        self._data.value = 0
        self._data.default = 0

        self._data.options.widget = 'integer'


class FloatParam(_AbsTypedParam):
    PARAM_TYPE = _scn_cor_base.ParamTypes.Float

    def __init__(self, *args, **kwargs):
        super(FloatParam, self).__init__(*args, **kwargs)

        self._data.category = 'constant'
        self._data.type = self.PARAM_TYPE

        self._data.value = 0.0
        self._data.default = 0.0

        self._data.options.widget = 'float'


class BooleanParam(_AbsTypedParam):
    PARAM_TYPE = _scn_cor_base.ParamTypes.Boolean

    def __init__(self, *args, **kwargs):
        super(BooleanParam, self).__init__(*args, **kwargs)

        self._data.category = 'constant'
        self._data.type = self.PARAM_TYPE

        self._data.value = False
        self._data.default = False

        self._data.options.widget = 'checkbox'


class StringArrayParam(_AbsTypedParam):
    PARAM_TYPE = _scn_cor_base.ParamTypes.StringArray

    def __init__(self, *args, **kwargs):
        super(StringArrayParam, self).__init__(*args, **kwargs)

        self._data.category = 'array'
        self._data.type = self.PARAM_TYPE
        self._data.value = []
        self._data.default = []

        self._data.options.widget = 'default'


class IntegerArrayParam(_AbsTypedParam):
    PARAM_TYPE = _scn_cor_base.ParamTypes.IntegerArray

    def __init__(self, *args, **kwargs):
        super(IntegerArrayParam, self).__init__(*args, **kwargs)

        self._data.category = 'array'
        self._data.type = self.PARAM_TYPE
        self._data.value = []
        self._data.default = []

        self._data.options.widget = 'default'


class FloatArrayParam(_AbsTypedParam):
    PARAM_TYPE = _scn_cor_base.ParamTypes.FloatArray

    def __init__(self, *args, **kwargs):
        super(FloatArrayParam, self).__init__(*args, **kwargs)

        self._data.type = self.PARAM_TYPE
        self._data.value = []
        self._data.default = []

        self._data.options.widget = 'default'


class DictParam(_AbsTypedParam):
    PARAM_TYPE = _scn_cor_base.ParamTypes.Dict

    def __init__(self, *args, **kwargs):
        super(DictParam, self).__init__(*args, **kwargs)

        self._data.category = 'other'
        self._data.type = self.PARAM_TYPE
        self._data.value = {}
        self._data.default = {}

        self._data.options.widget = 'default'


class ParamRootFactory:
    @staticmethod
    def add(scheme='typed'):
        def decorator(fnc):
            if scheme == 'typed':
                def wrapper(param_root, name=None, parent_path=None, param_path=None, *args, **kwargs):
                    prefix = name or scheme
                    param_path = param_root._generate_param_path(
                        name=name,
                        parent_path=parent_path,
                        param_path=param_path,
                        prefix=prefix
                    )
                    if param_path in param_root._dict:
                        return param_root._dict[param_path]

                    model = fnc(param_root, name, parent_path, param_path, *args, **kwargs)

                    param_root._dict[param_path] = model

                    port_path_opt = bsc_core.BscPortPathOpt(param_path)

                    name = port_path_opt.get_name()

                    model._set_param_path(param_path)
                    model.set_name(name)
                    model.set_gui_name(bsc_core.BscText.to_prettify(name))

                    if 'value' in kwargs:
                        model._set_value(kwargs['value'])
                    return model
                return wrapper
            elif scheme == 'group':
                def wrapper(param_root, name=None, parent_path=None, param_path=None, *args, **kwargs):
                    prefix = name or scheme
                    param_path = param_root._generate_param_path(
                        name=name,
                        parent_path=parent_path,
                        param_path=param_path,
                        prefix=prefix
                    )

                    if param_path in param_root._dict:
                        return param_root._dict[param_path]

                    model = fnc(param_root, name, parent_path, param_path, *args, **kwargs)
                    param_root._dict[param_path] = model
                    port_path_opt = bsc_core.BscPortPathOpt(param_path)

                    name = port_path_opt.get_name()

                    model._set_param_path(param_path)
                    model.set_name(name)
                    model.set_gui_name(bsc_core.BscText.to_prettify(name))

                    return model
                return wrapper
            elif scheme == 'auto':
                def wrapper(param_root, type_name, name=None, parent_path=None, param_path=None, *args, **kwargs):
                    prefix = name or scheme
                    param_path = param_root._generate_param_path(
                        name=name,
                        parent_path=parent_path,
                        param_path=param_path,
                        prefix=prefix
                    )

                    model = fnc(param_root, type_name, name, parent_path, param_path, *args, **kwargs)

                    param_root._dict[param_path] = model

                    port_path_opt = bsc_core.BscPortPathOpt(param_path)

                    name = port_path_opt.get_name()

                    model._set_param_path(param_path)
                    model.set_name(name)
                    model.set_gui_name(bsc_core.BscText.to_prettify(name))

                    if 'value' in kwargs:
                        model._set_value(kwargs['value'])
                    return model
                return wrapper
            else:
                raise RuntimeError()
        return decorator


class ParamRoot(_scn_cor_base._Base):
    PARAM_CLS_MAP = {
        GroupParam.PARAM_TYPE: GroupParam,
        CustomParam.PARAM_TYPE: CustomParam,

        StringParam.PARAM_TYPE: StringParam,
        IntegerParam.PARAM_TYPE: IntegerParam,
        FloatParam.PARAM_TYPE: FloatParam,
        BooleanParam.PARAM_TYPE: BooleanParam,

        StringArrayParam.PARAM_TYPE: StringArrayParam,
        IntegerArrayParam.PARAM_TYPE: IntegerArrayParam,
        FloatArrayParam.PARAM_TYPE: FloatArrayParam,

        DictParam.PARAM_TYPE: DictParam,
    }

    def __init__(self, node, data):
        self._node = node

        self._dict = data

    def get_root_model(self):
        return self._node.root_model

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

    @ParamRootFactory.add('auto')
    def create_auto(self, type_name, name=None, parent_path=None, param_path=None, *args, **kwargs):
        param_cls = self.PARAM_CLS_MAP[type_name]
        model = param_cls(self.get_root_model(), self.get_node_path())
        return model

    @ParamRootFactory.add('group')
    def add_group(self, name=None, parent_path=None, param_path=None, *args, **kwargs):
        model = GroupParam(self.get_root_model(), self.get_node_path())
        return model

    @ParamRootFactory.add('typed')
    def add_custom(self, name=None, parent_path=None, param_path=None, *args, **kwargs):
        model = CustomParam(self.get_root_model(), self.get_node_path())
        return model

    @ParamRootFactory.add('typed')
    def create_string(self, name=None, parent_path=None, param_path=None, *args, **kwargs):
        model = StringParam(self.get_root_model(), self.get_node_path())
        return model

    @ParamRootFactory.add('typed')
    def create_integer(self, name=None, parent_path=None, param_path=None, *args, **kwargs):
        model = IntegerParam(self.get_root_model(), self.get_node_path())
        return model

    @ParamRootFactory.add('typed')
    def add_boolean(self, name=None, parent_path=None, param_path=None, *args, **kwargs):
        model = BooleanParam(self.get_root_model(), self.get_node_path())
        return model

    @ParamRootFactory.add('typed')
    def create_integer_array(self, name=None, parent_path=None, param_path=None, *args, **kwargs):
        model = IntegerArrayParam(self.get_root_model(), self.get_node_path())
        return model

    @ParamRootFactory.add('typed')
    def create_integer_array(self, name=None, parent_path=None, param_path=None, *args, **kwargs):
        model = IntegerArrayParam(self.get_root_model(), self.get_node_path())
        return model

    @ParamRootFactory.add('typed')
    def create_string_array(self, name=None, parent_path=None, param_path=None, *args, **kwargs):
        model = StringArrayParam(self.get_root_model(), self.get_node_path())
        return model

    @ParamRootFactory.add('typed')
    def add_dict(self, name=None, parent_path=None, param_path=None, *args, **kwargs):
        model = DictParam(self.get_root_model(), self.get_node_path())
        return model

    def get_parameters(self):
        return list(self._dict.values())

    def get_parameter(self, param_path):
        return self._dict.get(param_path)
    
    def _add_parameter_by_data(self, data):
        param_path = data['param_path']
        type_name = data['type']
        kwargs = dict(
            type_name=type_name,
            param_path=param_path,
        )
        if 'value' in data:
            kwargs['value'] = data['value']

        self.create_auto(**kwargs).set_options(**data['options'])

