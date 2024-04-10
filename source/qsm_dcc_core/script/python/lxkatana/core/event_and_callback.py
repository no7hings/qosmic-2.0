# coding:utf-8
import fnmatch

import lxbasic.log as bsc_log
# katana
from .wrap import *

from . import node as ktn_cor_node


class EventOpt(object):
    KEY = 'event'

    class EventType(object):
        NodeCreate = 'node_create'

    #
    def __init__(self, handler, event_type):
        self._handler = handler
        self._event_type = event_type

    def register(self):
        self.deregister()
        #
        Utils.EventModule.RegisterEventHandler(
            handler=self._handler,
            eventType=self._event_type,
            enabled=True
        )
        #
        bsc_log.Log.trace_method_result(
            self.KEY,
            'register for "{}"'.format(self._event_type)
        )

    def deregister(self):
        if self.get_is_register() is True:
            Utils.EventModule.UnregisterEventHandler(
                handler=self._handler,
                eventType=self._event_type
            )
            bsc_log.Log.trace_method_result(
                self.KEY,
                'deregister for "{}"'.format(self._event_type)
            )

    def get_is_register(self):
        return Utils.EventModule.IsHandlerRegistered(
            handler=self._handler,
            eventType=self._event_type
        )


class CallbackOpt(object):
    KEY = 'callback'

    def __init__(self, function, callback_type):
        self._function = function
        self._callback_type = callback_type

    def append(self):
        bsc_log.Log.trace_method_result(
            self.KEY,
            'register for "{}"'.format(self._callback_type)
        )
        Callbacks.addCallback(
            callbackType=self._callback_type,
            callbackFcn=self._function
        )

    def deregister(self):
        bsc_log.Log.trace_method_result(
            self.KEY,
            'deregister for "{}"'.format(self._callback_type)
        )
        Callbacks.delCallback(
            callbackType=self._callback_type,
            callbackFcn=self._function
        )


