@echo off
pushd %~d0
if exist %HOMEDRIVE%%HOMEPATH%\packages\qsm_main (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_main is exists
) else (
    mkdir  %HOMEDRIVE%%HOMEPATH%\packages\qsm_main
)
if exist  %HOMEDRIVE%%HOMEPATH%\packages\qsm_main\99.99.99 (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_main\99.99.99 is exists
) else (
    mklink /D %HOMEDRIVE%%HOMEPATH%\packages\qsm_main\99.99.99 E:\myworkspace\qosmic-2.0\source\qsm_main
)
if exist %HOMEDRIVE%%HOMEPATH%\packages\qsm_core (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_core is exists
) else (
    mkdir  %HOMEDRIVE%%HOMEPATH%\packages\qsm_core
)
if exist  %HOMEDRIVE%%HOMEPATH%\packages\qsm_core\99.99.99 (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_core\99.99.99 is exists
) else (
    mklink /D %HOMEDRIVE%%HOMEPATH%\packages\qsm_core\99.99.99 E:\myworkspace\qosmic-2.0\source\qsm_core
)
if exist %HOMEDRIVE%%HOMEPATH%\packages\qsm_gui (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_gui is exists
) else (
    mkdir  %HOMEDRIVE%%HOMEPATH%\packages\qsm_gui
)
if exist  %HOMEDRIVE%%HOMEPATH%\packages\qsm_gui\99.99.99 (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_gui\99.99.99 is exists
) else (
    mklink /D %HOMEDRIVE%%HOMEPATH%\packages\qsm_gui\99.99.99 E:\myworkspace\qosmic-2.0\source\qsm_gui
)
if exist %HOMEDRIVE%%HOMEPATH%\packages\qsm_lib (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_lib is exists
) else (
    mkdir  %HOMEDRIVE%%HOMEPATH%\packages\qsm_lib
)
if exist  %HOMEDRIVE%%HOMEPATH%\packages\qsm_lib\99.99.99 (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_lib\99.99.99 is exists
) else (
    mklink /D %HOMEDRIVE%%HOMEPATH%\packages\qsm_lib\99.99.99 E:\myworkspace\qosmic-2.0\source\qsm_lib
)
if exist %HOMEDRIVE%%HOMEPATH%\packages\qsm_resource (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_resource is exists
) else (
    mkdir  %HOMEDRIVE%%HOMEPATH%\packages\qsm_resource
)
if exist  %HOMEDRIVE%%HOMEPATH%\packages\qsm_resource\99.99.99 (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_resource\99.99.99 is exists
) else (
    mklink /D %HOMEDRIVE%%HOMEPATH%\packages\qsm_resource\99.99.99 E:\myworkspace\qosmic-2.0\source\qsm_resource
)
if exist %HOMEDRIVE%%HOMEPATH%\packages\qsm_extra (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_extra is exists
) else (
    mkdir  %HOMEDRIVE%%HOMEPATH%\packages\qsm_extra
)
if exist  %HOMEDRIVE%%HOMEPATH%\packages\qsm_extra\99.99.99 (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_extra\99.99.99 is exists
) else (
    mklink /D %HOMEDRIVE%%HOMEPATH%\packages\qsm_extra\99.99.99 E:\myworkspace\qosmic-2.0\source\qsm_extra
)
if exist %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_main (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_main is exists
) else (
    mkdir  %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_main
)
if exist  %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_main\99.99.99 (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_main\99.99.99 is exists
) else (
    mklink /D %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_main\99.99.99 E:\myworkspace\qosmic-2.0\source\qsm_dcc_main
)
if exist %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_core (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_core is exists
) else (
    mkdir  %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_core
)
if exist  %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_core\99.99.99 (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_core\99.99.99 is exists
) else (
    mklink /D %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_core\99.99.99 E:\myworkspace\qosmic-2.0\source\qsm_dcc_core
)
if exist %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_gui (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_gui is exists
) else (
    mkdir  %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_gui
)
if exist  %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_gui\99.99.99 (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_gui\99.99.99 is exists
) else (
    mklink /D %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_gui\99.99.99 E:\myworkspace\qosmic-2.0\source\qsm_dcc_gui
)
if exist %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_lib (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_lib is exists
) else (
    mkdir  %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_lib
)
if exist  %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_lib\99.99.99 (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_lib\99.99.99 is exists
) else (
    mklink /D %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_lib\99.99.99 E:\myworkspace\qosmic-2.0\source\qsm_dcc_lib
)
if exist %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_resource (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_resource is exists
) else (
    mkdir  %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_resource
)
if exist  %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_resource\99.99.99 (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_resource\99.99.99 is exists
) else (
    mklink /D %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_resource\99.99.99 E:\myworkspace\qosmic-2.0\source\qsm_dcc_resource
)
if exist %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_extra (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_extra is exists
) else (
    mkdir  %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_extra
)
if exist  %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_extra\99.99.99 (
    echo %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_extra\99.99.99 is exists
) else (
    mklink /D %HOMEDRIVE%%HOMEPATH%\packages\qsm_dcc_extra\99.99.99 E:\myworkspace\qosmic-2.0\source\qsm_dcc_extra
)
popd
echo. & pause