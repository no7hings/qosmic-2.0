# coding:utf-8
import collections

import copy

import lxresource as bsc_resource

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage


class _AbsTxrBase(object):
    INSTANCE = None

    @classmethod
    def generate_instance(cls):
        if cls.INSTANCE is not None:
            return cls.INSTANCE
        cls.INSTANCE = cls()
        return cls.INSTANCE

    def __init__(self, configure):
        self._configure = configure
        self._build()

    def _build(self):
        raise NotImplementedError()

    def __str__(self):
        return self._configure.__str__()


class TxrMethodForBuild(_AbsTxrBase):
    CONTENT = None

    NAME_PATTERNS = [
        '{name}.{type}.<udim>.####.{format}',
        '{name}.{type}.<udim>.{format}',
        '{name}.{type}.{format}'
    ]

    @classmethod
    def _generate_content(cls):
        if cls.CONTENT is not None:
            return cls.CONTENT
        cls.CONTENT = bsc_resource.RscExtendConfigure.get_as_content('texture/build')
        cls.CONTENT.do_flatten()
        return cls.CONTENT

    @staticmethod
    def _generate_texture_data(directory_path, p, variants, mapper):
        dict_ = collections.OrderedDict()
        for i_type, i_v in mapper.items():
            for j_keyword in i_v:
                j_variants = copy.copy(variants)
                j_variants['type'] = j_keyword
                j_file_name = p.format(**j_variants)
                j_file_path = '{}/{}'.format(directory_path, j_file_name)
                if bsc_storage.StgFileMtdForMultiply.get_is_exists(j_file_path) is True:
                    dict_.setdefault(i_type, []).append(j_file_path)
        return dict_

    def _build(self):
        self._keyword_mapper = collections.OrderedDict()
        all_texture_types = self._configure.get_key_names_at('default')
        for i_texture_type in all_texture_types:
            i_ks = self._configure.get('default.{}.keywords'.format(i_texture_type))
            self._keyword_mapper[i_texture_type] = i_ks

    def __init__(self):
        super(TxrMethodForBuild, self).__init__(
            self._generate_content()
        )

    @classmethod
    def _generate_match_args(cls, file_opt):
        for i_p in cls.NAME_PATTERNS:
            i_p_0 = i_p.replace('{name}.{type}', '*')
            i_p_0 = i_p_0.format(format=file_opt.get_format())
            i_number_args = bsc_storage.StgFileMtdForMultiply.get_number_args(file_opt.get_name(), i_p_0)
            if i_number_args:
                i_file_name, _ = i_number_args
                return i_file_name, i_p
        return file_opt.get_name(), cls.NAME_PATTERNS[-1]

    def generate_all_texture_args(self, file_path):
        file_opt = bsc_storage.StgFileOpt(file_path)
        if file_opt.get_is_exists():
            file_name, p = self._generate_match_args(file_opt)
            p_opt = bsc_core.PtnParseOpt(p)
            variants = p_opt.get_variants(file_name)
            return variants['name'], self._generate_texture_data(
                file_opt.get_directory_path(),
                p,
                variants,
                self._keyword_mapper
            )

    def generate_one_texture_args(self, file_path):
        file_opt = bsc_storage.StgFileOpt(file_path)
        if file_opt.get_is_exists():
            file_name, p = self._generate_match_args(file_opt)
            p_opt = bsc_core.PtnParseOpt(p)
            variants = p_opt.get_variants(file_name)
            return variants['name'], variants['type'], '{}/{}'.format(file_opt.get_directory_path(), file_name)

    def get_all_texture_types(self):
        return self._keyword_mapper.keys()

    def get_usd_includes(self):
        return copy.copy(self._configure.get('usd.includes'))

    def get_usd_mapper(self):
        return copy.copy(self._configure.get('usd.mapper'))

    def get_arnold_includes(self):
        return copy.copy(self._configure.get('arnold.includes'))

    def get_arnold_mapper(self):
        return copy.copy(self._configure.get('arnold.mapper'))


class TxrMethodForColorSpaceAsAces(_AbsTxrBase):
    CONTENT = None
    INSTANCE = None

    @classmethod
    def _generate_content(cls):
        if cls.CONTENT is not None:
            return cls.CONTENT
        cls.CONTENT = bsc_resource.RscExtendConfigure.get_as_content('texture/color-space/aces')
        cls.CONTENT.do_flatten()
        return cls.CONTENT

    @classmethod
    def get_is_enable(cls):
        return bsc_core.EnvBaseMtd.get('OCIO') is not None

    def _build(self):
        self._convert_dict = self._configure.get('aces.convert')

    def __init__(self):
        super(TxrMethodForColorSpaceAsAces, self).__init__(
            self._generate_content()
        )

    def get_all_color_spaces(self):
        return self._configure.get('aces.color-spaces')

    def get_default_color_space(self):
        return self._configure.get('aces.default-color-space')

    def get_ocio_file(self):
        _ = bsc_core.EnvBaseMtd.get('OCIO')
        if _ is not None:
            return _
        return self._configure.get('aces.file')

    def to_aces_color_space(self, color_space):
        if self.get_is_enable() is True:
            return self._convert_dict[color_space]
        return color_space


class TxrMethodForColorSpaceAsTxConvert(_AbsTxrBase):
    CONTENT = None
    INSTANCE = None

    @classmethod
    def _generate_content(cls):
        if cls.CONTENT is not None:
            return cls.CONTENT
        cls.CONTENT = bsc_resource.RscExtendConfigure.get_as_content('texture/color-space/convert')
        cls.CONTENT.do_flatten()
        return cls.CONTENT

    def _build(self):
        self._keys = []
        self._color_space_dict = {}
        self._purpose_dict = {}
        keys = self._configure.get_key_names_at('tx')
        for i_key in keys:
            i_ps = self._configure.get('tx.{}.name-patterns'.format(i_key))
            i_color_space = self._configure.get('tx.{}.color-space'.format(i_key))
            for j_p in i_ps:
                self._color_space_dict[j_p] = i_color_space
                self._purpose_dict[j_p] = i_key

    def __init__(self):
        super(TxrMethodForColorSpaceAsTxConvert, self).__init__(
            self._generate_content()
        )

    def get_name_patterns(self):
        return self._color_space_dict.keys()

    def get_color_space_mapper(self):
        return self._color_space_dict

    def get_tx_color_space_input(self, file_path):
        file_opt = bsc_storage.StgFileOpt(file_path)
        _ = 'auto'
        # check is match configure, when not use "auto"
        for i_name_pattern in self.get_name_patterns():
            if file_opt.get_is_match_name_pattern(i_name_pattern) is True:
                _ = self._color_space_dict[i_name_pattern]
                break
        # when tag is "auto"
        if _ == 'auto':
            import lxarnold.core as and_core
            return and_core.AndTextureOpt(file_path).get_color_space()
        return _

    @classmethod
    def get_exr_color_space_input(cls, file_path):
        import lxarnold.core as and_core
        return and_core.AndTextureOpt(file_path).get_color_space()

    def get_purpose(self, file_path):
        file_opt = bsc_storage.StgFileOpt(file_path)
        for i_name_pattern in self.get_name_patterns():
            if file_opt.get_is_match_name_pattern(i_name_pattern) is True:
                return self._purpose_dict[i_name_pattern]
        return 'unknown'
