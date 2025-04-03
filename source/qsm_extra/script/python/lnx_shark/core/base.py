# coding:utf-8


class EntityTypes(object):
    Root = 'Root'

    Project = 'Project'
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


class Variants(dict):
    def __init__(self, *args, **kwargs):
        super(Variants, self).__init__(*args, **kwargs)

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