# coding:utf-8
import os

import pkgutil

import importlib

import lnx_nexsolve.node_type as t

dir_path = os.path.dirname(t.__file__)

all_names = os.listdir(dir_path)

for i in all_names:
    if i .startswith('__init__'):
        continue
    if i.endswith('.pyc'):
        continue

    i_module_name = '{}.{}'.format(t.__name__, os.path.splitext(i)[0])
    if pkgutil.find_loader(i_module_name):
        i_module = importlib.import_module(i_module_name)
        i_module.__dict__['register']()
