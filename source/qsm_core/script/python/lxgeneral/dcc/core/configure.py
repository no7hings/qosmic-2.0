# coding:utf-8


class DccMeshData(object):
    FaceVertices = 'face_vertices'
    Points = 'points'


class DccMeshCheckStatus(object):
    NonChanged = 'non-changed'
    #
    Deletion = 'deletion'
    Addition = 'addition'
    #
    NameChanged = 'name-changed'
    PathChanged = 'path-changed'
    PathExchanged = 'path-exchanged'
    #
    FaceVerticesChanged = 'face-vertices-changed'
    PointsChanged = 'points-changed'
    #
    GeometryChanged = 'geometry-changed'
    #
    All = [
        NonChanged,
        # custom
        Deletion, Addition,
        # naming and group
        NameChanged, PathChanged, PathExchanged,
        # topology
        FaceVerticesChanged, PointsChanged, GeometryChanged
    ]


class DccPort(object):
    VALIDATION_IGNORES = 'lx_validation_ignore'
    VALIDATION_CHECK_IGNORES = 'lx_validation_check_ignore'
    VALIDATION_REPAIR_IGNORES = 'lx_validation_repair_ignore'
    #
    GEOMETRY_UUIDS = 'lx_geometry_uuid'
