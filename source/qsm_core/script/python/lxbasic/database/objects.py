# coding:utf-8
import collections

import copy

import six

import lxbasic.content as bsc_content

import lxbasic.resource as bsc_resource

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgeneral.texture as gnl_texture

from . import base as _base


class DtbBaseOpt(object):
    PATHSEP = '/'

    class EntityCategories(object):
        Type = 'dtb_type'
        #
        Tag = 'dtb_tag'
        #
        Node = 'dtb_node'
        #
        Port = 'dtb_port'
        Assign = 'dtb_assign'
        Connection = 'dtb_connection'
        #
        All = [
            Type, Tag,
            #
            Node,
            #
            Port, Assign, Connection
        ]

    class EntityTypes(object):
        # type
        CategoryRoot = 'category_root'
        CategoryGroup = 'category_group'
        Category = 'category'
        Type = 'type'
        # tag
        TagGroup = 'tag_group'
        Tag = 'tag'
        # node
        ResourceGroup = 'resource_group'
        Resource = 'resource'
        Version = 'version'
        Storage = 'storage'
        #
        Attribute = 'attribute'
        Connection = 'connection'
        #
        Assign = 'assign'
        #
        Types = 'types'
        Tags = 'tags'

    class Kinds(object):
        # type, use for "resource" classification, one "resource" can have one or more "type"
        ResourceCategoryRoot = 'resource-category-root'
        ResourceCategoryGroup = 'resource-category-group'
        ResourceCategory = 'resource-category'
        ResourceType = 'resource-type'
        # tag, use for "resource" filter, one "resource" can have one or more "tag"
        ResourceSemanticTagGroup = 'resource-semantic-tag-group'
        ResourceUserTagGroup = 'resource-user-tag-group'
        ResourcePropertyTagGroup = 'resource-property-tag-group'
        ResourceStorageTagGroup = 'resource-storage-tag-group'
        #
        ResourcePrimarySemanticTag = 'resource-primary-semantic-tag'
        ResourceSecondarySemanticTag = 'resource-secondary-semantic-tag'
        ResourcePropertyTag = 'resource-property-tag'
        ResourceUserTag = 'resource-user-tag'
        ResourceFileTag = 'resource-file-tag'
        ResourceFormatTag = 'resource-format-tag'
        # resource
        Resource = 'resource'
        Asset = 'asset'
        # version
        Version = 'version'
        # storage
        Directory = 'directory'
        File = 'file'
        All = [
            ResourceCategoryRoot,
            ResourceCategoryGroup,
            ResourceCategory,
            ResourceType,
            # tag, use for "resource" filter, one "resource" can have one or more "tag"
            ResourceSemanticTagGroup,
            ResourceUserTagGroup,
            ResourcePropertyTagGroup,
            ResourceStorageTagGroup,
            #
            ResourcePrimarySemanticTag,
            ResourceSecondarySemanticTag,
            ResourcePropertyTag,
            ResourceUserTag,
            ResourceFileTag,
            ResourceFormatTag,
            # resource
            Resource,
            Asset,
            # version
            Version,
            # storage
            Directory,
            File,
        ]

    EntityTypeCategoryMapper = {
        # type
        EntityTypes.CategoryRoot: EntityCategories.Type,
        EntityTypes.CategoryGroup: EntityCategories.Type,
        EntityTypes.Category: EntityCategories.Type,
        EntityTypes.Type: EntityCategories.Type,
        # tag
        EntityTypes.TagGroup: EntityCategories.Tag,
        EntityTypes.Tag: EntityCategories.Tag,
        # node
        EntityTypes.Resource: EntityCategories.Node,
        EntityTypes.Version: EntityCategories.Node,
        EntityTypes.Storage: EntityCategories.Node,
        # port
        EntityTypes.Attribute: EntityCategories.Port,
        # connection
        EntityTypes.Connection: EntityCategories.Connection,
        # assign
        EntityTypes.Assign: EntityCategories.Assign,
        EntityTypes.Types: EntityCategories.Assign,
        EntityTypes.Tags: EntityCategories.Assign,
    }

    def __init__(self, database, disable_new_connection=False):
        if not database:
            raise RuntimeError()

        # if os.path.isfile(database) is False:
        #     raise RuntimeError()

        bsc_log.Log.trace_method_result(
            'database', 'setup from: {}'.format(database)
        )

        self._dtb_file_path = database
        self._dtb_file_opt = bsc_storage.StgFileOpt(
            database
        )
        self._dtb_file_opt.create_directory()

        self._dtb_opt = _base.DtbSqlConnectionOpt.create_from_database(
            self._dtb_file_opt.get_path()
        )

        self._disable_new_connection = disable_new_connection

    def get_database(self):
        return self._dtb_file_path

    database = property(get_database)

    def accept(self):
        self._dtb_opt.accept()

    # utility
    def add_entity(self, entity_type, data):
        entity_category = self.EntityTypeCategoryMapper[entity_type]
        if entity_category in [self.EntityCategories.Assign]:
            value = data['value']
            node = data['node']
            path = '{}->{}'.format(node, value)
            data['path'] = path
        #
        elif entity_category in [self.EntityCategories.Port]:
            node = data['node']
            port = data['port']
            path = '{}.{}'.format(node, port)
            data['path'] = path
        else:
            if 'path' in data:
                path = data.get('path')
                if path.startswith('/'):
                    if path == '/':
                        data['group'] = ''
                        data['name'] = ''
                    else:
                        #
                        path_opt = bsc_core.PthNodeOpt(path)
                        group = path_opt.get_parent_path()
                        data['group'] = group
                        name = path_opt.get_name()
                        data['name'] = name
                else:
                    data['name'] = path
            else:
                group = data['group']
                if group == '/':
                    path = '/{name}'.format(**data)
                else:
                    path = '{group}/{name}'.format(**data)
                data['path'] = path
        #
        data['entity_category'] = entity_category
        data['entity_type'] = entity_type
        table_opt = self._dtb_opt.get_table_opt(entity_category)
        table_opt.add(**data)
        self.accept()
        return self.get_entity(
            entity_type=entity_type,
            filters=[
                ('path', 'is', path)
            ]
        )

    def get_entity(self, entity_type, filters, new_connection=True):
        entity_category = self.EntityTypeCategoryMapper[entity_type]
        table_opt = self._dtb_opt.get_table_opt(entity_category)
        if isinstance(filters, list):
            filters.append(
                ('entity_type', 'is', entity_type)
            )
        return table_opt.get_one(
            filters=filters,
            new_connection=new_connection if self._disable_new_connection is False else False,
        )

    def get_entities(self, entity_type, filters=None, new_connection=True):
        entity_category = self.EntityTypeCategoryMapper[entity_type]
        table_opt = self._dtb_opt.get_table_opt(entity_category)
        if isinstance(filters, list):
            filters.append(
                ('entity_type', 'is', entity_type)
            )
        return table_opt.get_all(
            filters=filters,
            new_connection=new_connection if self._disable_new_connection is False else False
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.accept()


class DtbNodeOpt(object):
    def __init__(self, dtb_opt, dtb_entity, new_connection=False):
        self._dtb_opt = dtb_opt
        self._dtb_entity = dtb_entity
        self._new_connection = new_connection

    def get(self, key):
        return self._dtb_opt.get_entity(
            entity_type=self._dtb_opt.EntityTypes.Attribute,
            filters=[
                ('node', 'is', self._dtb_entity.path),
                ('port', 'is', key),
            ],
            new_connection=self._new_connection
        ).value

    def get_as_node(self, key):
        return self._dtb_opt.get_entity(
            entity_type=key,
            filters=[
                ('path', 'is', self.get(key)),
            ],
            new_connection=self._new_connection
        )


class DtbOptForResource(DtbBaseOpt):
    CACHE = dict()

    @classmethod
    def generate(cls, category_group):
        if category_group in cls.CACHE:
            return cls.CACHE[category_group]

        cfg = bsc_resource.RscExtendConfigure.get_yaml('database/library/resource-basic')
        if cfg is None:
            raise RuntimeError()

        cfg_extend = bsc_resource.RscExtendConfigure.get_yaml('database/library/resource-{}'.format(category_group))
        if cfg_extend is None:
            raise RuntimeError()

        opt = cls(
            cfg,
            cfg_extend
        )
        cls.CACHE[category_group] = opt
        return opt

    def __init__(self, configure_file, configure_file_extend=None, disable_new_connection=False):
        self._dtb_cfg_file_path = configure_file
        self._dtb_cfg_file_path_extend = configure_file_extend
        self._dtb_cfg_opt = bsc_content.Content(value=configure_file)
        if configure_file_extend is not None:
            if bsc_storage.StgFileOpt(configure_file_extend).get_is_file() is False:
                raise RuntimeError()
            #
            self._dtb_cfg_opt.update_from_content(
                bsc_content.Content(value=configure_file_extend)
            )

        self._dtb_cfg_opt.do_flatten()

        self._dtb_pattern_kwargs = {}
        library_root = bsc_core.EnvBaseMtd.get_library_root()
        if library_root is None:
            raise RuntimeError()

        self._dtb_stg_root = '{}/resource'.format(library_root)

        self._dtb_pattern_kwargs['root'] = self._dtb_stg_root
        db_file_pattern = self._dtb_cfg_opt.get('database.file')
        if db_file_pattern is None:
            return
        #
        super(DtbOptForResource, self).__init__(
            db_file_pattern.format(
                **self._dtb_pattern_kwargs
            ),
            disable_new_connection=disable_new_connection
        )

    def get_database_configure(self):
        return self._dtb_cfg_file_path

    database_configure = property(get_database_configure)

    def get_database_configure_opt(self):
        return self._dtb_cfg_opt

    database_configure_opt = property(get_database_configure_opt)

    def get_database_configure_extend(self):
        return self._dtb_cfg_file_path_extend

    database_configure_extend = property(get_database_configure_extend)

    def get_stg_root(self):
        return self._dtb_stg_root

    stg_root = property(get_stg_root)

    def get_pattern(self, keyword):
        return self._dtb_cfg_opt.get(
            'patterns.{}'.format(keyword)
        )

    def get_pattern_opt(self, keyword):
        p = self.get_pattern(keyword)
        p_opt = bsc_core.PtnStgParseOpt(p)
        return p_opt.update_variants_to(
            **self._dtb_pattern_kwargs
        )

    def get_pattern_kwargs(self):
        return self._dtb_pattern_kwargs

    def setup_entity_categories(self):
        dtb_type_options_dict = {}
        basic_dtb_type_options = self._dtb_cfg_opt.get('option.basic.default_basic_entity_type_options')
        basic_types = self._dtb_cfg_opt.get('option.basic_types')
        for i_basic_type, i_basic_kwargs in basic_types.items():
            i_dtb_type_options = collections.OrderedDict()
            i_dtb_type_options.update(basic_dtb_type_options)
            i_dtb_type_options.update(i_basic_kwargs.get('options') or {})
            i_dtb_type_options.update(i_basic_kwargs.get('options_extra') or {})
            dtb_type_options_dict[i_basic_type] = i_dtb_type_options
        #
        entity_categories = self._dtb_cfg_opt.get('option.entity_categories')
        for i_entity_category, i_entity_kwargs in entity_categories.items():
            i_basic_type = i_entity_kwargs['basic_type']
            # use copy
            i_entity_type_options = copy.copy(dtb_type_options_dict[i_basic_type])
            #
            i_entity_type_options.update(i_entity_kwargs.get('options_over') or {})
            i_entity_type_options.update(i_entity_kwargs.get('options_extra') or {})
            i_table_opt = self._dtb_opt.get_table_opt(name=i_entity_category)
            i_table_opt.create(i_entity_type_options)

    def setup_entities(self):
        entities = self._dtb_cfg_opt.get('option.entities')
        for i_path, i_kwargs in entities.items():
            i_entity_type = i_kwargs['entity_type']
            i_options = i_kwargs.get('options') or {}
            i_path_opt = bsc_core.PthNodeOpt(i_path)
            i_name = i_path_opt.name

            if 'gui_name' in i_kwargs:
                i_gui_name = i_kwargs['gui_name']
            else:
                i_gui_name = bsc_core.RawStrUnderlineOpt(i_name).to_prettify()

            self.add_entity(
                entity_type=i_entity_type,
                data=dict(
                    path=i_path,
                    gui_name=i_gui_name,
                    **i_options
                )
            )
            i_children = i_kwargs.get('children')
            if i_children is not None:
                i_child_entity_type = i_children.get('entity_type')
                if i_child_entity_type is None:
                    continue
                #
                i_child_names = i_children.get('names') or []
                i_child_options = i_children.get('options') or {}
                for j_child_name in i_child_names:
                    j_child_gui_name = bsc_core.RawStrUnderlineOpt(j_child_name).to_prettify()
                    self.add_entity(
                        entity_type=i_child_entity_type,
                        data=dict(
                            name=j_child_name,
                            gui_name=j_child_gui_name,
                            **i_child_options
                        )
                    )

    def create_category_root(self, path):
        _ = self.get_entity(
            entity_type=self.EntityTypes.CategoryRoot,
            filters=[
                ('path', 'is', path),
            ]
        )
        if _:
            return False, _
        #
        gui_name = 'All'
        options = dict(kind=self.Kinds.ResourceCategoryRoot, gui_icon_name='database/all')
        return True, self.add_entity(
            entity_type=self.EntityTypes.CategoryRoot,
            data=dict(
                path=path,
                gui_name=gui_name,
                **options
            )
        )

    def create_category_group(self, path):
        path_opt = bsc_core.PthNodeOpt(path)
        if not self.get_entity(
                entity_type=self.EntityTypes.CategoryRoot,
                filters=[
                    ('path', 'is', path_opt.get_parent_path()),
                ]
        ):
            raise RuntimeError()
        #
        _ = self.get_entity(
            entity_type=self.EntityTypes.CategoryGroup,
            filters=[
                ('path', 'is', path),
            ]
        )
        if _:
            return False, _
        #
        name = path_opt.get_name()
        gui_name = bsc_core.RawStrUnderlineOpt(name).to_prettify()
        options = dict(kind=self.Kinds.ResourceCategoryGroup, gui_icon_name='database/groups')
        return True, self.add_entity(
            entity_type=self.EntityTypes.CategoryGroup,
            data=dict(
                path=path,
                gui_name=gui_name,
                **options
            )
        )

    def create_category(self, path):
        path_opt = bsc_core.PthNodeOpt(path)
        if not self.get_entity(
                entity_type=self.EntityTypes.CategoryGroup,
                filters=[
                    ('path', 'is', path_opt.get_parent_path()),
                ]
        ):
            raise RuntimeError()
        #

        _ = self.get_entity(
            entity_type=self.EntityTypes.Category,
            filters=[
                ('path', 'is', path),
            ]
        )
        if _:
            return False, _
        #
        name = path_opt.get_name()
        gui_name = bsc_core.RawStrUnderlineOpt(name).to_prettify()
        options = dict(kind=self.Kinds.ResourceCategory, gui_icon_name='database/group')
        return True, self.add_entity(
            entity_type=self.EntityTypes.Category,
            data=dict(
                path=path,
                gui_name=gui_name,
                **options
            )
        )

    def get_category(self, path):
        return self.get_entity(
            entity_type=self.EntityTypes.Category,
            filters=[
                ('path', 'is', path),
            ]
        )

    def get_categories(self, category_group):
        return self.get_entities(
            entity_type=self.EntityTypes.Category,
            filters=[
                ('group', 'is', '/{}'.format(category_group)),
            ]
        )

    def create_type(self, path):
        path_opt = bsc_core.PthNodeOpt(path)
        if not self.get_entity(
                entity_type=self.EntityTypes.Category,
                filters=[
                    ('path', 'is', path_opt.get_parent_path()),
                ]
        ):
            raise RuntimeError()
        #
        _ = self.get_entity(
            entity_type=self.EntityTypes.Type,
            filters=[
                ('path', 'is', path),
            ]
        )
        if _:
            return False, _
        #
        name = path_opt.get_name()
        gui_name = bsc_core.RawStrUnderlineOpt(name).to_prettify()
        options = dict(kind=self.Kinds.ResourceType, gui_icon_name='database/object')
        options['gui_name'] = gui_name
        return True, self.add_entity(
            entity_type=self.EntityTypes.Type,
            data=dict(
                path=path,
                **options
            )
        )

    def get_type(self, path):
        return self.get_entity(
            entity_type=self.EntityTypes.Type,
            filters=[
                ('path', 'is', path),
            ]
        )

    def get_types(self, category_group, category):
        return self.get_entities(
            entity_type=self.EntityTypes.Type,
            filters=[
                ('group', 'is', '/{}/{}'.format(category_group, category)),
            ]
        )

    def create_type_assign(self, node_path, value, kind):
        _ = self.get_entity(
            entity_type=self.EntityTypes.Types,
            filters=[
                ('path', 'is', '{}->{}'.format(node_path, value)),
            ]
        )
        if _:
            return False, _
        return True, self.add_entity(
            entity_type=self.EntityTypes.Types,
            data=dict(
                kind=kind,
                #
                node=node_path,
                value=value
            )
        )

    def get_type_force(self, path):
        _ = self.get_entity(
            entity_type=self.EntityTypes.Type,
            filters=[
                ('path', 'is', path),
                ('kind', 'is', self.Kinds.ResourceType)
            ]
        )
        if _:
            return False, _
        #
        method_args = [
            self.create_category_root,
            self.create_category_group,
            self.create_category,
            self.create_type,
        ]
        path_opt = bsc_core.PthNodeOpt(path)
        components = path_opt.get_components()
        components.reverse()
        results = []
        for seq, i in enumerate(components):
            i_kwargs = dict(path=i.get_path())
            i_method = method_args[seq]
            results.append(i_method(**i_kwargs))
        #
        return results[-1]

    def get_all_resources(self):
        return self.get_entities(
            entity_type=self.EntityTypes.Resource,
            filters=[
                ('kind', 'is', self.Kinds.Resource)
            ]
        )

    def get_resource(self, path):
        return self.get_entity(
            entity_type=self.EntityTypes.Resource,
            filters=[
                ('path', 'is', path),
            ]
        )

    def create_resource(self, path, **kwargs):
        _ = self.get_entity(
            entity_type=self.EntityTypes.Resource,
            filters=[
                ('path', 'is', path),
            ]
        )
        if _:
            return False, _
        #
        path_opt = bsc_core.PthNodeOpt(path)
        name = path_opt.get_name()
        gui_name = bsc_core.RawStrUnderlineOpt(name).to_prettify()
        options = dict(kind=self.Kinds.Resource, gui_icon_name='database/object')
        options['gui_name'] = gui_name
        options.update(kwargs)
        return True, self.add_entity(
            entity_type=self.EntityTypes.Resource,
            data=dict(
                path=path,
                **options
            )
        )

    def get_resource_type_paths(self, resource_path):
        return [
            i.value for i in self.get_entities(
                entity_type=self.EntityTypes.Types,
                filters=[
                    ('node', 'is', resource_path),
                ]
            )
        ]

    def get_resource_types(self, path):
        return [
            self.get_type(i.value) for i in self.get_entities(
                entity_type=self.EntityTypes.Types,
                filters=[
                    ('node', 'is', path),
                ]
            )
        ]

    def create_version(self, path):
        _ = self.get_entity(
            entity_type=self.EntityTypes.Version,
            filters=[
                ('path', 'is', path),
            ]
        )
        if _:
            return False, _
        #
        path_opt = bsc_core.PthNodeOpt(path)
        name = path_opt.get_name()
        gui_name = name
        options = dict(kind=self.Kinds.Version, gui_icon_name='database/object')
        return True, self.add_entity(
            entity_type=self.EntityTypes.Version,
            data=dict(
                path=path,
                gui_name=gui_name,
                **options
            )
        )

    def get_dtb_version(self, path):
        return self.get_entity(
            entity_type=self.EntityTypes.Version,
            filters=[
                ('path', 'is', path),
            ]
        )

    def create_property(self, node_path, port_path, value, kind):
        atr_path = '.'.join([node_path, port_path])
        _ = self.get_entity(
            entity_type=self.EntityTypes.Attribute,
            filters=[
                ('path', 'is', atr_path),
            ]
        )
        if _:
            return False, _
        #
        return True, self.add_entity(
            entity_type=self.EntityTypes.Attribute,
            data=dict(
                kind=kind,
                node=node_path,
                port=port_path,
                value=value
            )
        )

    def create_storage(self, path, kind):
        if kind not in self.Kinds.All:
            raise RuntimeError()
        #
        _ = self.get_entity(
            entity_type=self.EntityTypes.Storage,
            filters=[
                ('path', 'is', path),
            ]
        )
        if _:
            return False, _
        #
        path_opt = bsc_core.PthNodeOpt(path)
        name = path_opt.get_name()
        gui_name = name
        options = dict(kind=kind, gui_icon_name='database/object')
        return True, self.add_entity(
            entity_type=self.EntityTypes.Storage,
            data=dict(
                path=path,
                gui_name=gui_name,
                **options
            )
        )

    def get_property(self, node_path, port_path):
        _ = self.get_entity(
            entity_type=self.EntityTypes.Attribute,
            filters=[
                ('path', 'is', '{}.{}'.format(node_path, port_path)),
            ]
        )
        if _:
            return _.value

    def create_tag(self, path, kind):
        _ = self.get_entity(
            entity_type=self.EntityTypes.Tag,
            filters=[
                ('path', 'is', path),
            ]
        )
        if _:
            return False, _
        options = dict(kind=kind, gui_icon_name='database/object')
        return True, self.add_entity(
            entity_type=self.EntityTypes.Tag,
            data=dict(
                path=path,
                **options
            )
        )

    def create_tag_assign(self, node_path, value, kind):
        _ = self.get_entity(
            entity_type=self.EntityTypes.Tags,
            filters=[
                ('path', 'is', '{}->{}'.format(node_path, value)),
            ]
        )
        if _:
            return False, _
        return True, self.add_entity(
            entity_type=self.EntityTypes.Tags,
            data=dict(
                kind=kind,
                #
                node=node_path,
                value=value
            )
        )

    @classmethod
    def guess_type_args(cls, keys):
        c_max = 4
        c = len(keys)
        if c < 3:
            keys += ['other']*(c_max-c-1)
        elif c > 3:
            keys = keys[:2]+['_'.join(keys[2:])]
        #
        return keys

    def find_resource_paths_by_category(self, *args):
        _ = args[0]
        if isinstance(_, _base.DtbDict):
            path = _.path
        elif isinstance(_, six.string_types):
            path = _
        else:
            raise RuntimeError()
        return map(
            lambda x: x.node, self.get_entities(
                entity_type=self.EntityTypes.Types,
                filters=[
                    ('kind', 'is', self.Kinds.ResourceType),
                    #
                    ('value', 'startswith', path)
                ]
            )
        )

    def find_resources_by_category(self, *args):
        _ = args[0]
        if isinstance(_, _base.DtbDict):
            path = _.path
        elif isinstance(_, six.string_types):
            path = _
        else:
            raise RuntimeError()
        return map(
            lambda x: self.get_resource(x.node),
            self.get_entities(
                entity_type=self.EntityTypes.Types,
                filters=[
                    ('kind', 'is', self.Kinds.ResourceType),
                    #
                    ('value', 'startswith', path)
                ]
            )
        )


class DtbNodeOptForRscVersion(object):
    def __init__(self, dtb_opt, dtb_version, disable_new_connection=False):
        self._dtb_opt = dtb_opt
        self._dtb_version = dtb_version
        self.__build_varints()

    def get(self, key):
        return self._variants[key]

    def __build_varints(self):
        p = self._dtb_opt.get_pattern(keyword='version-dir')
        p_o = bsc_core.PtnStgParseOpt(p)
        version_stg_path = self._dtb_opt.get_property(
            self._dtb_version.path, 'location'
        )
        # map to current platform
        version_stg_path = bsc_storage.StgPathMapper.map_to_current(version_stg_path)
        self._variants = p_o.get_variants(version_stg_path)

    def get_variants(self):
        return self._variants

    def get_resource(self):
        return self._dtb_opt.get_resource(
            self._dtb_opt.get_property(self._dtb_version.path, 'resource')
        )

    def get_types(self):
        return self._dtb_opt.get_resource_types(self.get_resource().path)

    def get_geometry_usd_file(self, force=False):
        p = self._dtb_opt.get_pattern(keyword='geometry-usd-file')
        p_o = bsc_core.PtnStgParseOpt(p)
        path = p_o.update_variants_to(**self._variants).get_value()
        if bsc_storage.StgPathMtd.get_is_exists(path):
            return path
        if force is True:
            return bsc_resource.ExtendResource.get('assets/library/geometry/sphere.usda')

    def get_geometry_abc_file(self):
        p = self._dtb_opt.get_pattern(keyword='geometry-abc-file')
        p_o = bsc_core.PtnStgParseOpt(p)
        path = p_o.update_variants_to(**self._variants).get_value()
        if bsc_storage.StgPathMtd.get_is_exists(path):
            return path

    def get_geometry_fbx_file(self):
        p = self._dtb_opt.get_pattern(keyword='geometry-fbx-file')
        p_o = bsc_core.PtnStgParseOpt(p)
        path = p_o.update_variants_to(**self._variants).get_value()
        if bsc_storage.StgPathMtd.get_is_exists(path):
            return path

    def get_look_preview_usd_file(self):
        p = self._dtb_opt.get_pattern(keyword='look-preview-usd-file')
        p_o = bsc_core.PtnStgParseOpt(p)
        path = p_o.update_variants_to(**self._variants).get_value()
        if bsc_storage.StgPathMtd.get_is_exists(path):
            return path
        return bsc_resource.ExtendResource.get('assets/library/preview-material.usda')

    def get_hdri_file(self):
        p = self._dtb_opt.get_pattern(keyword='hdri-original-jpg-file')
        p_o = bsc_core.PtnStgParseOpt(p)
        path = p_o.update_variants_to(**self._variants).get_value()
        if bsc_storage.StgPathMtd.get_is_exists(path):
            return path
        return bsc_resource.ExtendResource.get('assets/library/hdri/srgb/StinsonBeach.png')

    @classmethod
    def _get_texture_args(cls, directory_path):
        directory_opt = bsc_storage.StgDirectoryOpt(directory_path)
        texture_paths = directory_opt.get_file_paths(ext_includes=['.jpg'])
        if texture_paths:
            texture_path = texture_paths[0]
            m = gnl_texture.TxrMethodForBuild.generate_instance()
            return m.generate_all_texture_args(texture_path)

    def get_texture_preview_assigns(self):
        storage_dtb_path = '{}/{}'.format(self._dtb_version.path, 'texture_original_src_directory')
        dtb_storage = self._dtb_opt.get_entity(
            entity_type=self._dtb_opt.EntityTypes.Storage,
            filters=[
                ('path', 'is', storage_dtb_path)
            ]
        )
        dtb_storage_opt = DtbNodeOpt(self._dtb_opt, dtb_storage, new_connection=True)
        directory_stg_path = dtb_storage_opt.get('location')
        texture_args = self._get_texture_args(directory_stg_path)
        if texture_args:
            texture_name, texture_data = texture_args
            if texture_data:
                dict_ = {}
                for k, v in texture_data.items():
                    dict_[k] = v[0]
                return dict_
        return {}

    def get_scene_maya_file(self):
        p = self._dtb_opt.get_pattern(keyword='scene-maya-file')
        p_o = bsc_core.PtnStgParseOpt(p)
        return p_o.update_variants_to(**self._variants).get_value()

    def get_file(self, keyword):
        p = self._dtb_opt.get_pattern(keyword=keyword)
        p_o = bsc_core.PtnStgParseOpt(p)
        return p_o.update_variants_to(**self._variants).get_value()

    def get_exists_file(self, keyword):
        path = self.get_file(keyword)
        if bsc_storage.StgFileOpt(path).get_is_exists() is True:
            return path