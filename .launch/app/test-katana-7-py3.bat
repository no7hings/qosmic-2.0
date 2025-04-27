@echo off
pushd %~d0
set QSM_PYTHON_VERSION=3
rez-env katana-7.0v2 ktoa-4.2.5.0 qsm_katana_main  -- katana
popd
