# coding:utf-8
import lxcontent.core as ctt_core

import lxbasic.extra.methods as bsc_etr_methods

import lxresolver.core as rsv_core

r = rsv_core.RsvBase.generate_root()

p = r.get_rsv_project(
    project='nsa_dev'
)


m = bsc_etr_methods.get_module('new')

print m.EtrBase.get_app_execute_mapper(p)

f = m.EtrBase.get_deadline_configure_file(p)

deadline_configure = ctt_core.Content(value=f)

deadline_job_context = 'render'

if deadline_job_context:
    content_0 = deadline_configure.get_as_content(deadline_job_context)
    step = 'srf'
    if step:
        content_1 = content_0.get_as_content(step)
        print content_1
