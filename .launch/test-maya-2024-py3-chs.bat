@echo off
pushd %~d0
set MAYA_UI_LANGUAGE=zh_CN
set QSM_UI_LANGUAGE=chs
set QSM_PYTHON_VERSION=3
rez-env maya-2024 aces-1.2 qsm_maya_main  -- maya
popd
