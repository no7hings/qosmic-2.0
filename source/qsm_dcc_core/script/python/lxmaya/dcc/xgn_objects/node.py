# coding:utf-8
import re

import glob

import lxbasic.storage as bsc_storage

import lxbasic.dcc.objects as bsc_dcc_objects
# maya
from ...core.wrap import *

from ... import core as mya_core
# maya dcc objects
from ..objects import scene as mya_dcc_obj_scene

from ..objects import node as mya_dcc_obj_node

from ..objects import node_for_dag as mya_dcc_obj_node_for_dag


class GrowMesh(mya_dcc_obj_node_for_dag.Shape):
    def __init__(self, path):
        super(GrowMesh, self).__init__(path)

    def get_painter_file_node_paths(self):
        return cmds.listConnections(self.path, destination=0, source=1, type=mya_core.MyaNodeTypes.File) or []

    def get_painter_file_nodes(self):
        list_ = []
        for path in self.get_painter_file_node_paths():
            file_reference_node = mya_dcc_obj_node.TextureReference(path)
            list_.append(file_reference_node)
        return list_

    def _test(self):
        pass


class Scene(object):
    def __init__(self):
        pass

    @classmethod
    def get_palette(cls, name):
        return Palette(name=name)

    @classmethod
    def get_palettes(cls):
        return [cls.get_palette(i) for i in xg.palettes()]

    @property
    def version(self):
        return xg.version()

    @property
    def root_path(self):
        return xg.rootDir()

    @property
    def icon_path(self):
        return xg.iconDir()

    @property
    def global_repository_path(self):
        return xg.globalRepo()

    @property
    def local_repository_path(self):
        return xg.localRepo()

    @property
    def server_repository_path(self):
        return xg.userRepo()

    def _test(self):
        pass


class XGenObj(object):
    def __init__(self, *args):
        self._name = str(args[0])
        self._path = str(self._get_path(*args[1:]))

    @property
    def path(self):
        return self._path

    def _get_path(self, *args):
        if args:
            return '/'+'/'.join([i.name for i in args])+'/'+self.name
        return '/'+self.name

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self.__class__.__name__

    def get_class_name(self):
        return xg.nodeClass(self.name)

    def get_is_renderable(self):
        return xg.renderable(self.name)

    def _get_format_dict_(self, regex=False):
        return {}

    def get_ports(self):
        raise NotImplementedError()

    def _get_attribute_print(self):
        return [(i, i.get()) for i in self.get_ports()]

    def __str__(self):
        return '{}(name="{}")'.format(
            self.type,
            self.name
        )

    def __repr__(self):
        return self.__str__()


class Description(XGenObj):
    def __init__(self, name, platte):
        super(Description, self).__init__(name, platte)
        self._platte = platte

    @property
    def platte(self):
        return self._platte

    # property
    def get_id(self):
        return self.get_port('descriptionId').get()

    def get_data_directory(self):
        return '{}/{}'.format(self.platte.get_data_directory(), self.name)

    # object
    def get_object_exists(self, name):
        return name in xg.objects(self.platte.name, self.name)

    def get_object_names(self):
        return xg.objects(self.platte.name, self.name)

    def get_object(self, name):
        return Object(name=name, platte=self.platte, description=self)

    def get_objects(self):
        return [self.get_object(name=i) for i in self.get_object_names()]

    # module
    def get_module(self, name):
        return Module(name, self.platte, self)

    def get_module_names(self):
        return xg.fxModules(self.platte.name, self.name)

    def get_modules(self):
        return [self.get_module(name=i) for i in self.get_module_names()]

    def set_module_import(self, file_path):
        xg.importFXModule(self.platte.name, self.name, file_path)

    # attribute
    def get_port_is_exists(self, name):
        return name in xg.allAttrs(self.platte.name, self.name)

    def get_port(self, name):
        return Port(name=name, platte=self.platte, description=self)

    def get_ports(self, custom=False):
        if custom is True:
            fnc = xg.customAttrs
        else:
            fnc = xg.allAttrs
        return [
            self.get_port(name=i)
            for i in fnc(self.platte.name, self.name)
        ]

    # file port
    def get_file_attributes(self):
        def get_fnc_(lis_, obj_):
            ports = obj_.get_ports()
            for port in ports:
                if port.get_is_use_as_files() is True:
                    if port.get_is_file_enable():
                        lis_.append(port)

        list_ = []
        for i in self.get_objects():
            get_fnc_(list_, i)
        for i in self.get_modules():
            get_fnc_(list_, i)
        return list_

    # grow mesh
    def get_grow_mesh_names(self):
        return xg.boundGeometry(self.platte.name, self.name)

    def get_grow_meshes(self):
        return [GrowMesh(i) for i in self.get_grow_mesh_names()]

    def get_grow_mesh_indexes(self, patch_name):
        return xg.boundFaces(self.platte.name, self.name, patch_name)

    def get_grow_mesh_painter_file_nodes(self):
        list_ = []
        for g in self.get_grow_meshes():
            [list_.append(i) for i in g.get_painter_file_nodes()]
        return list_

    def get_grow_mesh_painter_file_paths(self):
        return list(set([i.get('fileTextureName') for i in self.get_grow_mesh_painter_file_nodes()]))

    def set_export_run(self, file_path):
        xg.exportDescription(self.platte.name, self.name, file_path)

    def get_guide_names(self):
        return xg.descriptionGuides(self.name) or []

    def set_curve_create_from_guide(self):
        guides = self.get_guide_names()
        if guides:
            cmds.select(guides)
            # int $lockLength = 1;
            # int $hide = 1;
            cmd = 'xgmCreateCurvesFromGuides 1 1'
            mel.eval(cmd)


