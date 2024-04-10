# encoding=utf-8
import inspect

import sys

import os

import imp

import pkgutil
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel


def setup_node_template_prcs(directory_paths):
    templates = []
    for i in directory_paths:
        sys_paths = sys.path
        if os.path.exists(i):
            if i not in sys_paths:
                sys.path.insert(0, i)
    #
    for _, i_module_name, _ in pkgutil.iter_modules(directory_paths):
        if i_module_name.startswith('ae_') and i_module_name not in templates:
            i_node_name = i_module_name[len('ae_'):]
            # noinspection PyBroadException
            try:
                module = __import__(i_module_name, globals(), locals(), [], -1)
                i_proc_name = 'AE{}Template'.format(i_node_name)
                i_method_name = i_node_name
                if hasattr(module, i_method_name):
                    templates.append(i_method_name)
                    register_node_template_prc(i_module_name, i_method_name, i_proc_name)
            except Exception:
                print 'error loading ae template file "{}"'.format(i_node_name)
                import traceback

                print traceback.format_exc()


def register_node_template_prc(module_name, method_name, proc_name):
    contents = '''global proc %(proc_name)s( string $nodeName ){python("import %(__name__)s;%(__name__)s.load_node_template_prc('%(module_name)s','%(method_name)s','" + $nodeName + "')");}'''
    d = locals().copy()
    d['__name__'] = __name__
    mel.eval(contents%d)


# noinspection PyPep8Naming
def load_node_template_prc(module_name, method_name, nodeName):
    # noinspection PyBroadException
    try:
        module = __import__(module_name, globals(), locals(), [], -1)
        # noinspection PyUnresolvedReferences
        imp.reload(module)
        method = module.__dict__[method_name]
        if inspect.isfunction(method):
            method(nodeName)
        elif inspect.isclass(method):
            inst = method(cmds.nodeType(nodeName))
            if hasattr(inst, '_doSetup'):
                inst._doSetup(nodeName)
        else:
            print "AE Object %s has Invalid Type %s"%(method, type(method))
    except Exception as e:
        print "Failed to Load Python Attribute Editor Template '%s.%s'"%(module_name, method_name)
        import traceback

        traceback.print_exc()
