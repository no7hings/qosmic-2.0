# coding:utf-8
import uncompyle6

filepath = 'Z:/temporaries/pyc_to_py/argument.pyc'

original_filepath = 'Z:/temporaries/pyc_to_py/argument.py'
with open(original_filepath, 'w') as f:
    uncompyle6.decompile_file(filepath, f)
