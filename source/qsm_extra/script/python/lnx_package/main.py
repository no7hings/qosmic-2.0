# coding:utf-8
from __future__ import print_function

import sys

import os

import pkg_resources


class PythonPackages(object):
    def __init__(self):
        pass

    @classmethod
    def get_package_info(cls, package_name):
        try:
            dist = pkg_resources.get_distribution(package_name)

            print(dist.project_name)
            print(dist.version)
            return dict(

            )
        except pkg_resources.DistributionNotFound:
            # sys.stderr.write('unresolved package: {}.\n'.format(package_name))
            return None

    @classmethod
    def get_all_packages(cls):
        python_paths = sys.path

        list_ = []

        for i_python_path in python_paths:
            if os.path.isdir(i_python_path):
                for j_dir_name in os.listdir(i_python_path):
                    j_package_path = os.path.join(i_python_path, j_dir_name)
                    if os.path.isdir(j_package_path):
                        if (
                            os.path.exists(os.path.join(j_package_path, '__init__.py'))
                            or os.path.exists(os.path.join(j_package_path, '__init__.pyc'))
                        ):
                            j_package_name = j_dir_name
                            i_info = cls.get_package_info(j_dir_name)
                            if i_info:
                                print(i_info)
                                list_.append(j_package_name)
                            else:
                                print(j_package_name, j_package_path, 'CCC')
        return list_

    def generate_dependent_tree(self):
        for i in pkg_resources.working_set:
            print(i, i.requires())

    @classmethod
    def test(cls):
        p = cls()
        p.generate_dependent_tree()

