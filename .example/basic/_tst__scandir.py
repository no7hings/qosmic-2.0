# coding:utf-8
import lxbasic.storage as bsc_storage

print bsc_storage.StgDirectoryOpt(
    '/production/shows/nsa_dev/assets/chr/nikki_rnd/user/team.srf/extend/texture/nn4y_UV_texture'
).get_is_readable()


# print bsc_storage.StgDirectoryOpt(
#     '/production/shows/nsa_dev/assets/chr/nikki_rnd/user/team.srf'
# ).get_all_directories()
