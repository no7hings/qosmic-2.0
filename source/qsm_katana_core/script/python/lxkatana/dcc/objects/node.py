# coding:utf-8
# katana
from ... import core as ktn_core

from ... import abstracts as ktn_abstracts


class Port(ktn_abstracts.AbsKtnPort):
    def __init__(self, node, name, port_assign):
        super(Port, self).__init__(node, name, port_assign)


class Connection(ktn_abstracts.AbsKtnObjConnection):
    PORT_PATHSEP = ktn_core.KtnUtil.PORT_PATHSEP

    def __init__(self, source, target):
        super(Connection, self).__init__(source, target)


class Node(ktn_abstracts.AbsKtnObj):
    DCC_PORT_CLS = Port
    DCC_CONNECTION_CLS = Connection

    def __init__(self, path):
        super(Node, self).__init__(path)
