# coding:utf-8
import fnmatch

import re

from . import raw as bsc_cor_raw


class PthNodeMtd(object):
    @classmethod
    def get_dag_args(cls, path, pathsep='/'):
        """
        :param path: str(<obj-path>)
        :param pathsep:
        :return: list[str(<obj-name>), ...]
        """
        if pathsep is None:
            raise TypeError()
        # is <root-obj>, etc: "/"
        if path == pathsep:
            return [pathsep, ]
        # is <obj>, etc: "/obj"
        return path.split(pathsep)

    @classmethod
    def get_dag_name(cls, path, pathsep='/'):
        """
        :param path:
        :param pathsep:
        :return:
        """
        # is <root-obj>, etc: "/"
        if path == pathsep:
            return pathsep
        # is <obj>, etc: "/obj"
        return cls.get_dag_args(path, pathsep)[-1]

    @classmethod
    def get_dag_parent_path(cls, path, pathsep='/'):
        """
        :param path:
        :param pathsep:
        :return:
        """
        dag_args = cls.get_dag_args(path, pathsep)
        # windows file-path-root etc: "D:/directory"
        if ':' in dag_args[0]:
            if len(dag_args) == 1:
                return None
            return pathsep.join(dag_args[:-1])
        if len(dag_args) == 1:
            return None
        elif len(dag_args) == 2:
            return pathsep
        return pathsep.join(dag_args[:-1])

    @classmethod
    def get_dag_parent_name(cls, path, pathsep):
        return cls.get_dag_name(
            cls.get_dag_parent_path(path, pathsep), pathsep
        )

    @classmethod
    def get_dag_component_paths(cls, path, pathsep='/'):
        """
        :param path:
        :param pathsep:
        :return: list[str(<obj-path>)]
        """

        def _rcs_fnc(lis_, path_):
            if path_ is not None:
                lis_.append(path_)
                _parent_path = cls.get_dag_parent_path(path_, pathsep)
                if _parent_path:
                    _rcs_fnc(lis_, _parent_path)

        lis = []
        _rcs_fnc(lis, path)
        return lis

    @classmethod
    def get_dag_name_with_namespace_clear(cls, name, namespacesep=':'):
        return name.split(namespacesep)[-1]

    @classmethod
    def get_dag_path_with_namespace_clear(cls, path, pathsep='/', namespacesep=':'):
        dag_args = cls.get_dag_args(path, pathsep)
        lis = []
        for i in dag_args:
            lis.append(cls.get_dag_name_with_namespace_clear(i, namespacesep))
        return cls.get_dag_path(lis, pathsep)

    @classmethod
    def get_dag_path_lstrip(cls, path, lstrip=None):
        if lstrip is not None:
            if path.startswith(lstrip):
                return path[len(lstrip):]
            elif lstrip.startswith(path):
                return ''
            return path
        return path

    @classmethod
    def get_dag_path(cls, dag_args, pathsep='/'):
        return pathsep.join(dag_args)

    @classmethod
    def get_dag_pathsep_replace(cls, path, pathsep_src='/', pathsep_tgt='/'):
        if path == pathsep_src:
            return pathsep_tgt
        return pathsep_tgt.join(cls.get_dag_args(path, pathsep=pathsep_src))

    @classmethod
    def get_dag_child_path(cls, path, child_name, pathsep='/'):
        if path == pathsep:
            return pathsep+child_name
        return pathsep.join([path, child_name])

    @classmethod
    def find_dag_child_paths(cls, path, paths, pathsep='/'):
        lis = []
        # etc. r'/shl/chr/test_0/[^/]*'
        if path == pathsep:
            ptn = r'{1}[^{1}]*'.format(path, pathsep)
        else:
            ptn = r'{0}{1}[^{1}]*'.format(path, pathsep)
        #
        for i_path in paths:
            if i_path != pathsep:
                _ = re.match(
                    ptn, i_path
                )
                if _ is not None:
                    if _.group() == i_path:
                        lis.append(i_path)
        return lis

    @classmethod
    def find_dag_child_names(cls, path, paths, pathsep='/'):
        return [cls.get_dag_name(x) for x in cls.find_dag_child_paths(path, paths, pathsep)]

    @classmethod
    def find_dag_sibling_paths(cls, path, paths, pathsep='/'):
        return cls.find_dag_child_paths(
            cls.get_dag_parent_path(path, pathsep), paths, pathsep
        )

    @classmethod
    def find_dag_sibling_names(cls, path, paths, pathsep='/'):
        """
        etc.
        ps = ['/cgm', '/cjd', '/shl', '/cg7', '/lib', '/lib_bck', '/nsa_dev', '/tnt', '/']
        print(
            PthNodeMtd.find_dag_sibling_names(
                '/cgm', ps
            )
        )
        :param path:
        :param paths:
        :param pathsep:
        :return:
        """
        return [cls.get_dag_name(x) for x in cls.find_dag_sibling_paths(path, paths, pathsep)]

    # replace word to '_' unless it's "a-z, A-Z, 0-9"
    @classmethod
    def cleanup_dag_path(cls, path, pathsep='/'):
        return re.sub(
            ur'[^\u4e00-\u9fa5a-zA-Z0-9{}]'.format(pathsep), '_', path
        )

    # leaf path is which path has no children
    @classmethod
    def to_leaf_paths(cls, paths):
        list_ = []
        for i_path in paths:
            i_is_leaf = True
            for j_path in paths:
                j_r = re.match(r'({})/(.*)'.format(i_path), j_path)
                if j_r:
                    i_is_leaf = False
                    break
            if i_is_leaf is True:
                list_.append(i_path)
        return list_


