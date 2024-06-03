# coding:utf-8
import maya.utils
import maya.cmds
def doSphere( radius ):
	maya.cmds.sphere( radius=radius )
maya.utils.executeInMainThreadWithResult( doSphere, 5.0 )