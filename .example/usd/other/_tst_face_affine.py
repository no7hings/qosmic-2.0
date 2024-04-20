# coding:utf-8
import lxusd.core as usd_core


points = [(0.9744213, 1.4900274, 2.210894), (2.030162, 1.596985, 1.2760347), (0.39794713, 0.3718635, 0.36228034), (1.2939336, 0.8158903, 0.3552439)]

usd_stage = usd_core.UsdStageOpt()

usd_stage.create_one(
    '/plane', 'Xform'
)

mesh = usd_stage.create_one(
    '/plane/planeShape', 'Mesh'
)

mesh_opt = usd_core.UsdMeshOpt(mesh)
mesh_opt.create(
    [4], [0, 1, 3, 2], points
)
mesh_opt.fill_display_color((1, 0, 0))

a = usd_core.FaceAffine(
    points
)

project_0_points, project_1_points = a.test()

m_project_0 = usd_stage.create_one(
    '/plane/planeShape_project_0', 'Mesh'
)

m_project_0_opt = usd_core.UsdMeshOpt(m_project_0)
m_project_0_opt.create(
    [4], [0, 1, 3, 2], project_0_points
)
m_project_0_opt.fill_display_color((0, 1, 0))

m_project_1 = usd_stage.create_one(
    '/plane/planeShape_project_1', 'Mesh'
)

m_project_1_opt = usd_core.UsdMeshOpt(m_project_1)
m_project_1_opt.create(
    [4], [0, 1, 3, 2], project_1_points
)
m_project_1_opt.fill_display_color((0, 1, 0))


usd_stage.export_to(
    '/data/e/workspace/lynxi/test/maya/vertex-color/test_face_affine.usda'
)