class Palette(XGenObj):
    DESCRIPTION_CLS = Description

    def __init__(self, name):
        super(Palette, self).__init__(name)

    # property
    def get_data_directory(self):
        s = self.get_port('xgDataPath').get()
        return s.format(**self._get_format_dict_()).replace('$', '')

    def set_data_directory(self, dir_path):
        self.get_port('xgDataPath').set(dir_path)

    def get_file_name(self):
        return cmds.getAttr('{}.xgFileName'.format(self.name))

    def get_file_path(self):
        directory_path = mya_dcc_obj_scene.Scene.get_current_directory_path()
        file_name = self.get_file_name()
        return '{}/{}'.format(directory_path, file_name)

    def get_project_path(self):
        return self.get_port('xgProjectPath').get()

    def repath_project_directory_to(self, dir_path):
        self.get_port('xgProjectPath').set(dir_path)

    # compose
    def get_description(self, name):
        return self.DESCRIPTION_CLS(
            name=name, platte=self
        )

    def get_descriptions(self):
        return [self.get_description(name=i) for i in xg.descriptions(self.name)]

    # port
    def get_port_is_exists(self, name):
        return name in xg.allAttrs(self.name)

    def get_port(self, name):
        return Port(name=name, platte=self)

    def get_ports(self, custom=False):
        if custom is True:
            fnc = xg.customAttrs
        else:
            fnc = xg.allAttrs
        return [
            self.get_port(name=i)
            for i in fnc(self.name)
        ]

    def set_export_run(self, file_path):
        xg.exportPalette(self.name, file_path)

    def set_description_import(self, file_path):
        xg.importDescription(self.name, file_path)

    def get_grow_meshes(self):
        return [
            GrowMesh(i)
            for i in
            list(set([j for i in self.get_descriptions() for j in i.get_grow_mesh_names()]))
        ]

    @classmethod
    def _get_files_in_node(cls, collection, node):
        ports = node.get_ports()
        for i_port in ports:
            if i_port.get_is_use_as_files() is True:
                if i_port.get_is_file_enable():
                    [collection.append(i) for i in i_port.get_stg_file_paths() if i not in collection]

    # description
    def get_description_file_paths(self):
        list_ = []
        for d in self.get_descriptions():
            self._get_files_in_node(list_, d)
            for o in d.get_objects():
                self._get_files_in_node(list_, o)
            for m in d.get_modules():
                self._get_files_in_node(list_, m)
        return list_

    def get_description_files(self):
        return [bsc_dcc_objects.StgFile(i) for i in self.get_description_file_paths()]

    def get_file_description_nodes(self):
        pass

    # grow mesh
    def get_grow_mesh_painter_file_nodes(self):
        list_ = []
        for g in self.get_grow_meshes():
            [list_.append(i) for i in g.get_painter_file_nodes()]
        return list_

    def get_grow_mesh_painter_file_paths(self):
        return list(set([i.get('fileTextureName') for i in self.get_grow_mesh_painter_file_nodes()]))

    def _get_format_dict_(self, regex=False):
        return {
            'PROJECT': self.get_project_path()
        }

    def _test(self):
        pass


