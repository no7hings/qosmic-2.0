# coding:utf-8
import copy

import six

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage


class GlobalVar:
    FILE_CACHE_FLAG = True


class Properties(dict):
    def __init__(self, *args, **kwargs):
        super(Properties, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        return self.__getitem__(item)  # = self[item]


class EntityTypes(object):
    Root = 'Root'
    Project = 'Project'
    Asset = 'Asset'
    Episode = 'Episode'
    Sequence = 'Sequence'
    Shot = 'Shot'
    Task = 'Task'


class VariantKeys:
    Root = 'root'
    Project = 'project'
    Asset = 'asset'
    Episode = 'episode'
    Sequence = 'sequence'
    Shot = 'shot'
    Task = 'task'


class EntityScanPatterns:
    Project = '{root}/{project}/Assets'
    Asset = '{root}/{project}/Assets/{role}/{asset}'

    Episode = '{root}/{project}/{episode}'
    Sequence = '{root}/{project}/{episode}/{sequence}/动画'
    # sequence name has chinese word, so add "{seq_EPT}" for match result.
    Shot = '{root}/{project}/{episode}/{sequence}{seq_EPT}/动画/通过文件/{shot}.ma'

    ProjectTask = '{root}/{project}/{task}'
    AssetTask = '{root}/{project}/Assets/{role}/{asset}/{task}/Final'
    SequenceTask = '{root}/{project}/{sequence}/{task}'
    ShotTask = '{root}/{project}/{sequence}/{shot}/{task}'


class EntityDirectoryPatterns:
    Project = '{root}/{project}'
    Asset = '{root}/{project}/Assets/{role}/{asset}'
    Sequence = '{root}/{project}/{sequence}'
    Shot = '{root}/{project}/{sequence}/{shot}'

    ProjectTask = '{root}/{project}/{task}'
    AssetTask = '{root}/{project}/Assets/{role}/{asset}/{task}'
    SequenceTask = '{root}/{project}/{sequence}/{task}'
    ShotTask = '{root}/{project}/{sequence}/{shot}/{task}'


class VariantKeyMatch:
    Project = '[a-zA-Z]*'
    Asset = '[a-zA-Z]*'

    Episode = '[a-zA-Z]*'
    Sequence = '[a-zA-Z]*'
    Shot = '[a-zA-Z]*[0-9]'

    MAP = {
        VariantKeys.Project: Project,
        VariantKeys.Asset: Asset,

        VariantKeys.Episode: Episode,
        VariantKeys.Sequence: Sequence,
        VariantKeys.Shot: Shot,
    }

    @classmethod
    def is_name_match(cls, name, p):
        return bsc_core.BscFnmatch.is_match(name, p)
    
    @classmethod
    def match_fnc(cls, variants, key):
        return bsc_core.BscFnmatch.is_match(variants[key], cls.MAP[key])


class EntityNodePatterns:
    Project = '/{project}'
    Asset = '/{project}/{asset}'

    Episode = '/{project}/{episode}'
    Sequence = '/{project}/{sequence}'
    Shot = '/{project}/{sequence}/{shot}'
    
    ProjectTask = '/{project}/{task}'
    AssetTask = '/{project}/{asset}/{task}'
    SequenceTask = '/{project}/{sequence}/{task}'
    ShotTask = '/{project}/{sequence}/{shot}/{task}'


class AssetRoles(object):
    Character = None


class EntityTasks(object):
    Concept = 'Design'
    Model = 'Maya'
    Rig = 'Rig'
    Surface = 'UE'

    Animation = '动画'


class StoragePatterns(object):
    MayaRigFile = '{root}/{project}/Assets/{role}/{asset}/Rig/Final/scenes/{asset}_Skin.ma'
    MayaModelFIle = '{root}/{project}/Assets/{role}/{asset}/Maya/Final/{asset}.ma'


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


class AbsEntity(object):
    Type = None
    VariantKey = None
    NextEntitiesCacheClassDict = dict()

    TasksCacheOptClass = None

    EntityTypes = EntityTypes
    EntityTasks = EntityTasks

    StoragePatterns = StoragePatterns

    @classmethod
    def _variant_cleanup_fnc(cls, variants):
        return variants

    @classmethod
    def _variant_validation_fnc(cls, variants):
        return True

    @classmethod
    def _generate_next_entities_cache_key(cls, entity_type, variants, variants_extend=None):
        variants = copy.copy(variants)
        variants['entity_type'] = entity_type
        if variants_extend is not None:
            variants.update(variants_extend)
        return bsc_core.BscHash.to_hash_key(variants)

    @classmethod
    def _generate_next_entities_cache_path(cls, cache_key):
        location = bsc_core.BscEnviron.get_cache_qosmic_root()
        return '{}/scan/{}.json'.format(location, cache_key)

    @classmethod
    def _pull_next_entities_cache(cls, cache_key):
        cache_path = cls._generate_next_entities_cache_path(cache_key)
        data = bsc_storage.StgFileOpt(cache_path).set_read()
        if data:
            return data.get('next_entities', [])
        return []

    def _push_next_entities_cache(self, cache_key, variants_list):
        data = dict(
            entity=self._variants,
            next_entities=variants_list
        )
        cache_path = self._generate_next_entities_cache_path(cache_key)
        bsc_storage.StgFileOpt(cache_path).set_write(data)

    def _generate_next_entities_cache_opt(self, entity_type, variants_extend=None, cache_flag=True):
        # generate key by scan variant, when variants is changed, generate new variant
        variants = copy.copy(self._variants)

        cache_key = self._generate_next_entities_cache_key(entity_type, variants, variants_extend)

        # cache mode
        if cache_flag is True:
            # when is created use exists
            if cache_key in self._next_entities_cache_opt_dict:
                entities_cache_opt = self._next_entities_cache_opt_dict[cache_key]
                return entities_cache_opt

        if GlobalVar.FILE_CACHE_FLAG is True:
            # when file cache is exists, use file cache
            variants_list = self._pull_next_entities_cache(cache_key)
            if variants_list:
                entities_cache_opt = self.NextEntitiesCacheClassDict[entity_type](self._root, variants)
                entities_cache_opt.update_from_cache(variants_list)
                return entities_cache_opt

        entities_cache_opt = self.NextEntitiesCacheClassDict[entity_type](self._root, variants)
        variants_list = entities_cache_opt.update_from_storage(variants_extend, cache_flag)

        self._push_next_entities_cache(cache_key, variants_list)

        bsc_log.Log.trace_result(
            'scan {} for: {}'.format(entity_type, bsc_core.auto_string(self._path))
        )

        self._next_entities_cache_opt_dict[cache_key] = entities_cache_opt
        return entities_cache_opt

    def _find_next_entities(self, entity_type, variants_extend=None, cache_flag=True):
        entities_cache_opt = self._generate_next_entities_cache_opt(entity_type, variants_extend, cache_flag)
        if variants_extend is not None:
            return entities_cache_opt.find_all(variants_extend)
        return entities_cache_opt.get_all()

    def _find_next_entity(self, name, entity_type, variants_extend=None, cache_flag=True):
        entities_cache_opt = self._generate_next_entities_cache_opt(entity_type, variants_extend, cache_flag)
        return entities_cache_opt.get(name)

    # evey entity has task, either project, asset, sequence, shot
    def _generate_tasks_cache_opt(self, variants_extend=None, cache_flag=True):
        if self._tasks_cache_opt is not None:
            return self._tasks_cache_opt

        variants = copy.copy(self._variants)
        _ = self.TasksCacheOptClass(self, variants)
        _.update_from_storage(variants_extend, cache_flag)
        self._tasks_cache_opt = _
        return _

    def __init__(self, root, path, variants):
        self._root = root
        self._root_entity_stack = root.entity_stack
        self._path = path
        self._path_opt = bsc_core.BscNodePathOpt(self._path)
        self._name = self._path_opt.get_name()
        self._variants = variants
        self._properties = Properties()
        self._properties.update(variants)

        self._next_entities_cache_opt_dict = dict()
        self._tasks_cache_opt = None

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

    @property
    def variants(self):
        return self._variants

    @property
    def tasks(self):
        _ = self._generate_tasks_cache_opt()
        return _.get_all()

    def task(self, name):
        _ = self._generate_tasks_cache_opt()
        return _.get(name)


class AbsEntitiesCacheOpt(object):
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
        self._dcc_ptn_opt = bsc_core.BscDccParseOpt(
            EntityNodePatterns.__dict__[self.EntityClass.Type]
        )

        self._entity_dict = {}
        self._variants_list = []
        self._entity_variant_key = self.EntityClass.VariantKey

    def __str__(self):
        return str(self._entity_dict.values())

    def update_from_storage(self, variants_extend=None, cache_flag=True):
        if variants_extend:
            for k, v in variants_extend.items():
                # variant is one
                if isinstance(v, six.string_types):
                    i_variants = copy.copy(self._variants)
                    i_variants[k] = v
                    i_matchers = self.scan_fnc(i_variants)
                    for k_variant in i_matchers:
                        self.register(k_variant)
                # variant is many
                elif isinstance(v, list):
                    for j in v:
                        j_variants = copy.copy(self._variants)
                        j_variants[k] = j
                        j_matchers = self.scan_fnc(j_variants)
                        for k_variant in j_matchers:
                            self.register(k_variant)
                else:
                    raise RuntimeError()
        else:
            variants = copy.copy(self._variants)
            matches = self.scan_fnc(variants)
            for i_variants in matches:
                self.register(i_variants)

        return self._variants_list

    def scan_fnc(self, variants):
        pth_opt = bsc_core.BscStgParseOpt(
            EntityScanPatterns.__dict__[self.EntityClass.Type]
        )
        pth_opt.update_variants(**variants)
        matchers = pth_opt.find_matches(sort=True)
        return matchers

    def register(self, variants):
        variants = self.EntityClass._variant_cleanup_fnc(variants)
        path = self._dcc_ptn_opt.update_variants_to(**variants).get_value()
        if path in self._entity_dict:
            return self._entity_dict[path]

        if self.EntityClass._variant_validation_fnc(variants) is True:
            entity = self.EntityClass(self._root, path, variants)
            self._root_entity_stack.register(path, entity)
            self._variants_list.append(variants)
            self._entity_dict[path] = entity
            return entity

    def to_entity_path(self, name):
        variants = copy.copy(self._variants)
        variants[self._entity_variant_key] = name
        return self._dcc_ptn_opt.update_variants_to(**variants).get_value()

    def update_from_cache(self, data):
        for i_variants in data:
            self.register(i_variants)

    def get_all(self):
        return self._entity_dict.values()

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
        if path in self._entity_dict:
            return self._entity_dict[path]

        variants = copy.copy(self._variants)
        variants[self._entity_variant_key] = name
        ptn_opt = self._stg_ptn_opt_for_scan.update_variants_to(
            **variants
        )
        matches = ptn_opt.find_matches()
        if matches:
            variants_new = matches[0]
            return self.register(variants_new)

    def exist(self, name):
        path = self.to_entity_path(name)
        return path in self._entity_dict


class AbsTask(object):
    Type = None

    def __init__(self, entity, path, variants):
        self._entity = entity
        self._path = path
        self._path_opt = bsc_core.BscNodePathOpt(self._path)
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


class AbsTasksCache(object):
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
        self._dcc_ptn_opt = bsc_core.BscDccParseOpt(
            EntityNodePatterns.__dict__[key]
        )

        self._entity_dict = {}
        self._entity_variant_key = self.EntityClass.VariantKey
        pass

    def update_from_storage(self, variants_extend=None, cache_flag=True):
        matches = self._stg_ptn_opt_for_scan.find_matches(sort=True)
        for i_variants in matches:
            self.register(i_variants)
    
    def register(self, variants):
        path = self._dcc_ptn_opt.update_variants_to(**variants).get_value()
        entity = self.EntityClass(self._entity, path, variants)
        self._entity_dict[path] = entity
        return entity

    def to_entity_path(self, name):
        variants = copy.copy(self._variants)
        variants[self._entity_variant_key] = name
        return self._dcc_ptn_opt.update_variants_to(**variants).get_value()

    def get_all(self):
        return self._entity_dict.values()

    def get(self, name):
        path = self.to_entity_path(name)
        if path in self._entity_dict:
            return self._entity_dict[path]

        variants = copy.copy(self._variants)
        variants[self._entity_variant_key] = name
        ptn_opt = self._stg_ptn_opt_for_scan.update_variants_to(
            **variants
        )
        matches = ptn_opt.find_matches()
        if matches:
            variants_new = matches[0]
            return self.register(variants_new)
