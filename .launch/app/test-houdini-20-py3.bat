@echo off
pushd %~d0
set QSM_PYTHON_VERSION=3
rez-env houdini-20.0.547 qsm_houdini_main  -- houdini
popd
