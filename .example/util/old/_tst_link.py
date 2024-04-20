# coding:utf-8
import os


def create_symlink_fnc(path_src, path_tgt):
    tgt_dir_path = os.path.dirname(path_tgt)
    src_rel_path = os.path.relpath(path_src, tgt_dir_path)
    if os.path.exists(path_tgt) is False:
        print src_rel_path, path_tgt
        os.symlink(src_rel_path, path_tgt)


create_symlink_fnc(
    '/data/f/paper_workspace/pglauncher/src/cjd_config', '/data/f/paper_workspace/pglauncher/src/lib_config'
)
