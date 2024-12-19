# coding:utf-8
import maya.cmds as cmds

import basic_usage

bones = cmds.ls(selection=1, type='joint')

if bones:
    result = cmds.promptDialog(
        title='Modify Gravity',
        message='Entry Multiply',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel',
        style='float'
    )
    if result == 'OK':
        value = cmds.promptDialog(query=True, text=True)

        for i_bone in bones:
            i_c = cmds.listConnections(i_bone+'.rotate', destination=0, source=1, type='boneDynamicsNode')
            if i_c:
                i_n = i_c[0]
                cmds.setAttr(i_n+'.gravityMultiply', value)
