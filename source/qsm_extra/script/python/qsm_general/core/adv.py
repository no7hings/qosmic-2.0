# coding:utf-8
import lxbasic.resource as bsc_resource


class AdvControlConfigure(object):
    def __init__(self):
        self._cfg = bsc_resource.RscExtendConfigure.get_as_content('gui/adv-picker')
        self._control_tree_cfg = self._cfg.get_as_content('control_tree')
        self._control_map_cfg = self._cfg.get_as_content('control_map')
    
    def find_next_keys_at(self, key):
        key_paths = self._control_tree_cfg.get_keys('*.{}.*'.format(key))
        return set([x.split('.')[-1] for x in key_paths])
    
    def get_control_keys_at(self, key, branch):
        return self._control_map_cfg.get(key+'.'+branch) or []
    
    def get_default_control_keys_at(self, key):
        return self.get_control_keys_at(key, 'default')

    def get_extra_control_keys_at(self, key):
        return self.get_control_keys_at(key, 'extra')
