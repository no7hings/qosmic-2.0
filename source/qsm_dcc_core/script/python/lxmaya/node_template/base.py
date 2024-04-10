# coding:utf-8
import inspect

import os.path

import re

import types

from contextlib import contextmanager
# noinspection PyUnresolvedReferences
import maya.mel as mel
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
from maya import OpenMayaUI
# noinspection PyUnresolvedReferences,PyPep8Naming
import pymel.core as pm

from PySide2 import QtCore, QtGui, QtWidgets

import shiboken2

_OBJECT_STORE = {}


# for convert python func to mel script
def ae_py_to_mel_proc(py_object, args=(), return_type=None, proc_name=None, use_name=False, proc_prefix='pyToMel_'):
    mel_params = []
    py_params = []
    mel_return = return_type if return_type else ''
    #
    for t, n in args:
        mel_params.append('%s $%s'%(t, n))
        #
        if t == 'string':
            py_params.append(r"""'"+$%s+"'"""%n)
        else:
            py_params.append(r'"+$%s+"'%n)
    #
    py_object_id = id(py_object)
    #
    d = {}
    #
    if proc_name:
        d['proc_name'] = proc_name
    elif use_name:
        d['proc_name'] = py_object.__name__
    else:
        if isinstance(py_object, types.LambdaType):
            proc_prefix += '_lambda'
        elif isinstance(py_object, (types.FunctionType, types.BuiltinFunctionType)):
            try:
                proc_prefix += '_'+py_object.__name__
            except (AttributeError, TypeError):
                pass
        elif isinstance(py_object, types.MethodType):
            try:
                proc_prefix += '_'+py_object.im_class.__name__+'_'+py_object.__name__
            except (AttributeError, TypeError):
                pass
        d['proc_name'] = '%s%s'%(proc_prefix, py_object_id)
    #
    d['proc_name'] = d['proc_name'].replace('<', '_').replace('>', '_').replace('-', '_')
    d['mel_params'] = ', '.join(mel_params)
    d['py_params'] = ', '.join(py_params)
    d['mel_return'] = mel_return
    d['this_module'] = __name__
    d['id'] = py_object_id
    #
    contents = '''global proc %(mel_return)s %(proc_name)s(%(mel_params)s){'''
    if mel_return:
        contents += 'return '
    contents += '''python("import %(this_module)s;%(this_module)s._OBJECT_STORE[%(id)s](%(py_params)s)");}'''
    mel.eval(contents%d)
    _OBJECT_STORE[py_object_id] = py_object
    return d['proc_name']


def ae_callback(func):
    return ae_py_to_mel_proc(func, [('string', 'nodeName')], proc_prefix='AECallback')


def capitalize(s):
    return s[0].upper()+s[1:] if s else s


def get_name_prettify(s):
    return ' '.join([capitalize(x) for x in re.findall('[a-zA-Z][a-z]*[0-9]*', s)])


def toCamelCase(s):
    parts = s.split('_')
    return ''.join([parts[0]]+[capitalize(x) for x in parts[1:]])


def attrTextFieldGrp(*args, **kwargs):
    attribute = kwargs.pop('attribute', kwargs.pop('a', None))
    assert attribute is not None, "You Must Passed an Attribute"
    #
    changeCommand = kwargs.pop('changeCommand', kwargs.pop('cc', None))
    if changeCommand:
        # noinspection PyCallingNonCallable
        def cc(newVal):
            cmds.setAttr(attribute, newVal, type="string")
            changeCommand(newVal)
    else:
        def cc(newVal):
            cmds.setAttr(attribute, newVal, type="string")
    #
    if kwargs.pop('edit', kwargs.pop('e', False)):
        ctrl = args[0]
        cmds.textFieldGrp(
            ctrl,
            edit=True,
            text=cmds.getAttr(attribute),
            changeCommand=cc
        )
        cmds.scriptJob(
            parent=ctrl,
            replacePrevious=True,
            attributeChange=[attribute, lambda: cmds.textFieldGrp(ctrl, edit=True, text=cmds.getAttr(attribute))]
        )
    elif kwargs.pop('query', kwargs.pop('q', False)):
        pass
    else:
        labelText = kwargs.pop('label', None)
        if not labelText:
            labelText = mel.eval('interToUI(\"{}\")'.format(attribute.split('.')[-1]))
        #
        ctrl = None
        if len(args) > 0:
            ctrl = args[0]
            cmds.textFieldGrp(
                ctrl,
                label=labelText,
                text=cmds.getAttr(attribute),
                changeCommand=cc
            )
        else:
            ctrl = cmds.textFieldGrp(
                label=labelText,
                text=cmds.getAttr(attribute),
                changeCommand=cc
            )
        #
        cmds.scriptJob(
            parent=ctrl,
            attributeChange=[attribute, lambda: cmds.textFieldGrp(ctrl, edit=True, text=cmds.getAttr(attribute))]
        )
        return ctrl


def attrType(attr):
    t = cmds.getAttr(attr, type=True)
    if t == 'float3':
        node, at = attr.split('.', 1)
        if cmds.attributeQuery(at, node=node, usedAsColor=1):
            t = 'color'
    return t


def modeMethod(func):
    def wrapped(self, *args, **kwargs):
        modeFunc = getattr(self._mode, func.__name__)
        if self._record:
            self._actions.append((modeFunc, args, kwargs))
        else:
            modeFunc(*args, **kwargs)

    #
    wrapped.__doc__ = func.__doc__
    wrapped.__name__ = func.__name__
    wrapped._orig = func
    return wrapped


def modeAttrMethod(func):
    def wrapped(self, attr, *args, **kwargs):
        assert isinstance(attr, basestring), "%r.%s: attr argument must be a string, got %s"%(
        self, func.__name__, type(attr).__name__)
        #
        modeFunc = getattr(self._mode, func.__name__)
        if self.convertToMayaStyle:
            attr = toCamelCase(attr)
        if self._record:
            self._actions.append((modeFunc, (attr,)+args, kwargs))
        else:
            modeFunc(attr, *args, **kwargs)
        #
        self._attributes.append(attr)

    #
    wrapped.__doc__ = func.__doc__
    wrapped.__name__ = func.__name__
    wrapped._orig = func
    return wrapped


