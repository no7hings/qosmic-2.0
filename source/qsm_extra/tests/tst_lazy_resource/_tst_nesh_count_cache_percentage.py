# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_lazy.resource.scripts as s

print s.MeshCountDataOpt(
    bsc_storage.StgFileOpt(
        'Z:/caches/temporary/.asset-cache/mesh-count/1MP/4FA75052-080C-3322-8407-850758131841.json'
    ).set_read()['mesh_count']
).non_cache_face_percentage

print s.AssetTag.to_cache_percentage_tag(0)