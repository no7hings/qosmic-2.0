# coding:utf-8
import lxbasic.resource as bsc_resource

parse_configure = bsc_resource.RscExtendConfigure.get_as_content('wsp_task/parse/default')
parse_configure.do_flatten()

print parse_configure
