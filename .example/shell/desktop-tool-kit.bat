@echo off
pushd %~d0

paper lxdcc qsm-hook-command -o "hook_key=desktop-tools/desktop-tool-kit"

popd
echo. & pause