class PthNodeOpt(object):
    PLANT_HSV_MAPPER = dict(
        tree_leaf=(120.0, 0.5, 0.15),
        tree_stem=(40.0, 0.5, 0.15),
        tree_flower=(300.0, 0.25, 0.75),
        #
        shrub_leaf=(110.0, 0.5, 0.15),
        shrub_stem=(60.0, 0.5, 0.15),
        shrub_flower=(300.0, 0.25, 0.75),
        #
        fern_leaf=(100, 0.8, 0.2),
        fern_stem=(100, 0.85, 0.25),
        fern_flower=(300.0, 0.25, 0.75),
        #
        flower_leaf=(90, 0.85, 0.25),
        flower_stem=(90, 0.9, 0.3),
        flower_petal=(300.0, 0.25, 0.75),
        flower_calyx=(100.0, 0.25, 0.75),
        #
        grass_leaf=(80, 0.85, 0.25),
        grass_stem=(80.0, 0.9, 0.3),
        grass_flower=(300.0, 0.25, 0.75),
    )

    def __init__(self, path):
        self.__pathsep = path[0]
        self.__path_text = path

    def get_pathsep(self):
        return self.__pathsep

    pathsep = property(get_pathsep)

    def get_path(self):
        return self.__path_text

    path = property(get_path)

    def get_name(self):
        return PthNodeMtd.get_dag_name(
            path=self.__path_text, pathsep=self.__pathsep
        )

    name = property(get_name)

    def set_name(self, name):
        self.__path_text = self.get_path_as_new_name(name)

    def get_path_as_new_name(self, name):
        parent = self.get_parent_path()
        if parent == self.__pathsep:
            return self.__pathsep.join(
                ['', name]
            )
        return self.__pathsep.join(
            [self.get_parent_path(), name]
        )

    def rename_to(self, name):
        return self.__class__(
            self.get_path_as_new_name(name)
        )

    def get_value(self):
        return self.__path_text

    value = property(get_value)

    def get_root(self):
        return self.__class__(self.pathsep)

    def get_is_root(self):
        return self.path == self.pathsep

    def get_parent_path(self):
        return PthNodeMtd.get_dag_parent_path(
            path=self.__path_text, pathsep=self.__pathsep
        )

    def parent_to_path(self, path):
        # noinspection PyAugmentAssignment
        self.__path_text = path+self.__path_text

    def get_ancestor_paths(self):
        return self.get_component_paths()[1:]

    def get_ancestors(self):
        return [self.__class__(i) for i in self.get_ancestor_paths()]

    def get_parent(self):
        _ = self.get_parent_path()
        if _:
            return self.__class__(
                self.get_parent_path()
            )

    def get_component_paths(self):
        return PthNodeMtd.get_dag_component_paths(
            path=self.__path_text, pathsep=self.__pathsep
        )

    def get_components(self):
        return [self.__class__(i) for i in self.get_component_paths()]

    def translate_to(self, pathsep='/'):
        return self.__class__(
            PthNodeMtd.get_dag_pathsep_replace(
                self.path,
                pathsep_src=self.pathsep,
                pathsep_tgt=pathsep
            )
        )

    def clear_namespace_to(self):
        return self.__class__(
            PthNodeMtd.get_dag_path_with_namespace_clear(
                self.path,
                pathsep=self.pathsep,
                # namespacesep=':',
            )
        )

    def get_name_namespace(self, namespacesep=':'):
        name = self.get_name()
        _ = name.split(namespacesep)
        # print _
        return namespacesep.join(_[:-1])

    def get_color_from_name(self, count=1000, maximum=255, offset=0, seed=0):
        return bsc_cor_raw.RawColorMtd.get_color_from_string(
            self.get_name(), count=count, maximum=maximum, offset=offset, seed=seed
        )

    def get_rgb_from_index(self, index, count, maximum=255, seed=0):
        pass

    def get_path_prettify(self, maximum=18):
        p = self.path
        n = self.name
        #
        d = p[:-len(n)-1]
        c = len(d)
        if c > maximum:
            return u'{}...{}/{}'.format(d[:(int(maximum/2)-3)], d[-(int(maximum/2)):], n)
        return p

    def get_rgb(self, maximum=255):
        return bsc_cor_raw.RawTextOpt(
            self.get_name()
        ).to_rgb__(maximum=maximum, s_p=50, v_p=100)

    def get_plant_rgb(self, maximum=255):
        for k, v in self.PLANT_HSV_MAPPER.items():
            if fnmatch.filter([self.__path_text], '*{}*'.format(k)):
                return bsc_cor_raw.RawColorMtd.hsv2rgb(
                    v[0], v[1], v[2], maximum
                )
        return 0.25, 0.75, 0.5

    def generate_child(self, name):
        return self.__class__(
            PthNodeMtd.get_dag_child_path(
                self.__path_text, name, pathsep=self.__pathsep
            )
        )

    def get_depth(self):
        return len(
            PthNodeMtd.get_dag_args(
                self.__path_text,
                pathsep=self.__pathsep
            )
        )

    def __str__(self):
        return self.__path_text

    def __repr__(self):
        return self.__str__()

    def to_string(self):
        return self.__path_text

    def to_dcc_path(self):
        return re.sub(r'/(\d+)([^/]+)', lambda x: '/_{}{}'.format(x.group(1), x.group(2)), self.__path_text)

    def to_dcc(self):
        return self.__class__(
            self.to_dcc_path()
        )


