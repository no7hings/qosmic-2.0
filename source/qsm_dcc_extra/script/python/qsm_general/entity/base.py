# coding:utf-8
import copy

import lxbasic.core as bsc_core


class Properties(dict):
    def __init__(self, *args, **kwargs):
        super(Properties, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        return self.__getitem__(item)  # = self[item]


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


class EntityResolvePatterns(object):
    Project = '{root}/{project}/Assets'
    Asset = '{root}/{project}/Assets/{role}/{asset}'
    Sequence = '{root}/{project}/{sequence}/{sequence}_{extra}'
    Shot = '{root}/{project}/{sequence}/{sequence}_{shot}'
    
    ProjectTask = '{root}/{project}/{task}'
    AssetTask = '{root}/{project}/Assets/{role}/{asset}/{task}/Final'
    SequenceTask = '{root}/{project}/{sequence}/{task}'
    ShotTask = '{root}/{project}/{sequence}/{sequence}_{shot}/{task}'


class EntityDirectoryPatterns(object):
    Project = '{root}/{project}'
    Asset = '{root}/{project}/Assets/{role}/{asset}'
    Sequence = '{root}/{project}/{sequence}'
    Shot = '{root}/{project}/{sequence}/{sequence}_{shot}'

    ProjectTask = '{root}/{project}/{task}'
    AssetTask = '{root}/{project}/Assets/{role}/{asset}/{task}'
    SequenceTask = '{root}/{project}/{sequence}/{task}'
    ShotTask = '{root}/{project}/{sequence}/{sequence}_{shot}/{task}'


class EntityNodePatterns(object):
    Project = '/{project}'
    Asset = '/{project}/{asset}'
    Sequence = '/{project}/{sequence}'
    Shot = '/{project}/{sequence}_{shot}'
    
    ProjectTask = '/{project}/{task}'
    AssetTask = '/{project}/{asset}/{task}'
    SequenceTask = '/{project}/{sequence}/{task}'
    ShotTask = '/{project}/{sequence}_{shot}/{task}'


class EntityTasks(object):
    Concept = 'Concept'
    Model = 'Model'


class NodeStack(object):
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


class AbsEntity(object):
    Type = None
    VariantKey = None
    NextEntityQueryClassDict = dict()
    TaskQueryClass = None

    def __init__(self, root, path, variants):
        self._root = root
        self._root_entity_stack = root.entity_stack
        self._path = path
        self._path_opt = bsc_core.PthNodeOpt(self._path)
        self._name = self._path_opt.get_name()
        self._properties = Properties()
        self._properties.update(variants)
        # for k, v in variants.items():
        #     self.__dict__[k] = v

        self._next_entity_query_cache_dict = dict()
        self._step_query_cache = None

    def __str__(self):
        return '{}(path="{}")'.format(
            self.Type, self._path,
        )

    def __repr__(self):
        return self.__str__()

    @property
    def type(self):
        return self.Type

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return self._path_opt.get_name()

    @property
    def path_opt(self):
        return self._path_opt

    @property
    def properties(self):
        return self._properties

    def _generate_next_entity_query(self, entity_type):
        if entity_type in self._next_entity_query_cache_dict:
            return self._next_entity_query_cache_dict[entity_type]
        variants = copy.copy(self._properties)
        _ = self.NextEntityQueryClassDict[entity_type](self._root, variants)
        self._next_entity_query_cache_dict[entity_type] = _
        return _

    def get_next_entities(self, entity_type=None):
        _ = self._generate_next_entity_query(entity_type)
        return _.get_all()

    def get_next_entity(self, name, entity_type):
        _ = self._generate_next_entity_query(entity_type)
        return _.get(name)

    def find_entity(self, path):
        return self._root_entity_stack.get(path)
    
    def _generate_step_query(self):
        if self._step_query_cache is not None:
            return self._step_query_cache
        variants = copy.copy(self._properties)
        _ = self.TaskQueryClass(self, variants)
        self._step_query_cache = _
        return _
    
    @property
    def tasks(self):
        _ = self._generate_step_query()
        return _.get_all()

    def task(self, name):
        _ = self._generate_step_query()
        return _.get(name)


class AbsEntityQuery(object):
    EntityClass = None

    def __init__(self, root, variants):
        self._root = root
        self._root_entity_stack = root.entity_stack

        self._variants = {}
        self._variants.update(variants)
        self._resolve_ptn_opt = bsc_core.PtnParseOpt(
            EntityResolvePatterns.__dict__[self.EntityClass.Type]
        )
        self._resolve_ptn_opt.update_variants(**self._variants)
        self._node_ptn_opt = bsc_core.PtnParseOpt(
            EntityNodePatterns.__dict__[self.EntityClass.Type]
        )
        self._cache_dict = {}
        self._entity_variant_key = self.EntityClass.VariantKey

        self.update()

    def update(self):
        matches = self._resolve_ptn_opt.get_matches(sort=True)
        for i_variants in matches:
            self.register(i_variants)

    def register(self, variants):
        path = self._node_ptn_opt.update_variants_to(**variants).get_value()
        entity = self.EntityClass(self._root, path, variants)
        self._root_entity_stack.register(path, entity)
        self._cache_dict[path] = entity
        return entity

    def to_entity_path(self, name):
        variants = copy.copy(self._variants)
        variants[self._entity_variant_key] = name
        return self._node_ptn_opt.update_variants_to(**variants).get_value()

    def get_all(self):
        return self._cache_dict.values()

    def get(self, name):
        path = self.to_entity_path(name)
        if path in self._cache_dict:
            return self._cache_dict[path]

        variants = copy.copy(self._variants)
        variants[self._entity_variant_key] = name
        ptn_opt = self._resolve_ptn_opt.update_variants_to(
            **variants
        )
        matches = ptn_opt.get_matches()
        if matches:
            variants_new = matches[0]
            return self.register(variants_new)

    def exist(self, name):
        path = self.to_entity_path(name)
        return path in self._cache_dict

    def __str__(self):
        return str(self._cache_dict.values())


class AbsTask(object):
    Type = None

    def __init__(self, entity, path, variants):
        self._entity = entity
        self._path = path
        self._path_opt = bsc_core.PthNodeOpt(self._path)
        self._name = self._path_opt.get_name()
        self._properties = Properties()
        self._properties.update(variants)

    def __str__(self):
        return '{}(path="{}")'.format(
            self.Type, self._path,
        )

    def __repr__(self):
        return self.__str__()

    @property
    def type(self):
        return self.Type

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return self._path_opt.get_name()

    @property
    def path_opt(self):
        return self._path_opt

    @property
    def properties(self):
        return self._properties


class AbsTaskQuery(object):
    EntityClass = None

    def __init__(self, entity, variants):
        self._entity = entity

        self._variants = {}
        self._variants.update(variants)
        key = '{}{}'.format(self._entity.Type, self.EntityClass.Type)
        self._resolve_ptn_opt = bsc_core.PtnParseOpt(
            EntityResolvePatterns.__dict__[key]
        )
        self._resolve_ptn_opt.update_variants(**self._variants)
        self._node_ptn_opt = bsc_core.PtnParseOpt(
            EntityNodePatterns.__dict__[key]
        )

        self._cache_dict = {}
        self.update()

    def update(self):
        matches = self._resolve_ptn_opt.get_matches(sort=True)
        for i_variants in matches:
            self.register(i_variants)
    
    def register(self, variants):
        path = self._node_ptn_opt.update_variants_to(**variants).get_value()
        entity = self.EntityClass(self._entity, path, variants)
        self._cache_dict[path] = entity
        return entity

    def get_all(self):
        return self._cache_dict.values()

    def get(self, name):
        return self._cache_dict.get(name)
