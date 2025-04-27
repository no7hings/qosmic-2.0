@echo off
pushd %~d0
set QSM_PYTHON_VERSION=3
set QSM_UI_LANGUAGE=chs
rez-env qsm_main pyside2-5.15.2 ffmpeg -- qsm-hook-python -o "hook_key=desktop-tools/qsm-lazy-workspace"
popd
