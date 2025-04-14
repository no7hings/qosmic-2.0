# coding:utf-8
import json

import six

import lxbasic.core as bsc_core

import lxbasic.pinyin as bsc_pinyin

import lxbasic.resource as bsc_resource


class GlobalVar:
    SYNC_CACHE_FLAG = True


class EntityTypes(object):
    Department = 'Department'
    User = 'User'

    Root = 'Root'

    Project = 'Project'

    ResourceType = 'ResourceType'

    Role = 'Role'
    Asset = 'Asset'
    Episode = 'Episode'
    Sequence = 'Sequence'
    Shot = 'Shot'

    Step = 'Step'
    Task = 'Task'

    Version = 'Version'

    All = [
        Department, User,

        Root,

        Project,

        ResourceType,

        Role,
        Asset,
        Episode,
        Sequence,
        Shot,

        Step, Task,

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
    Episode = 'episode'
    Sequence = 'sequence'
    Shot = 'shot'

    All = [
        Project,
        Asset,
        Episode,
        Sequence,
        Shot,
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


class EntityProperties(dict):
    def __init__(self, *args, **kwargs):
        super(EntityProperties, self).__init__(*args, **kwargs)

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


class DisorderConfig(object):
    INSTANCE = None

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if cls.INSTANCE is not None:
            return cls.INSTANCE

        self = super(DisorderConfig, cls).__new__(cls)

        # init
        cfg = bsc_resource.BscExtendConfigure.get_as_content('parsor/disorder/default')

        self._entity_resolve_pattern_dict = cfg.get('entity.resolve_patterns')
        self._entity_path_pattern_dict = cfg.get('entity.path_patterns')
        self._entity_task_dict = cfg.get('entity.tasks')
        self._entity_variant_key_dict = cfg.get('entity.variant_keys')
        self._entity_variant_key_regex_dict = cfg.get('entity.variant_key_regexes')
        self._file_pattern_dict = cfg.get('file_patterns')

        self._entity_variant_cleanup_keys = cfg.get('entity.variant_cleanup_keys')

        cls.INSTANCE = self
        return self


class EntityVariantKeys:
    """
    virtual value, real value is from configure.
    """
    Department = None
    User = None

    Root = None

    Project = None
    Role = None
    Asset = None
    Episode = None
    Sequence = None
    Shot = None
    Step = None
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

    Step = None

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
    ResourceTypes = ResourceTypes

    # update variants from configure here.
    EntityVariantKeys = EntityVariantKeys
    [setattr(EntityVariantKeys, k, v) for k, v in DisorderConfig()._entity_variant_key_dict.items()]
    
    EntityPathPatterns = EntityPathPatterns
    [setattr(EntityPathPatterns, k, v) for k, v in DisorderConfig()._entity_path_pattern_dict.items()]

    FilePatterns = FilePatterns
    [setattr(FilePatterns, k, v) for k, v in DisorderConfig()._file_pattern_dict.items()]

    EntityTasks = EntityTasks
    [setattr(EntityTasks, k, v) for k, v in DisorderConfig()._entity_task_dict.items()]

    @classmethod
    def to_entity_path(cls, entity_type, variants):
        path_pattern = getattr(EntityPathPatterns, entity_type)
        return bsc_core.BscDccParseOpt(path_pattern).update_variants_to(**variants).get_value()

    @classmethod
    def to_task_path(cls, entity_type, variants):
        path_pattern = getattr(EntityPathPatterns, '{}{}'.format(entity_type, EntityTypes.Task))
        return bsc_core.BscDccParseOpt(path_pattern).update_variants_to(**variants).get_value()

    @classmethod
    def to_task_path_(cls, variants):
        path_pattern = getattr(EntityPathPatterns, EntityTypes.Task)
        return bsc_core.BscDccParseOpt(path_pattern).update_variants_to(**variants).get_value()

    @classmethod
    def to_step_path(cls, entity_type, variants):
        path_pattern = getattr(EntityPathPatterns, EntityTypes.Step)
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
            variants[key], DisorderConfig()._entity_variant_key_regex_dict[key]
        )
    
    @classmethod
    def clean_fnc(cls, variants):
        for k, v in variants.items():
            if k in DisorderConfig()._entity_variant_cleanup_keys:
                variants[k] = bsc_pinyin.Text.cleanup(v, stop_on_chs=True)
        return variants


class AbsResourceTypeBase(object):
    Type = None
    VariantKey = None

    def __init__(self, entity, path, variants, *args, **kwargs):
        self._entity = entity
        self._entity_path = path
        self._path_opt = bsc_core.BscNodePathOpt(self._entity_path)
        self._name = self._path_opt.get_name()

        self._variants = variants
        self._properties = EntityProperties(**variants)

        self._entity_type = self.Type
        self._variants['entity_type'] = self._entity_type
        self._variants['entity_path'] = self._entity_path

    def __str__(self):
        return 'Step({})'.format(
            json.dumps(self._variants, indent=4)
        )

    def __repr__(self):
        return '\n'+self.__str__()

    @property
    def type(self):
        return self.Type

    @property
    def path(self):
        return self._entity_path

    @property
    def name(self):
        return self._path_opt.get_name()

    @property
    def path_opt(self):
        return self._path_opt

    @property
    def properties(self):
        return self._properties


class AbsStepBase(object):
    Type = None
    VariantKey = None

    def __init__(self, entity, path, variants, *args, **kwargs):
        self._entity = entity
        self._entity_path = path
        self._path_opt = bsc_core.BscNodePathOpt(self._entity_path)
        self._name = self._path_opt.get_name()

        self._variants = variants
        self._properties = EntityProperties(**variants)

        self._entity_type = self.Type
        self._variants['entity_type'] = self._entity_type
        self._variants['entity_path'] = self._entity_path

    def __str__(self):
        return 'Step({})'.format(
            json.dumps(self._variants, indent=4)
        )

    def __repr__(self):
        return '\n'+self.__str__()

    @property
    def type(self):
        return self.Type

    @property
    def path(self):
        return self._entity_path

    @property
    def name(self):
        return self._path_opt.get_name()

    @property
    def path_opt(self):
        return self._path_opt

    @property
    def properties(self):
        return self._properties


class AbsTaskBase(object):
    Type = None
    VariantKey = None

    def __init__(self, entity, path, variants, *args, **kwargs):
        self._entity = entity
        self._entity_path = path
        self._path_opt = bsc_core.BscNodePathOpt(self._entity_path)
        self._name = self._path_opt.get_name()

        self._variants = variants
        self._properties = EntityProperties(**variants)

        self._entity_type = self.Type
        self._variants['entity_type'] = self._entity_type
        self._variants['entity_path'] = self._entity_path

    def __str__(self):
        return 'Task({})'.format(
            json.dumps(self._variants, indent=4)
        )

    def __repr__(self):
        return '\n'+self.__str__()

    @property
    def type(self):
        return self.Type

    @property
    def path(self):
        return self._entity_path

    @property
    def name(self):
        return self._path_opt.get_name()

    @property
    def path_opt(self):
        return self._path_opt

    @property
    def properties(self):
        return self._properties

    def find_result(self, p):
        p_opt = bsc_core.BscStgParseOpt(p)
        _ = p_opt.get_exists_results(**self._variants)
        if _:
            return _[0]

    def to_storage_path(self, p):
        p_opt = bsc_core.BscStgParseOpt(p)
        p_opt = p_opt.update_variants_to(**self._variants)
        return p_opt.get_value()
