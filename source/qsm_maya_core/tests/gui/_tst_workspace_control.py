# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


def main():
    name = 'TEST'

    # window
    window_name = '{}_window'.format(name)
    if cmds.window(window_name, query=1, exists=1):
        cmds.deleteUI(window_name)
    cmds.window(window_name, width=480, sizeable=1)

    # layout
    layout_name = '{}_layout'.format(name)
    cmds.tabLayout(layout_name, innerMarginWidth=4, innerMarginHeight=4, parent=window_name)

    cmds.columnLayout('abc', columnAttach=('both', 5), rowSpacing=10, columnWidth=250)

    # dock
    dock_name = '{}_dock'.format(name)
    if cmds.dockControl(dock_name, query=1, exists=1):
        cmds.deleteUI(dock_name)

    cmds.dockControl(
        dock_name, area='left', label='TEST', content=window_name, allowedArea=['left', 'right'], sizeable=1, width=480
    )


if __name__ == '__main__':
    main()
