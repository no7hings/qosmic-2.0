# coding:utf-8


class RsvPlatforms(object):
    Windows = 'windows'
    Linux = 'linux'
    All = [
        Windows,
        Linux
    ]


class RsvApplications(object):
    Maya = 'maya'
    Houdini = 'houdini'
    Katana = 'katana'
    Clarisse = 'clarisse'
    Nuke = 'nuke'
    Python = 'python'
    Lynxi = 'lynxi'
    #
    DCCS = [
        Maya,
        Houdini,
        Katana,
        Clarisse,
        Nuke
    ]
    All = [
        Maya,
        Houdini,
        Katana,
        Clarisse,
        Nuke,
        Python,
        Lynxi
    ]
    #
    PATHSEP_DICT = {
        Maya: '|',
        Houdini: '/',
        Katana: '/',
        Clarisse: '/',
        Nuke: '/'
    }

    @classmethod
    def get_pathsep(cls, application):
        return cls.PATHSEP_DICT[application]


class RsvEntityCategories(object):
    Project = 'project'
    ResourceGroup = 'resource_group'
    Resource = 'resource'
    Step = 'step'
    Task = 'task'


class RsvEntityTypes(object):
    Project = 'project'
    Role = 'role'
    Asset = 'asset'
    Sequence = 'sequence'
    Shot = 'shot'
    #
    Step = 'step'
    Task = 'task'
    #
    Version = 'version'
    #
    Projects = [
        Project
    ]
    #
    ResourceGroups = [
        Role,
        Sequence
    ]
    #
    Resources = [
        Asset,
        Shot
    ]
    #
    All = [
        Asset,
        Sequence,
        Shot
    ]


class RsvVariantCategories(object):
    Schemes = 'schemes'
    Roles = 'roles'
    Workspaces = 'workspaces'
    #
    ProjectSteps = 'project_steps'
    #
    AssetSteps = 'asset_steps'
    #
    SequenceSteps = 'sequence_steps'
    ShotSteps = 'shot_steps'
    #
    ProjectTasks = 'project_tasks'
    AssetTasks = 'asset_tasks'
    SequenceTasks = 'sequence_tasks'
    ShotTasks = 'shot_tasks'
    #
    All = [
        Schemes,
        Roles,
        Workspaces,
        ProjectSteps, AssetSteps, SequenceSteps, ShotSteps,
        ProjectTasks, AssetTasks, SequenceTasks, ShotTasks
    ]


class RsvVariantTypes(object):
    Root = 'root'

    Project = 'project'
    Workspace = 'workspace'
    WorkspaceKey = 'workspace_key'

    Branch = 'branch'

    Role = 'role'
    Asset = 'asset'

    Sequence = 'sequence'
    Shot = 'shot'

    Step = 'step'
    Task = 'task'
    Version = 'version'

    TaskExtra = 'task_extra'
    VersionExtra = 'version_extra'

    User = 'user'
    Artist = 'artist'

    Inners = [
        Branch
    ]

    Trunks = [
        Project,
        Role, Sequence,
        Asset, Shot,
    ]

    Branches = [
        Step, Task,
        Version,
    ]

    Mains = Trunks+Branches

    VariableTypes = [
        Workspace,
        WorkspaceKey
    ]

    Constructs = [
        Root,
        Project,
        Workspace, WorkspaceKey,
        Branch,
        Role, Sequence,
        Asset, Shot,
        Step, Task,
        Version,
        TaskExtra, VersionExtra,
        User, Artist,
    ]

    Keyword = 'keyword'
    Pattern = 'pattern'
    Result = 'result'

    Category = 'category'
    Type = 'type'
    Path = 'path'

    Update = 'update'

    Extends = [
        Category, Type, Path,
        Keyword, Pattern,
        Result, Update
    ]

    Descriptions = Mains + [Path, Category, Type]


class RsvWorkspaceKeys(object):
    User = 'user'
    Source = 'source'
    Release = 'release'
    Temporary = 'temporary'

    Mains = [
        Source,
        Release
    ]
    All = [
        User,
        Source,
        Release,
        Temporary
    ]


class RsvWorkspaceMatchKeys(object):
    Sources = ['source', 'work']
    Users = ['user']
    Releases = ['release', 'publish']
    Temporaries = ['temporary', 'output']


class RsvVersion(object):
    LATEST = 'latest'
    NEW = 'new'
    ALL = 'all'
