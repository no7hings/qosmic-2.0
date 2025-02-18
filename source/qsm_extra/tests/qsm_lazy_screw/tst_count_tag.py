# coding:utf-8
import lnx_resora.resource_types.asset.scripts as s

print(s.AssetTag.to_face_count_tag(
    10000
))

print(s.AssetTag.to_memory_size_tag(
    4507869184
))
