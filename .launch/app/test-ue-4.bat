@echo off
pushd %~d0
set PYTHONIOENCODING=utf-8
set UE_SHADER_COMPILE_WORKER_THREADS=2
rez-env unreal4 qsm_ue_main pyqt5-5.3.2 ffmpeg -- UE4Editor E:\myworkspace\game\demo_1\MyProject4\MyProject4.uproject
popd