class EventMtd(object):
    @classmethod
    def get_all_event_types(cls):
        pass

    # noinspection PyUnusedLocal
    @classmethod
    def set_port_value(cls, *args, **kwargs):
        event_type, event_id = args
        ktn_obj = kwargs['node']
        ktn_port = kwargs['param']
        ktn_obj_opt = ktn_cor_node.NGNodeOpt(ktn_obj)
        if ktn_obj_opt.type == 'ArnoldShadingNode':
            shader_type_name = ktn_obj_opt.get_port_raw('nodeType')
            if shader_type_name in ['ramp_rgb', 'ramp_float']:
                ktn_port_opt = ktn_cor_node.NGPortOpt(ktn_port)
                if fnmatch.filter([ktn_port_opt.path], '*.parameters.ramp_Knots.value.*'):
                    cls.set_arnold_ramp_write(ktn_obj_opt)
                elif fnmatch.filter([ktn_port_opt.path], '*.parameters.ramp_Floats.value.*'):
                    cls.set_arnold_ramp_write(ktn_obj_opt)
                elif fnmatch.filter([ktn_port_opt.path], '*.parameters.ramp_Colors.value.*'):
                    cls.set_arnold_ramp_write(ktn_obj_opt)

    # noinspection PyUnusedLocal
    @classmethod
    def set_port_connect(cls, *args, **kwargs):
        event_type, event_id = args
        source = kwargs['portA']
        target = kwargs['portB']
        ktn_obj = target.getNode()
        ktn_obj_opt = ktn_cor_node.NGNodeOpt(ktn_obj)
        if ktn_obj_opt:
            if ktn_obj_opt.type == 'ArnoldShadingNode':
                shader_type_name = ktn_obj_opt.get_port_raw('nodeType')
                if shader_type_name in ['ramp_rgb', 'ramp_float']:
                    cls.set_arnold_ramp_read(ktn_obj_opt)

    # noinspection PyUnusedLocal
    @classmethod
    def set_port_disconnect(cls, *args, **kwargs):
        event_type, event_id = args
        source = kwargs['portA']
        target = kwargs['portB']
        ktn_obj = target.getNode()
        ktn_obj_opt = ktn_cor_node.NGNodeOpt(ktn_obj)
        if ktn_obj_opt:
            if ktn_obj_opt.type == 'ArnoldShadingNode':
                shader_type_name = ktn_obj_opt.get_port_raw('nodeType')
                if shader_type_name in ['ramp_rgb', 'ramp_float']:
                    cls.set_arnold_ramp_read(ktn_obj_opt)

    # noinspection PyUnusedLocal
    @classmethod
    def set_node_create(cls, *args, **kwargs):
        event_type, event_id = args
        ktn_obj = kwargs['node']
        ktn_obj_opt = ktn_cor_node.NGNodeOpt(ktn_obj)
        if ktn_obj_opt.type == 'ArnoldShadingNode':
            shader_type_name = ktn_obj_opt.get_port_raw('nodeType')
            if shader_type_name in ['ramp_rgb', 'ramp_float']:
                cls.set_arnold_ramp_read(ktn_obj_opt)
            #
            cls._set_arnold_obj_name_update_(ktn_obj_opt)

    # noinspection PyUnusedLocal
    @classmethod
    def set_node_edit(cls, *args, **kwargs):
        event_type, event_id = args
        ktn_obj = kwargs['node']
        ktn_obj_opt = ktn_cor_node.NGNodeOpt(ktn_obj)
        if ktn_obj_opt.type == 'ArnoldShadingNode':
            shader_type_name = ktn_obj_opt.get_port_raw('nodeType')
            if shader_type_name in ['ramp_rgb', 'ramp_float']:
                cls.set_arnold_ramp_read(ktn_obj_opt)

    @classmethod
    def set_arnold_ramp_write(cls, ktn_obj_opt):
        cls._set_arnold_ramp_write_(ktn_obj_opt)
        # bsc_log.Log.trace_method_result(
        #     'ramp-write',
        #     'obj-name="{}"'.format(ktn_obj_opt.name)
        # )

    @classmethod
    def _set_arnold_ramp_write_(cls, ktn_obj_opt):
        # noinspection PyUnresolvedReferences
        # key = sys._getframe().f_code.co_name
        # Utils.UndoStack.OpenGroup(key)
        #
        ramp_value_dict = {}
        shader_type_name = ktn_obj_opt.get_port_raw('nodeType')
        if shader_type_name == 'ramp_rgb':
            keys = ['ramp', 'ramp_Knots', 'ramp_Interpolation', 'ramp_Colors']
        elif shader_type_name == 'ramp_float':
            keys = ['ramp', 'ramp_Knots', 'ramp_Interpolation', 'ramp_Floats']
        else:
            raise
        for i_key in keys:
            value_port_path = 'parameters.{}.value'.format(i_key)
            value = ktn_obj_opt.get_port_raw(value_port_path)
            #
            ramp_value_dict[i_key] = value
            i_port_path = 'lx_ramp_value'
            i_ktn_port = ktn_obj_opt.get_port(i_port_path)
            if i_ktn_port is None:
                ktn_obj_opt.create_port(i_port_path, 'string', str(ramp_value_dict))
            else:
                i_ktn_port_opt = ktn_cor_node.NGPortOpt(i_ktn_port)
                i_ktn_port_opt.set(str(ramp_value_dict))
        #
        # Utils.UndoStack.CloseGroup()

    @classmethod
    def set_arnold_ramp_read(cls, ktn_obj_opt):
        def fnc_():
            cls._set_arnold_ramp_read_(ktn_obj_opt)
            # bsc_log.Log.trace_method_result(
            #     'ramp-read',
            #     'obj-name="{}"'.format(ktn_obj_opt.name)
            # )

        #
        import threading

        timer = threading.Timer(1, fnc_)
        timer.start()

    @classmethod
    def _set_arnold_ramp_read_(cls, ktn_obj_opt):
        # noinspection PyUnresolvedReferences
        # key = sys._getframe().f_code.co_name
        # Utils.UndoStack.OpenGroup(key)
        #
        ramp_value_port = ktn_obj_opt.get_port('lx_ramp_value')
        if ramp_value_port is not None:
            ramp_value_port_opt = ktn_cor_node.NGPortOpt(ramp_value_port)
            ramp_value_dict = eval(ramp_value_port_opt.get() or '{}')
            for key, value in ramp_value_dict.items():
                enable_port_path = 'parameters.{}.enable'.format(key)
                value_port_path = 'parameters.{}.value'.format(key)
                ktn_obj_opt.set_port_raw(enable_port_path, 1)
                ktn_obj_opt.set_port_raw(value_port_path, value)
        #
        # Utils.UndoStack.CloseGroup()

    @classmethod
    def _set_arnold_obj_name_update_(cls, ktn_obj_opt):
        # noinspection PyUnresolvedReferences
        # key = sys._getframe().f_code.co_name
        # Utils.UndoStack.OpenGroup(key)
        #
        # shader_obj_name = ktn_obj_opt.get_port_raw('name')
        obj_name = ktn_obj_opt.name
        ktn_obj = ktn_obj_opt.ktn_obj
        if ktn_obj.isRenameAllowed() is True:
            if ktn_obj.isAutoRenameAllowed() is False:
                ktn_obj_opt.set_port_raw('name', obj_name)
                ktn_obj.setAutoRenameAllowed(True)
        #
        # Utils.UndoStack.CloseGroup()

    @classmethod
    def set_events_register(cls):
        ss = [
            (cls.set_port_value, 'parameter_setValue'),
            (cls.set_port_connect, 'port_connect'),
            (cls.set_port_disconnect, 'port_disconnect'),
            (cls.set_node_create, 'node_create'),
            (cls.set_node_edit, 'node_setEdited')
        ]
        #
        for handler, event_type in ss:
            event_opt = EventOpt(handler=handler, event_type=event_type)
            event_opt.register()


