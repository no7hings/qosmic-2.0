# coding:utf-8


class EntityTypes(object):
    Project = 'Project'
    Asset = 'Asset'
    Episode = 'Episode'
    Sequence = 'Sequence'
    Shot = 'Shot'
    Task = 'Task'
    Version = 'Version'

    All = [
        Project,
        Asset,
        Episode,
        Sequence,
        Shot,
        Task,
        Version,
    ]


class SpaceKeys(object):
    Disorder = 'disorder'
    Source = 'source'
    Release = 'release'
    Temporary = 'temporary'


class Properties(dict):
    def __init__(self, *args, **kwargs):
        super(Properties, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        return self.__getitem__(item)  # = self[item]

    def __str__(self):
        keys = self.keys()
        keys.sort()
        return 'dict(\n{}\n)'.format(
            ',\n'.join(
                ['    {}="{}"'.format(k, self[k]) for k in keys]
            )
        )
