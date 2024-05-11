# 引号嵌套和&转义
> 多层引号嵌套逻辑, 第二层为\", 第三层为\\\"
> 在引号中的&不需要转义, 其他正常转义为^&
```shell
rez-env qsm_dcc_main maya-2019 usd-20.11 -- maya -batch -command "python(\"print \\\"A&BC\\\"\")"
```

```shell
rez-env qsm_dcc_main maya-2019 usd-20.11 -- maya -batch -command "python(\"import lxsession.commands as ssn_commands;ssn_commands.execute_option_hook(option=\\\"option_hook_key=dcc-process/maya-process&method=fbx-to-usd&fbx=Z:/libraries/resource/all/asset/modular_building_balcony_ukjsdavdw/v0001/geometry/fbx/modular_building_balcony_ukjsdavdw.fbx&usd=Z:/libraries/resource/all/asset/modular_building_balcony_ukjsdavdw/v0001/geometry/usd/modular_building_balcony_ukjsdavdw.usd&use_update_mode=True\\\")\")"
```