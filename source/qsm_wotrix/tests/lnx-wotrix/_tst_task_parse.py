# coding:utf-8
import lxbasic.resource as bsc_resource

parse_configure = bsc_resource.BscConfigure.get_as_content('parsor/parse/default')
parse_configure.do_flatten()

print(parse_configure)