def swatchLabel(nodeName):
    nodeType = cmds.nodeType(nodeName)
    classificationsList = cmds.getClassification(nodeType)
    for classification in classificationsList:
        allClassList = classification.split(':')
        for allClass in allClassList:
            classList = allClass.split('/')
            if 'swatch' == classList[0]:
                continue
            else:
                if classList:
                    if 'shader' != classList[-1]:
                        classList = filter(lambda x: x != 'shader', classList)
                    return "\n".join(map(lambda x: x.capitalize(), classList))
                else:
                    return "Sample"


def swatchDisplayNew(plugName):
    nodeAndAttrs = plugName.split(".")
    node = nodeAndAttrs[0]

    cmds.formLayout('swatchDisplayForm')
    cmds.text('swatchLabel', label=swatchLabel(node))
    cmds.swatchDisplayPort('swatchDisplay', wh=(64, 64), rs=64)
    #
    cmds.popupMenu('swatchPopup', button=3)
    cmds.menuItem('swatchSmall', label='Small')
    cmds.menuItem('swatchMedium', label='Medium')
    cmds.menuItem('swatchLarge', label='Large')
    #
    cmds.setParent(upLevel=True)
    gTextColumnWidthIndex = mel.eval("$tempVar=$gTextColumnWidthIndex;")
    cmds.formLayout(
        'swatchDisplayForm',
        edit=True,
        af=[
            ('swatchLabel', "top", 0),
            ('swatchLabel', "bottom", 0),
            ('swatchDisplay', "top", 0),
            ('swatchDisplay', "bottom", 0)
        ],
        aof=[
            ('swatchLabel', "right", -gTextColumnWidthIndex)
        ],
        an=[
            ('swatchLabel', "left"),
            ('swatchDisplay', "right")
        ],
        ac=[
            ('swatchDisplay', "left", 5, 'swatchLabel')
        ]
    )
    swatchDisplayReplace(plugName)


def swatchDisplayReplace(plugName):
    nodeAndAttrs = plugName.split(".")
    node = nodeAndAttrs[0]
    #
    cmds.swatchDisplayPort(
        'swatchDisplay',
        edit=True,
        shadingNode=node,
        annotation='Refresh Swatch',
        pressCommand=lambda *args: mel.eval("updateFileNodeSwatch "+node)
    )
    cmds.popupMenu('swatchPopup', edit=True, button=3)
    cmds.menuItem(
        'swatchSmall',
        edit=True,
        command=lambda *args: cmds.swatchDisplayPort('swatchDisplay', edit=True, wh=(64, 64), rs=64)
    )
    cmds.menuItem(
        'swatchMedium',
        edit=True,
        command=lambda *args: cmds.swatchDisplayPort('swatchDisplay', edit=True, wh=(96, 96), rs=96)
    )
    cmds.menuItem(
        'swatchLarge',
        edit=True,
        command=lambda *args: cmds.swatchDisplayPort('swatchDisplay', edit=True, wh=(128, 128), rs=128)
    )
    cmds.text('swatchLabel', edit=True, label=swatchLabel(node))


def file_button_fnc(*args):
    _atr_path = args[0]
    _file_path = cmds.getAttr(_atr_path)
    #
    _directory_path = os.path.dirname(_file_path)
    #
    __file_paths = cmds.fileDialog2(
        fileFilter='All Files (*.*)',
        cap='Load File',
        okc='Load',
        fm=4,
        dir=_directory_path
    ) or []
    if __file_paths:
        __file_path = __file_paths[0]
        cmds.setAttr(_atr_path, __file_path, type="string")


def file_new_fnc(atr_path):
    def edit_fnc_(new_file_path_):
        cmds.setAttr(atr_path, new_file_path_, type="string")

    #
    _ = atr_path.split('.')
    obj_name = _[0]
    port_name = _[-1]
    node_type_name = cmds.nodeType(obj_name)
    gui_name_0 = '{}_{}_entry'.format(node_type_name, port_name)
    gui_name_1 = '{}_{}_button'.format(node_type_name, port_name)
    label = get_name_prettify(port_name)
    #
    cmds.rowLayout(
        nc=2,
        cw2=(360, 30),
        cl2=('left', 'left'),
        adjustableColumn=1,
        columnAttach=[(1, 'left', -4), (2, 'left', 0)]
    )
    cmds.textFieldGrp(
        gui_name_0,
        label=label,
        changeCommand=edit_fnc_
    )
    cmds.textFieldGrp(
        gui_name_0,
        edit=True,
        text=cmds.getAttr(atr_path)
    )
    cmds.symbolButton(
        gui_name_1,
        image='folder-closed.png',
        command=lambda arg=None, x=atr_path: file_button_fnc(x)
    )
    cmds.scriptJob(
        parent=gui_name_0,
        replacePrevious=True,
        attributeChange=[
            atr_path,
            lambda: cmds.textFieldGrp(gui_name_0, edit=True, text=cmds.getAttr(atr_path))
        ]
    )


def file_replace_fnc(atr_path):
    _ = atr_path.split('.')
    obj_name = _[0]
    port_name = _[-1]
    node_type_name = cmds.nodeType(obj_name)
    gui_name_0 = '{}_{}_entry'.format(node_type_name, port_name)
    gui_name_1 = '{}_{}_button'.format(node_type_name, port_name)
    #
    cmds.textFieldGrp(
        gui_name_0,
        edit=True,
        text=cmds.getAttr(atr_path)
    )
    cmds.symbolButton(
        gui_name_1,
        edit=True,
        image='folder-closed.png',
        command=lambda arg=None, x=atr_path: file_button_fnc(x)
    )
    cmds.scriptJob(
        parent=gui_name_0,
        replacePrevious=True,
        attributeChange=[
            atr_path,
            lambda: cmds.textFieldGrp(gui_name_0, edit=True, text=cmds.getAttr(atr_path))
        ]
    )


class baseMode(object):
    def __init__(self, template):
        self.template = template

    @property
    def nodeName(self):
        return self.template.nodeName

    @property
    def attr(self):
        return self.template.attr

    #
    def nodeType(self):
        self.template.nodeType()

    #
    def nodeAttr(self, attr):
        return self.template.nodeAttr(attr)

    #
    def nodeAttrExists(self, attr):
        return self.template.nodeAttrExists(attr)