class Object(XGenObj):
    def __init__(self, name, platte, description):
        super(Object, self).__init__(name, platte, description)
        self._platte, self._description, = platte, description

    @property
    def platte(self):
        return self._platte

    @property
    def type(self):
        return self.name

    @property
    def description(self):
        return self._description

    # port
    def get_port_is_exists(self, name):
        return name in xg.allAttrs(self.platte.name, self.description.name, self.name)

    def get_port_paths(self, custom=False):
        if custom is True:
            fnc = xg.customAttrs
        else:
            fnc = xg.allAttrs
        return fnc(self.platte.name, self.description.name, self.name)

    def get_port(self, name):
        return Port(name=name, platte=self.platte, description=self.description, object=self)

    def get_ports(self, custom=False):
        return [
            self.get_port(name=i)
            for i in self.get_port_paths(custom)
        ]

    def _get_format_dict_(self, regex=False):
        return {
            'DESC': self.description.get_data_directory(),
            'FXMODULE': self.name
        }


class Module(Object):
    def __init__(self, name, platte, description):
        super(Module, self).__init__(name, platte, description)

    @property
    def type(self):
        return xg.fxModuleType(self.platte.name, self.description.name, self.name)

    def set_export_run(self, file_path):
        xg.exportFXModule(self.platte, self._description, self.name, file_path)


class Port(object):
    STG_FILE_CLS = bsc_dcc_objects.StgFile

    # noinspection PyUnusedLocal,PyShadowingBuiltins
    def __init__(self, name, platte=None, description=None, object=None):
        self._name, self._platte, self._description, self._object = name, platte, description, object

    def _get_sub_args(self):
        return [i.name for i in [self.platte, self.description, self.object] if i is not None]

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self.node.path+'.'+self.name

    @property
    def node(self):
        return [i for i in [self.platte, self.description, self.object] if i is not None][-1]

    @property
    def platte(self):
        return self._platte

    @property
    def description(self):
        return self._description

    @property
    def object(self):
        return self._object

    def get_is_exists(self):
        sub_args = self._get_sub_args()
        return xg.attrExists(self.name, sub_args)

    def add(self):
        sub_args = self._get_sub_args()
        xg.addCustomAttr(self.name, *sub_args)

    def remove(self):
        sub_args = self._get_sub_args()
        xg.remCustomAttr(self.name, *sub_args)

    def get(self):
        sub_args = self._get_sub_args()
        return xg.getAttr(self.name, *sub_args)

    def set(self, value):
        sub_args = self._get_sub_args()
        xg.setAttr(self.name, value, *sub_args)

    def get_is_use_as_files(self):
        return '${DESC}/' in self.get()

    def get_is_file_enable(self):
        def get_ignore_fnc_(ignore_config_):
            _ignore_name, _ignore_value = ignore_config_
            _enable_attribute = node.get_port(_ignore_name)
            s = _enable_attribute.get()
            if isinstance(_ignore_value, (tuple, list)):
                return s not in _ignore_value
            return not s == _ignore_value

        node = self.node
        node_type = node.type
        if node_type in mya_core.MyaXGen.PATH_IGNORE_DICT:
            port_path = self.name
            if port_path in mya_core.MyaXGen.PATH_IGNORE_DICT[node_type]:
                ignore_config = mya_core.MyaXGen.PATH_IGNORE_DICT[node_type][port_path]
                if isinstance(ignore_config, tuple):
                    return get_ignore_fnc_(ignore_config)
                elif isinstance(ignore_config, list):
                    results = [get_ignore_fnc_(i) for i in ignore_config]
                    if False in results:
                        return False
                    return True
                return True
            return True
        return True

    def _get_file_in_path(self, file_paths, dir_path):
        description = self.description
        if description is not None:
            grow_meshes = self.description.get_grow_meshes()
            for grow_mesh in grow_meshes:
                glob_patten = '{}/{}.*'.format(dir_path, grow_mesh.transform.name)
                glob_results = glob.glob(glob_patten)
                if not glob_results:
                    file_paths.append(glob_patten)
                    cmds.warning('{} >> file: "{}" is non-exists.'.format(self.path, glob_patten))
                else:
                    [file_paths.append(i) for i in glob_results if i not in file_paths]

    def get_stg_file_paths(self):
        list_ = []
        if self.get_is_use_as_files():
            s = self.get()
            if '''=map('${DESC}/''' in s:
                re_patten = re.compile(r'''map\('(.*?)'\)''', re.S)
                re_results = re.findall(re_patten, s)
                # multi files
                if re_results:
                    for re_result in re_results:
                        dir_path = re_result.format(**self.node._get_format_dict_()).replace('$', '')
                        self._get_file_in_path(list_, dir_path)
            # single files
            elif s.startswith('''${DESC}/'''):
                dir_path = s.format(**self.node._get_format_dict_()).replace('$', '')
                self._get_file_in_path(list_, dir_path)
        return list_

    def get_stg_files(self):
        return [self.STG_FILE_CLS(i) for i in self.get_stg_file_paths()]

    def __str__(self):
        return '{}(name="{}", node="{}")'.format(
            self.__class__.__name__,
            self.name,
            self.node.name
        )

    def __repr__(self):
        return self.__str__()


