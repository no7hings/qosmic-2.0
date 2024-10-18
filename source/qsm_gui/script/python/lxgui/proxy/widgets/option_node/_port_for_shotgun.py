# coding:utf-8
import _port_base

import _input_for_shotgun


# shotgun
class PrxPortForShotgunEntity(_port_base.AbsPrxPort):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_shotgun.PrxInputForShotgunEntityChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortForShotgunEntity, self).__init__(*args, **kwargs)

    def get_stg_entity(self):
        return self._prx_port_input.get_stg_entity()

    def set_name(self, *args, **kwargs):
        super(PrxPortForShotgunEntity, self).set_name(*args, **kwargs)
        self.get_input_widget()._set_name_text_(args[0])

    def append(self, value):
        self._prx_port_input.append(value)

    def set_shotgun_entity_kwargs(self, *args, **kwargs):
        self._prx_port_input.set_shotgun_entity_kwargs(*args, **kwargs)

    def run_build_extra_use_thread(self, cache_fnc, build_fnc, post_fnc):
        self._prx_port_input.run_build_extra_use_thread(
            cache_fnc, build_fnc, post_fnc
        )


class PrxPortForShotgunEntities(_port_base.AbsPrxPort):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_shotgun.PrxInputForShotgunEntitiesChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortForShotgunEntities, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortForShotgunEntities, self).set_name(*args, **kwargs)
        self.get_input_widget()._set_name_text_(args[0])
        self.get_input_widget()._get_entry_widget_()._set_empty_text_(args[0])

    def append(self, value):
        self._prx_port_input.append(value)

    def set_shotgun_entity_kwargs(self, *args, **kwargs):
        self._prx_port_input.set_shotgun_entity_kwargs(*args, **kwargs)

    def run_build_extra_use_thread(self, cache_fnc, build_fnc, post_fnc):
        self._prx_port_input.run_build_extra_use_thread(
            cache_fnc, build_fnc, post_fnc
        )