class rootMode(baseMode):
    def __init__(self, template):
        super(rootMode, self).__init__(template)
        #
        self._atr_path = None
        #
        self._nodeName = None
        self._type = self.template.nodeType()

    #
    def _updateCallback(self, nodeAttr):
        self.template._doUpdate(nodeAttr.split('.')[0])

    #
    def preSetup(self):
        self.addCustom('message', self._updateCallback, self._updateCallback)

    #
    def postSetup(self):
        pass

    #
    def update(self):
        pass

    #
    def addTemplate(self, attr, template):
        if template._isRootMode():
            template._doSetup(self.nodeAttr(attr))
        else:
            self.addChildTemplate(attr, template)

    @staticmethod
    def addChildTemplate(attr, template):
        template._setToChildMode()
        template._record = True
        template.setup()
        for attr in template._attributes:
            try:
                cmds.editorTemplate(suppress=attr)
            except RuntimeError:
                pass
        cmds.editorTemplate(
            ae_callback(template._doSetup),
            ae_callback(template._doUpdate),
            attr,
            callCustom=True
        )

    @staticmethod
    def _set_control_add_(attr, label=None, changeCommand=None, annotation=None, preventOverride=False, dynamic=False):
        if not label:
            label = get_name_prettify(attr)
        #
        args = [attr]
        kwargs = {}
        #
        if dynamic:
            kwargs['addDynamicControl'] = True
        else:
            kwargs['addControl'] = True
        #
        if changeCommand:
            if hasattr(changeCommand, '__call__'):
                changeCommand = ae_callback(changeCommand)
            #
            args.append(changeCommand)
        if label:
            kwargs['label'] = label
        if annotation:
            kwargs['annotation'] = annotation
        #
        cmds.editorTemplate(*args, **kwargs)

    @classmethod
    def _set_enumerate_control_add_(cls, port_path, enumerate_option):
        def new_fnc_(atr_path_):
            _ = atr_path_.split('.')
            _obj_name = _[0]
            _port_name = _[-1]
            _node_type_name = cmds.nodeType(_obj_name)
            _gui_name = '{}__{}__button'.format(_node_type_name, _port_name)
            #
            _enumerate_items = [
                (_seq, _i) for _seq, _i in enumerate(enumerate_option.split('|'))
            ]
            cmds.setUITemplate(
                'attributeEditorPresetsTemplate',
                pushTemplate=True
            )
            cmds.attrEnumOptionMenuGrp(
                _gui_name,
                attribute=atr_path_,
                label=label,
                enumeratedItem=_enumerate_items
            )
            cmds.setUITemplate(popTemplate=True)

        def replace_fnc_(atr_path_):
            _ = atr_path_.split('.')
            _obj_name = _[0]
            _port_name = _[-1]
            _node_type_name = cmds.nodeType(_obj_name)
            _gui_name = '{}__{}__button'.format(_node_type_name, _port_name)
            #
            cmds.attrEnumOptionMenuGrp(
                _gui_name,
                edit=True,
                attribute=atr_path_
            )

        #
        label = get_name_prettify(port_path)
        #
        cls.addCustom(port_path, new_fnc_, replace_fnc_)

    @classmethod
    def _set_file_name_control_add_(cls, port_path):
        cls.addCustom(
            port_path, file_new_fnc, file_replace_fnc
        )

    @classmethod
    def addControl(
            cls, attr, label=None, changeCommand=None, annotation=None, preventOverride=False, dynamic=False,
            useAsFileName=False, enumerateOption=None
            ):
        if enumerateOption is not None:
            cls._set_enumerate_control_add_(
                attr, enumerateOption
            )
        elif useAsFileName is True:
            cls._set_file_name_control_add_(
                attr
            )
        else:
            cls._set_control_add_(
                attr,
                label,
                changeCommand,
                annotation,
                preventOverride,
                dynamic
            )

    @staticmethod
    def suppress(attr):
        cmds.editorTemplate(suppress=attr)

    @staticmethod
    def addCustom(attr, newFunc, replaceFunc):
        if hasattr(newFunc, '__call__'):
            newFunc = ae_callback(newFunc)
        if hasattr(replaceFunc, '__call__'):
            replaceFunc = ae_callback(replaceFunc)
        args = (newFunc, replaceFunc, attr)
        cmds.editorTemplate(callCustom=1, *args)

    @staticmethod
    def addSeparator():
        cmds.editorTemplate(addSeparator=True)

    @staticmethod
    def dimControl(nodeName, control, state):
        cmds.editorTemplate(dimControl=(nodeName, control, state))

    @staticmethod
    def beginLayout(name, collapse=True):
        cmds.editorTemplate(beginLayout=name, collapse=collapse)

    @staticmethod
    def endLayout():
        cmds.editorTemplate(endLayout=True)

    @staticmethod
    def beginScrollLayout():
        cmds.editorTemplate(beginScrollLayout=True)

    @staticmethod
    def endScrollLayout():
        cmds.editorTemplate(endScrollLayout=True)

    @staticmethod
    def beginNoOptimize():
        cmds.editorTemplate(beginNoOptimize=True)

    @staticmethod
    def endNoOptimize():
        cmds.editorTemplate(endNoOptimize=True)

    @staticmethod
    def interruptOptimize():
        cmds.editorTemplate(interruptOptimize=True)

    @staticmethod
    def addComponents():
        cmds.editorTemplate(addComponents=True)

    @staticmethod
    def addExtraControls(label=None):
        kwargs = {}
        if label:
            kwargs['extraControlsLabel'] = label
        cmds.editorTemplate(addExtraControls=True, **kwargs)


class AttrControlGrp(object):
    uiTypeDic = {
        'float': cmds.attrFieldSliderGrp,
        'float2': cmds.attrFieldGrp,
        'float3': cmds.attrFieldGrp,
        'color': cmds.attrColorSliderGrp,
        'bool': cmds.attrControlGrp,
        'long': cmds.attrFieldSliderGrp,
        'byte': cmds.attrFieldSliderGrp,
        'long2': cmds.attrFieldGrp,
        'long3': cmds.attrFieldGrp,
        'short': cmds.attrFieldSliderGrp,
        'short2': cmds.attrFieldGrp,
        'short3': cmds.attrFieldGrp,
        'enum': cmds.attrEnumOptionMenuGrp,
        'double': cmds.attrFieldSliderGrp,
        'double2': cmds.attrFieldGrp,
        'double3': cmds.attrFieldGrp,
        'string': attrTextFieldGrp,
        'message': cmds.attrNavigationControlGrp
    }

    def __init__(self, attribute, *args, **kwargs):
        self.attribute = attribute
        self.type = kwargs.pop('type', kwargs.pop('typ', None))
        #
        if not self.type:
            self.type = attrType(self.attribute)

        if self.type in ['color', 'enum', 'message']:
            self.callback = kwargs.pop('changeCommand', None)
        else:
            self.callback = None
        kwargs['attribute'] = self.attribute
        if self.type not in self.uiTypeDic:
            return
        cmd = self.uiTypeDic[self.type]
        try:
            self.control = cmd(*args, **kwargs)
        except RuntimeError:
            print "Error creating %s:"%cmd.__name__
            raise
        if self.callback:
            cmds.scriptJob(
                attributeChange=[self.attribute, self.callback],
                replacePrevious=True,
                parent=self.control
            )

    #
    def edit(self, **kwargs):
        kwargs['edit'] = True
        if self.type not in self.uiTypeDic:
            return
        self.uiTypeDic[self.type](self.control, **kwargs)

    #
    def setAttribute(self, attribute):
        self.attribute = attribute
        if self.type not in self.uiTypeDic:
            return
        self.uiTypeDic[self.type](self.control, edit=True, attribute=self.attribute)
        if self.callback:
            cmds.scriptJob(
                attributeChange=[self.attribute, self.callback],
                replacePrevious=True,
                parent=self.control
            )