class GroomFnc(object):
    def __init__(self):
        self._check_dict = {}

    # description
    @classmethod
    def get_description_files(cls):
        list_ = []
        s = Scene()
        for p in s.get_palettes():
            [list_.append(i) for i in p.get_description_files() if i not in list_]
        return list_

    @classmethod
    def get_description_file_paths(cls):
        list_ = []
        s = Scene()
        for p in s.get_palettes():
            [list_.append(i) for i in p.get_description_file_paths() if i not in list_]
        return list_

    @classmethod
    def get_description_lost_files(cls):
        list_ = []
        files = cls.get_description_files()
        if files:
            for file_ in files:
                if file_.get_is_exists() is False:
                    list_.append(file_)
        return list_

    @classmethod
    def get_description_lost_file_paths(cls):
        return [i.file_path for i in cls.get_description_lost_files()]

    # grow mesh
    @classmethod
    def get_grow_mesh_painter_file_nodes(cls):
        list_ = []
        s = Scene()
        for p in s.get_palettes():
            [list_.append(i) for i in p.get_grow_mesh_painter_file_nodes()]
        return list_

    @classmethod
    def get_grow_mesh_painter_file_node_paths(cls):
        return list(set([i.path for i in cls.get_grow_mesh_painter_file_nodes()]))

    @classmethod
    def get_grow_mesh_painter_file_paths(cls):
        return list(set([i.get('fileTextureName') for i in cls.get_grow_mesh_painter_file_nodes()]))

    # lost
    @classmethod
    def get_grow_mesh_lost_painter_file_nodes(cls):
        list_ = []
        file_nodes = cls.get_grow_mesh_painter_file_nodes()
        if file_nodes:
            for i_file_node in file_nodes:
                if bsc_storage.StgFileMtd.get_is_exists(i_file_node.get('fileTextureName')) is False:
                    list_.append(i_file_node)
        return list_

    @classmethod
    def get_grow_mesh_lost_painter_file_node_paths(cls):
        return list(set([i.path for i in cls.get_grow_mesh_lost_painter_file_nodes()]))

    @classmethod
    def get_grow_mesh_lost_painter_file_paths(cls):
        list_ = []
        file_nodes = cls.get_grow_mesh_painter_file_nodes()
        if file_nodes:
            for i_file_node in file_nodes:
                i_file_path = i_file_node.get('fileTextureName')
                if bsc_storage.StgFileMtd.get_is_exists(i_file_path) is False:
                    list_.append(i_file_path)
        return list_

    # action
    @classmethod
    def set_grow_mesh_painter_file_collection(cls, target_dir_path, repath=False):
        pass

    def _test(self):
        pass
