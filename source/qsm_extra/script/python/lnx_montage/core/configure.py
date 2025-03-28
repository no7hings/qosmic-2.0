# coding:utf-8
import lxbasic.content as bsc_content


class MtgConfigure(bsc_content.Configure):
    INSTANCE = None

    class AtrKeys:
        Root = [
            'translateX', 'translateY', 'translateZ',
            'rotateX', 'rotateY', 'rotateZ'
        ]
        Default = [
            'rotateX', 'rotateY', 'rotateZ'
        ]

    class Namespaces:
        Transfer = 'transfer'

    def __init__(self, *args, **kwargs):
        super(MtgConfigure, self).__init__(*args, **kwargs)

    def __new__(cls, *args, **kwargs):
        if cls.INSTANCE is not None:
            return cls.INSTANCE

        self = super(MtgConfigure, cls).__new__(cls)
        self._content = self.generate_local_configure()
        self._sketch_key_dict = {}
        self._all_sketch_key_list = []
        self._basic_sketch_key_list = []
        self._extra_sketch_key_dict = {}
        self._control_key_dict = {}
        self._adv_sketch_key_dict = {}
        self._mocap_sketch_key_dict = {}
        for k, v in self._content.get('sketches').items():
            i_sketch_key = v['key']
            self._sketch_key_dict[k] = i_sketch_key
            self._all_sketch_key_list.append(i_sketch_key)
            i_basic_flag = v.get('basic')
            if i_basic_flag is True:
                self._basic_sketch_key_list.append(i_sketch_key)

            i_extra_key = v.get('extra')
            if i_extra_key:
                self._extra_sketch_key_dict[k] = i_extra_key

            i_control_key = v.get('control')
            if i_control_key:
                self._control_key_dict[k] = i_control_key

            i_adv_sketch_key = v.get('adv_key')
            if i_adv_sketch_key:
                self._adv_sketch_key_dict[k] = i_adv_sketch_key

            i_mocap_sketch_key = v.get('mocap_key')
            if i_mocap_sketch_key:
                self._mocap_sketch_key_dict[k] = i_mocap_sketch_key

        self._root_sketch_key = self._sketch_key_dict['Root_M']
        cls.INSTANCE = self
        return self

    @property
    def all_sketch_keys(self):
        return self._all_sketch_key_list

    @property
    def basic_sketch_keys(self):
        return self._basic_sketch_key_list

    @property
    def extra_sketch_key_query(self):
        return self._extra_sketch_key_dict

    @property
    def control_key_query(self):
        return self._control_key_dict

    @property
    def adv_sketch_key_query(self):
        return self._adv_sketch_key_dict

    @property
    def mocap_sketch_key_query(self):
        return self._mocap_sketch_key_dict

    @property
    def root_sketch_key(self):
        return self._root_sketch_key

    def get_sketch_key(self, key):
        return self._sketch_key_dict[key]

    def __str__(self):
        return bsc_content.ToString(
            self._content.get_value()
        ).generate()