class childMode(baseMode):
    def __init__(self, template):
        super(childMode, self).__init__(template)
        self._controls = []
        self._layoutStack = []

    #
    def preSetup(self):
        cmds.setUITemplate('attributeEditorTemplate', pushTemplate=True)
        self._layoutStack = [cmds.setParent(query=True)]

    @staticmethod
    def postSetup():
        cmds.setUITemplate(popTemplate=True)

    #
    def update(self):
        cmds.setUITemplate('attributeEditorTemplate', pushTemplate=True)
        try:
            for attr, updateFunc, parent in self._controls:
                cmds.setParent(parent)
                updateFunc(self.nodeAttr(attr))
        except:
            print("Template %r Failed to Update Attribute '%s'"%(self.template, self.attr))
            raise
        finally:
            cmds.setUITemplate(popTemplate=True)

    #
    def addTemplate(self, attr, template):
        self.addChildTemplate(attr, template)

    #
    def addChildTemplate(self, attr, template):
        template._setToChildMode()
        template._record = True
        template.setup()
        for attr in template._attributes:
            try:
                cmds.editorTemplate(suppress=attr)
            except RuntimeError:
                pass
        self.addCustom(attr, template._doSetup, template._doUpdate)

    #
    def addControl(
            self, attr, label=None, changeCommand=None, annotation=None, preventOverride=False, dynamic=False,
            enumeratedItem=None
            ):
        if not label:
            label = get_name_prettify(attr)
        #
        kwargs = {'label': label, 'attribute': self.nodeAttr(attr)}
        if annotation:
            kwargs['annotation'] = annotation
        if changeCommand:
            kwargs['changeCommand'] = changeCommand
        if enumeratedItem:
            kwargs['enumeratedItem'] = enumeratedItem
        #
        parent = self._layoutStack[-1]
        cmds.setParent(parent)
        control = AttrControlGrp(**kwargs)
        #
        self._controls.append((attr, control.setAttribute, parent))

    #
    def addCustom(self, attr, createFunc, updateFunc):
        parent = self._layoutStack[-1]
        cmds.setParent(parent)
        col = cmds.columnLayout(adj=True)
        #
        createFunc(self.nodeAttr(attr))
        cmds.setParent(parent)
        self._controls.append((attr, updateFunc, col))

    @staticmethod
    def addSeparator():
        cmds.separator()

    #
    def beginLayout(self, label, **kwargs):
        kwargs['label'] = label
        cmds.setParent(self._layoutStack[-1])
        cmds.frameLayout(**kwargs)
        self._layoutStack.append(cmds.columnLayout(adjustableColumn=True))

    #
    def endLayout(self):
        self._layoutStack.pop()
        cmds.setParent(self._layoutStack[-1])

    #
    def beginNoOptimize(self):
        pass

    #
    def endNoOptimize(self):
        pass

    #
    def beginScrollLayout(self):
        pass

    #
    def endScrollLayout(self):
        pass

    #
    def addExtraControls(self):
        pass


class AbsTemplateBase(object):
    def __init__(self, nodeType):
        self._type = nodeType
        self._nodeName = None
        self._atr_path = None

    #
    def __repr__(self):
        return '%s(%r)'%(self.__class__.__name__, self._type)

    @property
    def nodeName(self):
        return self._nodeName

    @property
    def attr(self):
        return self._atr_path

    #
    def nodeType(self):
        if self._type is None:
            self._type = cmds.objectType(self.nodeName)
        return self._type

    #
    def nodeAttr(self, attr=None):
        if attr is None:
            attr = self.attr
        return self.nodeName+'.'+attr

    #
    def nodeAttrExists(self, attr):
        return cmds.addAttr(self.nodeAttr(attr), q=1, ex=1)


