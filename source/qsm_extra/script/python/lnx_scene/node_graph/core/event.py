# coding:utf-8
import enum

from ...core import base as _scn_cor_base


class EventTypes(enum.IntEnum):
    NodeSetEdited = 0x00

    PortConnect = 0x10
    PortDisconnect = 0x11
    ParamSetValue = 0x12


class EventFactory:
    @staticmethod
    def send(event_type):
        def decorator(fnc):
            def wrapper(entity, *args, **kwargs):
                result = fnc(entity, *args, **kwargs)
                if entity.ENTITY_TYPE == _scn_cor_base.EntityTypes.Parameter:
                    entity.root_model._event_sent(
                        event_type, 0,
                        dict(
                            event_id=0,
                            node=entity.get_node().get_path(),
                            param=entity.get_param_path()
                        )
                    )
                elif entity.ENTITY_TYPE == _scn_cor_base.EntityTypes.Node:
                    entity.root_model._event_sent(
                        event_type, 0,
                        dict(
                            event_id=0,
                            node=entity.get_path(),
                        )
                    )
                return result
            return wrapper
        return decorator