# noinspection PyUnusedLocal
class CallbackMtd(object):
    @classmethod
    def set_scene_load(cls, *args, **kwargs):
        # {'filename': '/data/f/event_test.katana', 'objectHash': None}
        # file_path = kwargs['filename']
        _ = NodegraphAPI.GetAllNodesByType('ArnoldShadingNode') or []

        for ktn_obj in _:
            ktn_obj_opt = ktn_cor_node.NGNodeOpt(ktn_obj)
            shader_type_name = ktn_obj_opt.get_port_raw('nodeType')
            if shader_type_name in ['ramp_rgb', 'ramp_float']:
                # noinspection PyBroadException
                try:
                    EventMtd.set_arnold_ramp_write(ktn_obj_opt)
                except Exception:
                    print ktn_obj_opt.name

    @classmethod
    def add_arnold_callbacks(cls):
        ss = [
            (cls.set_scene_load, Callbacks.Type.onSceneLoad),
        ]
        for function, callback_type in ss:
            callback_opt = CallbackOpt(function=function, callback_type=callback_type)
            callback_opt.append()

    # noinspection PyUnusedLocal
    @classmethod
    def add_callbacks(cls, data):
        for function, callback_type in data:
            pass

    @classmethod
    def add_as_startup_complete(cls, fnc):
        callback_opt = CallbackOpt(function=fnc, callback_type=Callbacks.Type.onStartupComplete)
        callback_opt.append()

    @classmethod
    def add_as_scene_new(cls, fnc):
        callback_opt = CallbackOpt(function=fnc, callback_type=Callbacks.Type.onNewScene)
        callback_opt.append()

    @classmethod
    def add_as_scene_open(cls, fnc):
        callback_opt = CallbackOpt(function=fnc, callback_type=Callbacks.Type.onSceneLoad)
        callback_opt.append()

    @classmethod
    def add_as_scene_save(cls, fnc):
        callback_opt = CallbackOpt(function=fnc, callback_type=Callbacks.Type.onSceneSave)
        callback_opt.append()

    @classmethod
    def add_as_render_setup(cls, fnc):
        callback_opt = CallbackOpt(function=fnc, callback_type=Callbacks.Type.onRenderSetup)
        callback_opt.append()