class AbsNodeTemplate(AbsTemplateBase):
    convertToMayaStyle = False

    def __init__(self, nodeType):
        super(AbsNodeTemplate, self).__init__(nodeType)
        #
        self._rootMode = rootMode(self)
        self._childMode = childMode(self)
        #
        self._mode = self._rootMode
        self._actions = []
        self._attributes = []
        self._record = False

    #
    def _setToRootMode(self):
        self._mode = self._rootMode

    #
    def _isRootMode(self):
        return self._mode == self._rootMode

    #
    def _setToChildMode(self):
        self._mode = self._childMode

    #
    def _isChildMode(self):
        return self._mode == self._childMode

    #
    def _setActiveNodeAttr(self, nodeName):
        parts = nodeName.split('.', 1)
        self._nodeName = parts[0]
        if len(parts) > 1:
            self._atr_path = parts[1]

    #
    def _doSetup(self, nodeAttr):
        self._setActiveNodeAttr(nodeAttr)
        self._mode.preSetup()
        if self._record:
            for func, args, kwargs in self._actions:
                func(*args, **kwargs)
        else:
            self.setup()
        self._mode.postSetup()

    #
    def _doUpdate(self, nodeAttr):
        self._setActiveNodeAttr(nodeAttr)
        self._mode.update()

    @modeMethod
    def update(self):
        pass

    @modeAttrMethod
    def addTemplate(self, attr, template):
        pass

    @modeAttrMethod
    def addChildTemplate(self, attr, template):
        pass

    @modeAttrMethod
    def addControl(
            self, attr, label=None, changeCommand=None, annotation=None, preventOverride=False, dynamic=False,
            useAsFileName=False, enumerateOption=None
            ):
        pass

    @modeMethod
    def suppress(self, attr):
        pass

    @modeMethod
    def addSeparator(self):
        pass

    @modeAttrMethod
    def addCustom(self, attr, createFunc, updateFunc):
        pass

    @modeMethod
    def beginLayout(self, label, **kwargs):
        pass

    @modeMethod
    def endLayout(self):
        pass

    @modeMethod
    def beginNoOptimize(self):
        pass

    @modeMethod
    def endNoOptimize(self):
        pass

    @modeMethod
    def beginScrollLayout(self):
        pass

    @modeMethod
    def endScrollLayout(self):
        pass

    @modeMethod
    def addExtraControls(self):
        pass

    @contextmanager
    def scroll_layout(self):
        # noinspection PyArgumentList
        self.beginScrollLayout()
        yield
        # noinspection PyArgumentList
        self.endScrollLayout()

    @contextmanager
    def layout(self, label, **kwargs):
        # noinspection PyArgumentList
        self.beginLayout(label, **kwargs)
        yield
        # noinspection PyArgumentList
        self.endLayout()

    #
    def addSwatch(self):
        self.addCustom("message", swatchDisplayNew, swatchDisplayReplace)

    # for override
    def setup(self):
        pass

    @classmethod
    def get_qt_object(cls, maya_ui_name, qt_type=QtWidgets.QWidget):
        ptr = OpenMayaUI.MQtUtil.findControl(maya_ui_name)
        if ptr is None:
            ptr = OpenMayaUI.MQtUtil.findLayout(maya_ui_name)
            if ptr is None:
                ptr = OpenMayaUI.MQtUtil.findMenuItem(maya_ui_name)
        #
        if ptr is not None:
            obj = shiboken2.wrapInstance(long(ptr), qt_type)
            return obj

    @classmethod
    def get_current_widget(cls):
        currentWidgetName = cmds.setParent(query=True)
        return cls.get_qt_object(currentWidgetName)

    def create_port(self, atr_path):
        pass

    def set_port_replace(self, atr_path):
        pass


class AeMtd(object):
    CACHE = {}

    @classmethod
    def set_ae_register(cls, node_type, class_path):
        cls.CACHE[node_type] = class_path

        proc_name = 'AE%sTemplate'%node_type
        script = '''global proc %s(string $node_name){python("from lxmaya.node_template import base as mya_node_template_base; mya_node_template_base.AeMtd.set_load('%s','" + $node_name + "')");}'''%(
            proc_name, node_type
        )
        mel.eval(script)

    @classmethod
    def set_load(cls, node_type, node_name):
        try:
            if node_type in cls.CACHE:
                class_path = cls.CACHE[node_type]
                modules = class_path.split('.')
                class_name = modules[-1]
                module_name = '.'.join(modules[:-1])
                if module_name:
                    import importlib

                    import imp

                    module = importlib.import_module(module_name)
                    imp.reload(module)

                    class_obj = module.__dict__[class_name]
                    class_obj(node_name)
        except Exception as e:
            print 'Error loading AE Template for node type {}'.format(node_type)
            import traceback

            traceback.print_exc()


class AeMtd2(object):
    @classmethod
    def aeProc(cls, modName, objName, procName):
        contents = '''global proc %(procName)s( string $nodeName ){python("import %(__name__)s;%(__name__)s.aeLoader('%(modName)s','%(objName)s','" + $nodeName + "')");}'''
        d = locals().copy()
        d['__name__'] = __name__
        mel.eval(contents%d)

    @classmethod
    def aeLoader(cls, modName, objName, nodeName):
        mod = __import__(modName, globals(), locals(), [objName], -1)
        try:
            f = getattr(mod, objName)
            if inspect.isfunction(f):
                f(nodeName)
            elif inspect.isclass(f):
                inst = f(cmds.nodeType(nodeName))
                inst._doSetup(nodeName)
            else:
                print "AE Object %s has Invalid Type %s"%(f, type(f))
        except Exception:
            print "Failed to Load Python Attribute Editor Template '%s.%s'"%(modName, objName)
            import traceback

            traceback.print_exc()


