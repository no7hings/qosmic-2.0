# coding:utf-8


class EntityTypes(object):
    Root = 'Root'
    Project = 'Project'
    Asset = 'Asset'
    Sequence = 'Sequence'
    Shot = 'Shot'
    Task = 'Task'


class VariantKeys(object):
    Root = 'root'
    Project = 'project'
    Asset = 'asset'
    Sequence = 'sequence'
    Shot = 'shot'
    Task = 'task'


class Properties(dict):
    def __init__(self, *args, **kwargs):
        super(Properties, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        return self.__getitem__(item)  # = self[item]

    def __str__(self):
        return '(\n{}\n)'.format(
            '\n'.join(
                ['    {}={}'.format(k, v) for k, v in self.items()]
            )
        )