class PthNodeMapOpt(object):
    """
s = PthNodeMapOpt(
    {
        '/master/mod/hi': '/master/hi',
        '/master/cfx': '/master/aux/cfx',
        '/master/grm': '/master/aux/grm',
    }
)

for i in [
    '/master/mod/hi',
    '/master/mod/hi/a',
    '/master/cfx',
    '/master/grm'
]:
    print s.get(i)
    """

    def __init__(self, mapper, pathsep='/'):
        self._mapper = mapper
        self._mapper_reverse = {v: k for k, v in mapper.items()}
        self._pathsep = pathsep

    def get(self, path):
        for k, v in self._mapper.items():
            if path == k:
                return v
            elif path.startswith(
                    k+self._pathsep
            ):
                return v+path[len(k):]
        return path

    def get_as_reverse(self, path):
        for k, v in self._mapper_reverse.items():
            if path == k:
                return v
            elif path.startswith(
                    k+self._pathsep
            ):
                return v+path[len(k):]
        return path


class PthPortMtd(object):
    @classmethod
    def get_dag_args(cls, path, pathsep='.'):
        return path.split(pathsep)

    @classmethod
    def get_dag_name(cls, path, pathsep='.'):
        return cls.get_dag_args(path, pathsep)[-1]

    @classmethod
    def get_dag_parent_path(cls, path, pathsep='.'):
        dag_args = cls.get_dag_args(path, pathsep)
        if len(dag_args) == 1:
            return None
        elif len(dag_args) == 2:
            return dag_args[0]
        return pathsep.join(dag_args[:-1])

    @classmethod
    def get_dag_component_paths(cls, path, pathsep='.'):
        def _rcs_fnc(lis_, path_):
            if path_ is not None:
                lis_.append(path_)
                _parent_path = cls.get_dag_parent_path(path_, pathsep)
                if _parent_path:
                    _rcs_fnc(lis_, _parent_path)

        lis = []
        _rcs_fnc(lis, path)
        return lis


class PthPortOpt(object):

    def __init__(self, path, pathsep='.'):
        self.__path_text = path
        self.__pathsep = pathsep

    def get_pathsep(self):
        return self.__pathsep

    pathsep = property(get_pathsep)

    def get_path(self):
        return self.__path_text

    path = property(get_path)

    def get_name(self):
        return PthPortMtd.get_dag_name(
            path=self.__path_text, pathsep=self.__pathsep
        )

    def get_is_top_level(self):
        return self.get_parent_path() is None

    def get_component_paths(self):
        return PthPortMtd.get_dag_component_paths(
            path=self.__path_text, pathsep=self.__pathsep
        )

    def get_components(self):
        return [self.__class__(i) for i in self.get_component_paths()]

    def get_parent_path(self):
        return PthPortMtd.get_dag_parent_path(
            path=self.__path_text, pathsep=self.__pathsep
        )

    def get_parent(self):
        _ = self.get_parent_path()
        if _:
            return self.__class__(
                _
            )

    def get_ancestor_paths(self):
        return self.get_component_paths()[1:]

    def to_string(self):
        return self.__path_text

    def __str__(self):
        return self.__path_text

    def __repr__(self):
        return self.__str__()


class PthAttributeMtd(object):
    @classmethod
    def join_by(cls, obj_path, port_path, port_pathsep='.'):
        return port_pathsep.join([obj_path, port_path])

    @classmethod
    def split_by(cls, path, pathsep='.'):
        _ = path.split(pathsep)
        return _[0], pathsep.join(_[1:])


class PthAttributeOpt(object):
    def __init__(self, atr_path, port_pathsep='.'):
        self._path = atr_path
        self._port_pathsep = port_pathsep
        _ = self._path.split(self._port_pathsep)
        self._obj_path = _[0]
        self._port_path = self._port_pathsep.join(_[1:])

    @property
    def path(self):
        return self._path

    @property
    def obj_path(self):
        return self._obj_path

    @property
    def port_path(self):
        return self._port_path

    def to_args(self):
        return self._obj_path, self._port_path