class ControlBase(object):
    @classmethod
    def get_gui_key(cls, atr_path):
        _ = atr_path.split('.')
        node, port_path = _
        node_type = cmds.nodeType(node)
        return 'GUI_{}__{}'.format(node_type, port_path)

    @classmethod
    def get_gui_replace_args(cls, atr_path):
        _ = atr_path.split('.')
        node, keys = _
        node_type = cmds.nodeType(node)
        list_ = []
        for i_index, i_key in enumerate(keys.split('&')):
            list_.append(
                (i_key, 'GUI_{}__{}'.format(node_type, i_key))
            )
        return node, list_

    @classmethod
    def get_gui_new_args(cls, atr_path, labels, icons):
        _ = atr_path.split('.')
        node, keys = _
        node_type = cmds.nodeType(node)
        list_ = []
        for i_index, i_key in enumerate(keys.split('&')):
            i_label = labels.split('&')[i_index]
            i_icon = icons.split('&')[i_index]
            list_.append(
                (i_key, 'GUI_{}__{}'.format(node_type, i_key), i_label, i_icon)
            )
        return node, list_

    @classmethod
    def gui_new_fnc(cls, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def gui_replace_fnc(cls, *args, **kwargs):
        raise NotImplementedError()


class FileControl(ControlBase):
    @classmethod
    def gui_update_value(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        value = cmds.getAttr(atr_path) or ''
        cmds.textFieldGrp(
            gui_key,
            edit=True,
            text=value,
            annotation='attribute="{}"'.format(atr_path)
        )

    @classmethod
    def gui_update_edit_callback(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        cmds.textFieldGrp(
            gui_key,
            edit=1,
            changeCommand=lambda x: cls.dcc_update_value(atr_path),
        )
        cmds.symbolButton(
            gui_key+'__button',
            edit=1,
            command=lambda x: cls.dcc_update_value_by_button(atr_path)
        )

    #
    @classmethod
    def dcc_update_value(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        value = cmds.getAttr(atr_path) or ''
        value_new = cmds.textFieldGrp(
            gui_key,
            query=1,
            text=1
        ) or ''
        if value_new != value:
            cmds.setAttr(atr_path, value_new, type="string")

    @classmethod
    def dcc_update_value_by_button(cls, atr_path):
        import os

        gui_key = cls.get_gui_key(atr_path)
        value = cmds.getAttr(atr_path) or ''
        #
        results = cmds.fileDialog2(
            fileFilter='All Files (*.*)',
            cap='Load File',
            okc='Load',
            fm=4,
            dir=os.path.dirname(value)
        ) or []
        if results:
            value_new = results[0]
            if value_new != value:
                cmds.setAttr(atr_path, value_new, type="string")
                cmds.textFieldGrp(
                    gui_key,
                    edit=1,
                    text=value_new
                )

    @classmethod
    def dcc_update_attribute_change_callback(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        cmds.scriptJob(
            parent=gui_key,
            replacePrevious=True,
            attributeChange=[
                atr_path,
                lambda: cls.gui_update_value(atr_path)
            ]
        )

    #
    @classmethod
    def gui_new_fnc(cls, atr_path, label):
        gui_key = cls.get_gui_key(atr_path)
        #
        cmds.rowLayout(
            nc=2,
            cw2=(360, 30),
            cl2=('left', 'left'),
            adjustableColumn=1,
            columnAttach=[(1, 'left', -2), (2, 'left', 0)]
        )
        cmds.textFieldGrp(
            gui_key,
            label=label
        )
        cmds.symbolButton(
            gui_key+'__button',
            image='folder-closed.png'
        )
        cls.gui_update_edit_callback(atr_path)
        cls.gui_update_value(atr_path)
        cls.dcc_update_attribute_change_callback(atr_path)

    @classmethod
    def gui_replace_fnc(cls, atr_path):
        cls.gui_update_edit_callback(atr_path)
        cls.gui_update_value(atr_path)
        cls.dcc_update_attribute_change_callback(atr_path)


class EnumerateControl(ControlBase):
    @classmethod
    def get_dcc_values(cls, enumerate_option):
        return enumerate_option.split('|')

    @classmethod
    def get_gui_values(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        return [cmds.menuItem(i, query=1, label=1) for i in cmds.optionMenuGrp(gui_key, query=1, itemListLong=1) or []]

    @classmethod
    def gui_build_and_update_value(cls, atr_path, enumerate_option):
        gui_key = cls.get_gui_key(atr_path)
        #
        gui_values = cls.get_gui_values(atr_path)
        values = cls.get_dcc_values(enumerate_option)
        if values != gui_values:
            [cmds.deleteUI(i) for i in cmds.optionMenuGrp(gui_key, query=1, itemListLong=1) or []]
            for i_index, i_version in enumerate(values):
                cmds.menuItem(
                    label=i_version, data=i_index,
                    parent=gui_key+'|OptionMenu'
                )
        #
        cls.gui_update_value(atr_path)

    @classmethod
    def gui_update_value(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        #
        values = cls.get_gui_values(atr_path)
        value_current = cmds.getAttr(atr_path)
        if value_current in values:
            index = values.index(value_current)
            cmds.optionMenuGrp(
                gui_key,
                edit=1,
                select=index+1,
                annotation='attribute="{}"'.format(atr_path)
            )
        else:
            cmds.optionMenuGrp(
                gui_key,
                edit=1,
                select=1,
                annotation='attribute="{}"'.format(atr_path)
            )

    @classmethod
    def gui_update_edit_callback(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        cmds.optionMenuGrp(
            gui_key,
            edit=1,
            changeCommand=lambda x: cls.dcc_update_value(atr_path)
        )

    @classmethod
    def dcc_update_value(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        items = cmds.optionMenuGrp(gui_key, query=1, itemListLong=1)
        index = cmds.optionMenuGrp(gui_key, query=1, select=1)
        value_current = cmds.getAttr(atr_path)
        value_current_new = cmds.menuItem(items[index-1], query=1, label=1)
        if value_current_new != value_current:
            cmds.setAttr(
                atr_path, value_current_new, type='string'
            )

    @classmethod
    def dcc_update_attribute_change_callback(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        #
        cmds.scriptJob(
            parent=gui_key,
            replacePrevious=True,
            attributeChange=[
                atr_path,
                lambda: cls.gui_update_value(atr_path)
            ]
        )

    @classmethod
    def gui_new_fnc(cls, atr_path, label, enumerate_option):
        gui_key = cls.get_gui_key(atr_path)
        cmds.optionMenuGrp(
            gui_key,
            label=label
        )
        cls.gui_build_and_update_value(atr_path, enumerate_option)
        cls.gui_update_edit_callback(atr_path)
        cls.dcc_update_attribute_change_callback(atr_path)

    @classmethod
    def gui_replace_fnc(cls, atr_path, enumerate_option):
        cls.gui_build_and_update_value(atr_path, enumerate_option)
        cls.gui_update_edit_callback(atr_path)
        cls.dcc_update_attribute_change_callback(atr_path)


class IconButtonControls(ControlBase):
    @classmethod
    def execute_fnc(cls, *args, **kwargs):
        print args, kwargs

    @classmethod
    def gui_new_fnc(cls, atr_path, labels, icons, data_port_path):
        node_, gui_args = cls.get_gui_new_args(atr_path, labels, icons)
        cmds.columnLayout(
            adjustableColumn=2,
            rowSpacing=4,
            # backgroundColor=(.15, .15, .15)
        )
        cmds.rowLayout(
            numberOfColumns=4,
            adjustableColumn=1,
            columnWidth4=[120]*4,
            columnAttach4=['both']*4,
            columnAlign4=['center']*4,
            columnOffset4=[2]*4
        )
        cmds.text(label='')
        for i_key, i_gui_key, i_label, i_icon in gui_args:
            cmds.nodeIconButton(
                i_gui_key,
                style='iconAndTextHorizontal',
                image1=i_icon,
                label=i_label,
                command=lambda key=i_key, node=node_: cls.execute_fnc(key=key, node=node)
            )

    @classmethod
    def gui_replace_fnc(cls, atr_path, data_port_path):
        node_, gui_args = cls.get_gui_replace_args(atr_path)
        for i_key, i_gui_key in gui_args:
            cmds.nodeIconButton(
                i_gui_key,
                edit=1,
                command=lambda key=i_key, node=node_: cls.execute_fnc(key=key, node=node)
            )


class TextControl(ControlBase):
    @classmethod
    def gui_update_value(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        value = cmds.getAttr(atr_path) or ''
        cmds.textFieldGrp(
            gui_key,
            edit=True,
            text=value,
            annotation='attribute="{}"'.format(atr_path)
        )

    @classmethod
    def gui_update_edit_callback(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        cmds.textFieldGrp(
            gui_key,
            edit=1,
            changeCommand=lambda x: cls.dcc_update_value(atr_path)
        )

    #
    @classmethod
    def dcc_update_value(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        value = cmds.getAttr(atr_path) or ''
        value_new = cmds.textFieldGrp(
            gui_key,
            query=1,
            text=1
        ) or ''
        if value_new != value:
            cmds.setAttr(atr_path, value_new, type="string")

    @classmethod
    def dcc_update_attribute_change_callback(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        cmds.scriptJob(
            parent=gui_key,
            replacePrevious=True,
            attributeChange=[
                atr_path,
                lambda: cls.gui_update_value(atr_path)
            ]
        )

    #
    @classmethod
    def gui_new_fnc(cls, atr_path, label, lock=False):
        gui_key = cls.get_gui_key(atr_path)
        #
        cmds.textFieldGrp(
            gui_key,
            label=label,
            editable=not lock,
        )
        cls.gui_update_edit_callback(atr_path)
        cls.gui_update_value(atr_path)
        cls.dcc_update_attribute_change_callback(atr_path)

    @classmethod
    def gui_replace_fnc(cls, atr_path):
        cls.gui_update_edit_callback(atr_path)
        cls.gui_update_value(atr_path)
        cls.dcc_update_attribute_change_callback(atr_path)


class DataControls(ControlBase):
    @classmethod
    def get_dcc_value_data(cls, atr_path):
        raw = cmds.getAttr(
            atr_path
        )
        try:
            _ = eval(raw)
            if isinstance(_, dict):
                return _
        except SyntaxError as e:
            pass
        return {}

    @classmethod
    def get_gui_key_data(cls, atr_path, build_port_path, build_key):
        _ = atr_path.split('.')
        node, port_path = _
        data_atr_path = '{}.{}'.format(node, build_port_path)
        raw = cmds.getAttr(
            data_atr_path
        )
        try:
            _ = eval(raw)
            if isinstance(_, dict):
                if port_path in _:
                    data = _[port_path]
                    return data.get(build_key) or []
        except SyntaxError as e:
            pass
        return []

    #
    @classmethod
    def gui_update_value(cls, atr_path, key_data):
        data = cls.get_dcc_value_data(atr_path)
        gui_key = cls.get_gui_key(atr_path)
        for i_key, i_label in key_data:
            i_gui_key = gui_key+'__'+i_key
            if i_key in data:
                i_value = data[i_key]
            else:
                i_value = ''
            #
            cmds.textFieldGrp(
                i_gui_key,
                edit=1,
                text=i_value,
                annotation='attribute="{}"\nkey="{}"'.format(atr_path, i_key)
            )

    @classmethod
    def dcc_update_attribute_change_callback(cls, atr_path, key_data):
        gui_key = cls.get_gui_key(atr_path)
        cmds.scriptJob(
            parent=gui_key,
            replacePrevious=True,
            attributeChange=[
                atr_path,
                lambda: cls.gui_update_value(atr_path, key_data)
            ]
        )

    #
    @classmethod
    def gui_new_fnc(cls, atr_path, build_port_path, build_key):
        key_data = cls.get_gui_key_data(atr_path, build_port_path, build_key)
        gui_key = cls.get_gui_key(atr_path)
        cmds.columnLayout(
            gui_key,
            adjustableColumn=1,
            # backgroundColor=(.275, .275, .275)
        )
        for i_key, i_label in key_data:
            i_gui_key = gui_key+'__'+i_key
            cmds.textFieldGrp(
                i_gui_key,
                label=i_label,
                editable=False
            )
        cls.gui_update_value(atr_path, key_data)
        cls.dcc_update_attribute_change_callback(atr_path, key_data)

    @classmethod
    def gui_replace_fnc(cls, atr_path, build_port_path, build_key):
        key_data = cls.get_gui_key_data(atr_path, build_port_path, build_key)
        #
        cls.gui_update_value(atr_path, key_data)
        cls.dcc_update_attribute_change_callback(atr_path, key_data)


class VariantControl(ControlBase):
    @classmethod
    def get_dcc_values(cls, atr_path, data_port_path):
        _ = atr_path.split('.')
        node, port_path = _
        data_atr_path = '{}.{}'.format(node, data_port_path)
        raw = cmds.getAttr(
            data_atr_path
        )
        try:
            _ = eval(raw)
            if isinstance(_, dict):
                if port_path in _:
                    data = _[port_path]
                    return data['all'], data['default']
        except SyntaxError as e:
            pass
        return ['None'], 'None'

    @classmethod
    def get_gui_values(cls, atr_path):
        gui_key = cls.get_gui_key(atr_path)
        return [cmds.menuItem(i, query=1, label=1) for i in cmds.optionMenuGrp(gui_key, query=1, itemListLong=1) or []]

    #
    @classmethod
    def gui_build_and_update_value(cls, atr_path, data_port_path):
        gui_key = cls.get_gui_key(atr_path)
        #
        gui_values = cls.get_gui_values(atr_path)
        values, value_default = cls.get_dcc_values(atr_path, data_port_path)
        if values != gui_values:
            [cmds.deleteUI(i) for i in cmds.optionMenuGrp(gui_key, query=1, itemListLong=1) or []]
            for i_index, i_version in enumerate(values):
                cmds.menuItem(
                    label=i_version, data=i_index,
                    parent=gui_key+'|OptionMenu'
                )
        #
        cls.gui_update_value(atr_path, data_port_path)

    @classmethod
    def gui_update_value(cls, atr_path, data_port_path):
        gui_key = cls.get_gui_key(atr_path)
        #
        values = cls.get_gui_values(atr_path)
        value_current = cmds.getAttr(atr_path)
        if value_current in values:
            index = values.index(value_current)
            cmds.optionMenuGrp(
                gui_key,
                edit=1,
                select=index+1,
                annotation='attribute="{}"'.format(atr_path)
            )
        else:
            cmds.optionMenuGrp(
                gui_key,
                edit=1,
                select=1,
                annotation='attribute="{}"'.format(atr_path)
            )
        #
        cls.gui_check_value(atr_path, data_port_path)

    @classmethod
    def gui_update_edit_callback(cls, atr_path, data_port_path):
        gui_key = cls.get_gui_key(atr_path)
        cmds.optionMenuGrp(
            gui_key,
            edit=1,
            changeCommand=lambda x: cls.dcc_update_value(atr_path, data_port_path)
        )

    #
    @classmethod
    def dcc_update_value(cls, atr_path, data_port_path):
        gui_key = cls.get_gui_key(atr_path)
        items = cmds.optionMenuGrp(gui_key, query=1, itemListLong=1)
        index = cmds.optionMenuGrp(gui_key, query=1, select=1)
        value_current = cmds.getAttr(atr_path)
        value_current_new = cmds.menuItem(items[index-1], query=1, label=1)
        if value_current_new != value_current:
            cmds.setAttr(
                atr_path, value_current_new, type='string'
            )
        cls.gui_check_value(atr_path, data_port_path)

    @classmethod
    def dcc_update_attribute_change_callback(cls, atr_path, data_port_path):
        gui_key = cls.get_gui_key(atr_path)
        #
        cmds.scriptJob(
            parent=gui_key,
            replacePrevious=True,
            attributeChange=[
                atr_path,
                lambda: cls.gui_update_value(atr_path, data_port_path)
            ]
        )

    #
    @classmethod
    def gui_update_value_by_data(cls, atr_path, data_port_path):
        gui_key = cls.get_gui_key(atr_path)
        #
        gui_values = cls.get_gui_values(atr_path)
        values, value_default = cls.get_dcc_values(atr_path, data_port_path)
        if values != gui_values:
            [cmds.deleteUI(i) for i in cmds.optionMenuGrp(gui_key, query=1, itemListLong=1) or []]
            for i_index, i_version in enumerate(values):
                cmds.menuItem(
                    label=i_version, data=i_index,
                    parent=gui_key+'|OptionMenu'
                )
        cls.gui_update_value(atr_path, data_port_path)

    @classmethod
    def dcc_update_data_change_callback(cls, atr_path, data_port_path):
        _ = atr_path.split('.')
        node, port_path = _

        gui_key = cls.get_gui_key(atr_path)

        data_atr_path = '{}.{}'.format(node, data_port_path)
        cmds.scriptJob(
            parent=gui_key,
            replacePrevious=True,
            attributeChange=[
                data_atr_path,
                lambda: cls.gui_update_value_by_data(atr_path, data_port_path)
            ]
        )

    #
    @classmethod
    def gui_check_value(cls, atr_path, data_port_path):
        values, value_default = cls.get_dcc_values(atr_path, data_port_path)
        gui_key = cls.get_gui_key(atr_path)
        value_current = cmds.getAttr(atr_path)
        if value_current != 'None':
            if value_current == value_default:
                cmds.optionMenu(gui_key+'|OptionMenu', edit=1, backgroundColor=(.125, 0.75, 0.5))
            else:
                cmds.optionMenu(gui_key+'|OptionMenu', edit=1, backgroundColor=(.75, 0.75, 0.125))
        else:
            cmds.optionMenu(gui_key+'|OptionMenu', edit=1, backgroundColor=(.375, 0.375, 0.375))

    #
    @classmethod
    def gui_new_fnc(cls, atr_path, label, data_port_path):
        gui_key = cls.get_gui_key(atr_path)
        cmds.optionMenuGrp(
            gui_key,
            label=label
        )
        cls.gui_update_edit_callback(atr_path, data_port_path)
        cls.gui_build_and_update_value(atr_path, data_port_path)
        cls.dcc_update_attribute_change_callback(atr_path, data_port_path)
        cls.dcc_update_data_change_callback(atr_path, data_port_path)

    @classmethod
    def gui_replace_fnc(cls, atr_path, data_port_path):
        cls.gui_update_edit_callback(atr_path, data_port_path)
        cls.gui_build_and_update_value(atr_path, data_port_path)
        cls.dcc_update_attribute_change_callback(atr_path, data_port_path)
        cls.dcc_update_data_change_callback(atr_path, data_port_path)


class AbsNodeTemplateNew(pm.ui.AETemplate):
    def __init__(self, node_name):
        super(AbsNodeTemplateNew, self).__init__(node_name)
        self.setup()

    @contextmanager
    def scroll_layout(self):
        # noinspection PyArgumentList
        self.beginScrollLayout()
        yield
        # noinspection PyArgumentList
        self.endScrollLayout()

    @contextmanager
    def layout(self, label, **kwargs):
        # noinspection PyArgumentList
        self.beginLayout(label, **kwargs)
        yield
        # noinspection PyArgumentList
        self.endLayout()

    def _add_text_control_(self, port_path, label, lock=False):
        self.addCustom(
            port_path,
            lambda atr_path: TextControl.gui_new_fnc(atr_path, label, lock),
            lambda atr_path: TextControl.gui_replace_fnc(atr_path)
        )

    def _add_file_control_(self, port_path, label):
        self.addCustom(
            port_path,
            lambda atr_path: FileControl.gui_new_fnc(atr_path, label),
            lambda atr_path: FileControl.gui_replace_fnc(atr_path)
        )

    def _add_enumerate_control_(self, port_path, label, enumerate_option):
        self.addCustom(
            port_path,
            lambda atr_path: EnumerateControl.gui_new_fnc(atr_path, label, enumerate_option),
            lambda atr_path: EnumerateControl.gui_replace_fnc(atr_path, enumerate_option)
        )

    def _add_variant_control_(self, port_path, label, data_port_path):
        self.addCustom(
            port_path,
            lambda atr_path: VariantControl.gui_new_fnc(atr_path, label, data_port_path),
            lambda atr_path: VariantControl.gui_replace_fnc(atr_path, data_port_path)
        )

    def _add_data_controls_(self, port_path, build_port_path, build_key):
        self.addCustom(
            port_path,
            lambda atr_path: DataControls.gui_new_fnc(atr_path, build_port_path, build_key),
            lambda atr_path: DataControls.gui_replace_fnc(atr_path, build_port_path, build_key)
        )

    def _add_button_controls_(self, keys, labels, icons, data_port_path):
        self.addCustom(
            keys,
            lambda atr_path: IconButtonControls.gui_new_fnc(atr_path, labels, icons, data_port_path),
            lambda atr_path: IconButtonControls.gui_replace_fnc(atr_path, data_port_path)
        )

    @staticmethod
    def addCustom(attr, newFunc, replaceFunc):
        if hasattr(newFunc, '__call__'):
            newFunc = ae_callback(newFunc)
        if hasattr(replaceFunc, '__call__'):
            replaceFunc = ae_callback(replaceFunc)
        args = (newFunc, replaceFunc, attr)
        cmds.editorTemplate(callCustom=1, *args)

    def setup(self):
        raise NotImplementedError()
