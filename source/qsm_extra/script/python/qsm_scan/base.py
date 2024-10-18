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


class EntityScanPatterns(object):
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


class AssetRoles(object):
    Character = None


class EntityTasks(object):
    Concept = 'Design'
    Model = 'Maya'
    Rig = 'Rig'
    Surface = 'UE'


class StoragePatterns(object):
    MayaRigFile = '{root}/{project}/Assets/{role}/{asset}/Rig/Final/scenes/{asset}_Skin.ma'
    MayaModelFIle = '{root}/{project}/Assets/{role}/{asset}/Maya/Final/{asset}.ma'


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

    EntityTypes = EntityTypes
    EntityTasks = EntityTasks

    StoragePatterns = StoragePatterns

    def __init__(self, root, path, variants):
        self._root = root
        self._root_entity_stack = root.entity_stack
        self._path = path
        self._path_opt = bsc_core.BscPathOpt(self._path)
        self._name = self._path_opt.get_name()
        self._variants = variants
        self._properties = Properties()
        self._properties.update(variants)

        self._next_entity_query_cache_dict = dict()
        self._step_query_cache = None

    def __str__(self):
        return '{}(path="{}")'.format(
            self.Type, bsc_core.auto_string(self._path),
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

    def _generate_next_entity_query(self, entity_type, variants_extend=None):
        if entity_type in self._next_entity_query_cache_dict:
            _ = self._next_entity_query_cache_dict[entity_type]
            if variants_extend is not None:
                _.do_update(variants_extend)
            return _
        variants = copy.copy(self._variants)
        _ = self.NextEntityQueryClassDict[entity_type](self._root, variants)
        _.do_update(variants_extend)
        self._next_entity_query_cache_dict[entity_type] = _
        return _

    def get_next_entities(self, entity_type, variants_extend=None):
        _ = self._generate_next_entity_query(entity_type, variants_extend)
        if variants_extend is not None:
            return _.find_all(variants_extend)
        return _.get_all()

    def get_next_entity(self, name, entity_type):
        _ = self._generate_next_entity_query(entity_type)
        return _.get(name)

    def _generate_step_query(self, variants_extend=None):
        if self._step_query_cache is not None:
            return self._step_query_cache
        variants = copy.copy(self._variants)
        _ = self.TaskQueryClass(self, variants)
        _.do_update(variants_extend)
        self._step_query_cache = _
        return _

    @classmethod
    def _validation_fnc(cls, variants):
        return True

    @property
    def tasks(self):
        _ = self._generate_step_query()
        return _.get_all()

    def task(self, name):
        _ = self._generate_step_query()
        return _.get(name)


class AbsEntitiesCache(object):
    EntityClass = None

    def __init__(self, root, variants):
        self._root = root
        self._root_entity_stack = root.entity_stack

        self._variants = {}
        self._variants.update(variants)
        self._stg_ptn_opt_for_scan = bsc_core.BscStgParseOpt(
            EntityScanPatterns.__dict__[self.EntityClass.Type]
        )
        self._stg_ptn_opt_for_scan.update_variants(**self._variants)
        self._dcc_ptn_opt = bsc_core.PthDccParseOpt(
            EntityNodePatterns.__dict__[self.EntityClass.Type]
        )
        self._cache_dict = {}
        self._entity_variant_key = self.EntityClass.VariantKey

    def do_update(self, variants_extend=None):
        if variants_extend:
            for k, v in variants_extend.items():
                for j in v:
                    j_pth_opt = bsc_core.BscStgParseOpt(
                        EntityScanPatterns.__dict__[self.EntityClass.Type]
                    )
                    j_variants = copy.copy(self._variants)
                    j_variants[k] = j
                    j_pth_opt.update_variants(**j_variants)
                    j_matchers = j_pth_opt.get_matches(sort=True)
                    for k_variant in j_matchers:
                        self.register(k_variant)
        else:
            matches = self._stg_ptn_opt_for_scan.get_matches(sort=True)
            for i_variants in matches:
                self.register(i_variants)

    def register(self, variants):
        if self.EntityClass._validation_fnc(variants) is True:
            path = self._dcc_ptn_opt.update_variants_to(**variants).get_value()
            entity = self.EntityClass(self._root, path, variants)
            self._root_entity_stack.register(path, entity)
            self._cache_dict[path] = entity
            return entity

    def to_entity_path(self, name):
        variants = copy.copy(self._variants)
        variants[self._entity_variant_key] = name
        return self._dcc_ptn_opt.update_variants_to(**variants).get_value()

    def get_all(self):
        return self._cache_dict.values()

    def find_all(self, variants_extend):
        list_ = []
        _ = self.get_all()
        for i in _:
            i_enables = []
            for j_k, j_v in variants_extend.items():
                if i.properties.get(j_k) in j_v:
                    i_enables.append(True)
                else:
                    i_enables.append(False)
            if sum(i_enables) == len(i_enables):
                list_.append(i)
        return list_

    def get(self, name):
        path = self.to_entity_path(name)
        if path in self._cache_dict:
            return self._cache_dict[path]

        variants = copy.copy(self._variants)
        variants[self._entity_variant_key] = name
        ptn_opt = self._stg_ptn_opt_for_scan.update_variants_to(
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
        self._path_opt = bsc_core.BscPathOpt(self._path)
        self._name = self._path_opt.get_name()

        self._variants = variants
        self._properties = Properties()
        self._properties.update(variants)

    def __str__(self):
        return '{}(path="{}")'.format(
            self.Type, bsc_core.auto_string(self._path),
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
    
    def find_result(self, p):
        p_opt = bsc_core.BscStgParseOpt(p)
        _ = p_opt.get_exists_results(**self._variants)
        if _:
            return _[0]
    
    def to_storage_path(self, p):
        p_opt = bsc_core.BscStgParseOpt(p)
        p_opt = p_opt.update_variants_to(**self._variants)
        return p_opt.get_value()


class AbsTaskQuery(object):
    EntityClass = None

    def __init__(self, entity, variants):
        self._entity = entity

        self._variants = {}
        self._variants.update(variants)
        key = '{}{}'.format(self._entity.Type, self.EntityClass.Type)
        self._stg_ptn_opt_for_scan = bsc_core.BscStgParseOpt(
            EntityScanPatterns.__dict__[key]
        )
        self._stg_ptn_opt_for_scan.update_variants(**self._variants)
        self._dcc_ptn_opt = bsc_core.PthDccParseOpt(
            EntityNodePatterns.__dict__[key]
        )

        self._cache_dict = {}
        self._entity_variant_key = self.EntityClass.VariantKey
        pass

    def do_update(self, variants_extend=None):
        matches = self._stg_ptn_opt_for_scan.get_matches(sort=True)
        for i_variants in matches:
            self.register(i_variants)
    
    def register(self, variants):
        path = self._dcc_ptn_opt.update_variants_to(**variants).get_value()
        entity = self.EntityClass(self._entity, path, variants)
        self._cache_dict[path] = entity
        return entity

    def to_entity_path(self, name):
        variants = copy.copy(self._variants)
        variants[self._entity_variant_key] = name
        return self._dcc_ptn_opt.update_variants_to(**variants).get_value()

    def get_all(self):
        return self._cache_dict.values()

    def get(self, name):
        path = self.to_entity_path(name)
        if path in self._cache_dict:
            return self._cache_dict[path]

        variants = copy.copy(self._variants)
        variants[self._entity_variant_key] = name
        ptn_opt = self._stg_ptn_opt_for_scan.update_variants_to(
            **variants
        )
        matches = ptn_opt.get_matches()
        if matches:
            variants_new = matches[0]
            return self.register(variants_new)
