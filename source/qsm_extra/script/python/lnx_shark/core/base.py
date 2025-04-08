# coding:utf-8
import six

import lxbasic.core as bsc_core

import lxbasic.pinyin as bsc_pinyin

import lxbasic.resource as bsc_resource


class EntityTypes(object):
    User = 'User'

    Root = 'Root'

    Project = 'Project'
    Role = 'Role'
    Asset = 'Asset'
    Episode = 'Episode'
    Sequence = 'Sequence'
    Shot = 'Shot'
    Task = 'Task'
    Version = 'Version'

    All = [
        User,

        Root,

        Project,
        Role,
        Asset,
        Episode,
        Sequence,
        Shot,
        Task,
        Version,
    ]


class RootKeys:
    Disorder = 'disorder'
    Source = 'source'
    Release = 'release'
    Temporary = 'temporary'

    All = [
        Disorder,
        Source, Release, Temporary
    ]


class SpaceKeys:
    Disorder = 'disorder'
    Source = 'source'
    Release = 'release'
    Temporary = 'temporary'

    All = [
        Disorder,
        Source, Release, Temporary
    ]


class ResourceTypes:
    Project = 'project'
    Asset = 'asset'
    Sequence = 'sequence'
    Shot = 'shot'

    All = [
        Project,
        Asset,
        Sequence,
        Shot
    ]


class StepKeys:
    # general
    General = 'general'
    # asset
    Model = 'model'
    Groom = 'groom'
    Rig = 'rig'
    CFX = 'cfx'
    Surface = 'surface'
    Layout = 'layout'
    # shot
    Animation = 'animation'

    All = [
        General,
        Model, Groom, Rig, CFX, Surface,
        Layout, Animation
    ]


class TaskKeys:
    # general
    General = 'general'
    # asset
    Model = 'model'
    Groom = 'groom'
    Rig = 'rig'
    CFXRig = 'cfx_rig'
    Surface = 'surface'
    # shot
    Layout = 'layout'
    Animation = 'animation'

    All = [
        General,
        Model, Groom, Rig, CFXRig, Surface,
        Layout, Animation
    ]


class EntityVariants(dict):
    def __init__(self, *args, **kwargs):
        super(EntityVariants, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        return self.__getitem__(item)  # = self[item]

    def __str__(self):
        keys = list(self.keys())
        keys.sort()
        return 'dict(\n{}\n)'.format(
            ',\n'.join(
                ['    {}="{}"'.format(k, self[k]) for k in keys]
            )
        )


class EntityConfig(object):
    INSTANCE = None
    INITIALIZED = False

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if cls.INSTANCE is not None:
            return cls.INSTANCE

        self = super(EntityConfig, cls).__new__(cls)

        # init
        cfg = bsc_resource.BscExtendConfigure.get_as_content('shark/disorder/default')

        self._entity_resolve_pattern_dict = cfg.get('entity.resolve_patterns')
        self._entity_path_pattern_dict = cfg.get('entity.path_patterns')
        self._entity_task_dict = cfg.get('entity.tasks')
        self._entity_variant_key_dict = cfg.get('entity.variant_keys')
        self._entity_variant_key_regex_dict = cfg.get('entity.variant_key_regexes')
        self._entity_variant_cleanup_keys = cfg.get('entity.variant_cleanup_keys')

        self._file_pattern_dict = cfg.get('file_patterns')

        cls.INSTANCE = self
        return self


class EntityVariantKeys:
    """
    virtual value, real value is from configure.
    """
    User = None

    Root = None

    Project = None
    Role = None
    Asset = None
    Episode = None
    Sequence = None
    Shot = None
    Task = None
    Version = None


class EntityPathPatterns:
    User = None

    Root = None

    Project = None
    Role = None
    Asset = None

    Episode = None
    Sequence = None
    Shot = None

    ProjectTask = None
    AssetTask = None
    SequenceTask = None
    ShotTask = None


class EntityTasks:
    """
    virtual value, real value is from configure.
    """
    Concept = None
    Model = None
    Rig = None
    Surface = None

    Animation = None


class FilePatterns:
    """
    virtual value, real value is from configure.
    """
    MayaRigFile = None
    MayaModelFIle = None


class AbsEntityBase(object):
    Type = None
    VariantKey = None

    EntityTypes = EntityTypes

    # update variants from configure here.
    EntityVariantKeys = EntityVariantKeys
    [setattr(EntityVariantKeys, k, v) for k, v in EntityConfig()._entity_variant_key_dict.items()]
    
    EntityPathPatterns = EntityPathPatterns
    [setattr(EntityPathPatterns, k, v) for k, v in EntityConfig()._entity_path_pattern_dict.items()]

    FilePatterns = FilePatterns
    [setattr(FilePatterns, k, v) for k, v in EntityConfig()._file_pattern_dict.items()]

    EntityTasks = EntityTasks
    [setattr(EntityTasks, k, v) for k, v in EntityConfig()._entity_task_dict.items()]

    @classmethod
    def to_entity_path(cls, entity_type, variants):
        path_pattern = getattr(EntityPathPatterns, entity_type)
        return bsc_core.BscDccParseOpt(path_pattern).update_variants_to(**variants).get_value()


class EntityStack(object):
    def __init__(self):
        self._paths = []
        self._entity_dict = {}

    def __contains__(self, path):
        if isinstance(path, six.string_types):
            return path in self._entity_dict
        return False

    def register(self, path, entity):
        if self.exists(path) is False:
            self._paths.append(path)
            self._entity_dict[path] = entity
            return True
        return False

    def get(self, path):
        if path in self._entity_dict:
            return self._entity_dict[path]

    def get_all(self):
        return [self._entity_dict[i] for i in self._paths]

    def exists(self, path):
        return path in self._entity_dict


class EntityVariantKeyFnc:
    @classmethod
    def is_name_match(cls, name, p):
        return bsc_core.BscFnmatch.is_match(name, p)

    @classmethod
    def match_fnc(cls, variants, key):
        return bsc_core.BscFnmatch.is_match(
            variants[key], EntityConfig()._entity_variant_key_regex_dict[key]
        )
    
    @classmethod
    def clean_fnc(cls, variants):
        for k, v in variants.items():
            if k in EntityConfig()._entity_variant_cleanup_keys:
                variants[k] = bsc_pinyin.Text.cleanup(v, stop_on_chs=True)
        return variants
