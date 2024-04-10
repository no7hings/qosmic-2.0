# coding:utf-8
import lxbasic.core as bsc_core


class AbsObjDagPath(object):
    def __init__(self, path):
        self._pathsep = path[0]
        self._path = path

    @property
    def pathsep(self):
        return self._pathsep

    def get_name(self):
        return bsc_core.PthNodeMtd.get_dag_name(
            path=self._path, pathsep=self._pathsep
        )

    name = property(get_name)

    @property
    def path(self):
        return self._path

    def get_root(self):
        return self.__class__(self.pathsep)

    def get_is_root(self):
        return self.path == self.pathsep

    def get_parent_path(self):
        return bsc_core.PthNodeMtd.get_dag_parent_path(
            path=self._path, pathsep=self._pathsep
        )

    def parent_to_path(self, path):
        # noinspection PyAugmentAssignment
        self._path = path+self._path

    def get_ancestor_paths(self):
        return self.get_component_paths()[1:]

    def get_parent(self):
        _ = self.get_parent_path()
        if _:
            return self.__class__(
                self.get_parent_path()
            )

    def get_component_paths(self):
        return bsc_core.PthNodeMtd.get_dag_component_paths(
            path=self._path, pathsep=self._pathsep
        )

    def get_components(self):
        return [self.__class__(i) for i in self.get_component_paths()]

    def translate_to(self, pathsep):
        return self.__class__(
            bsc_core.PthNodeMtd.get_dag_pathsep_replace(
                self.path,
                pathsep_src=self.pathsep,
                pathsep_tgt=pathsep
            )
        )

    def clear_namespace_to(self):
        return self.__class__(
            bsc_core.PthNodeMtd.get_dag_path_with_namespace_clear(
                self.path,
                pathsep=self.pathsep,
                namespacesep=':'
            )
        )

    def __str__(self):
        return self._path

    def to_string(self):
        return self._path


class AbsPortDagPath(object):
    PATHSEP = '.'

    def __init__(self, path):
        self._pathsep = self.PATHSEP
        self._path = path

    @property
    def name(self):
        return bsc_core.PthPortMtd.get_dag_name(
            path=self._path, pathsep=self._pathsep
        )

    @property
    def pathsep(self):
        return self._pathsep

    @property
    def path(self):
        return self._path

    def get_parent_path(self):
        return bsc_core.PthNodeMtd.get_dag_parent_path(
            path=self._path, pathsep=self._pathsep
        )
