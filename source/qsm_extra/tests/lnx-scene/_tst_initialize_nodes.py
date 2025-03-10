# coding:utf-8
import os

import pkgutil

import importlib

import lnx_scene.node_graph.nodes as module

dir_path = os.path.dirname(module.__file__)

all_names = os.listdir(dir_path)

for i in all_names:
    if i .startswith('__init__'):
        continue
    if i.endswith('.pyc'):
        continue

    i_module_name = '{}.{}'.format(module.__name__, os.path.splitext(i)[0])
    if pkgutil.find_loader(i_module_name):
        i_module = importlib.import_module(i_module_name)
        i_module.__dict__['register']()
