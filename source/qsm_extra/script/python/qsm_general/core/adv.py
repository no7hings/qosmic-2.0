# coding:utf-8
import lxbasic.resource as bsc_resource


class AdvCharacterControlConfigure(object):
    def __init__(self):
        self._cfg = bsc_resource.BscExtendConfigure.get_as_content('gui/adv-character-control')
        self._body_control_tree_cfg = self._cfg.get_as_content('body_control_tree')
        self._body_control_map_cfg = self._cfg.get_as_content('body_control_map')
    
    def find_next_keys_at(self, key):
        key_paths = self._body_control_tree_cfg.get_keys('*.{}.*'.format(key))
        return set([x.split('.')[-1] for x in key_paths])
    
    def get_control_keys_at(self, key, branch):
        return self._body_control_map_cfg.get(key+'.'+branch) or []
    
    def get_default_control_keys_at(self, key):
        return self.get_control_keys_at(key, 'default')

    def get_extra_control_keys_at(self, key):
        return self.get_control_keys_at(key, 'extra')

    def get_body_all_curve_control_keys(self):
        return self._cfg.get('body_control_keys')
    
    def get_face_all_curve_control_keys(self):
        return self._cfg.get('face_control_keys')

    def get_all_curve_control_keys(self):
        return self.get_body_all_curve_control_keys() + self.get_face_all_curve_control_keys()
