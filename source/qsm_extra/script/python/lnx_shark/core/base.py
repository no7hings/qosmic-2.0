# coding:utf-8
import lxbasic.resource as bsc_resource


class EntityTypes(object):
    Root = 'Root'

    Project = 'Project'
    Role = 'Role'
    Asset = 'Asset'
    Episode = 'Episode'
    Sequence = 'Sequence'
    Shot = 'Shot'
    Task = 'Task'
    Version = 'Version'

    User = 'User'

    All = [
        Root,

        Project,
        Role,
        Asset,
        Episode,
        Sequence,
        Shot,
        Task,
        Version,

        User
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
        cfg = bsc_resource.BscExtendConfigure.get_as_content('scan/default')
        self._entity_resolve_pattern_dict = cfg.get('entity.resolve_patterns')
        self._entity_path_pattern_dict = cfg.get('entity.path_patterns')
        self._entity_task_dict = cfg.get('entity.tasks')
        self._entity_variant_key_dict = cfg.get('entity.variant_keys')
        self._entity_variant_key_regex_dict = cfg.get('entity.variant_key_regexes')
        self._file_pattern_dict = cfg.get('file_patterns')

        cls.INSTANCE = self
        return self


class EntityStack(object):
    def __init__(self):
        self._paths = []
        self._entity_dict = {}

    def register(self, path, entity):
        self._paths.append(path)
        self._entity_dict[path] = entity

    def get(self, path):
        if path in self._entity_dict:
            return self._entity_dict[path]

    def get_all(self):
        return [self._entity_dict[i] for i in self._paths]

    def exists(self, path):
        return path in self._entity_dict