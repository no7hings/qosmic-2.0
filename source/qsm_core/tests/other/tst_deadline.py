# coding:utf-8
import lxbasic.deadline as bsc_deadline

c = bsc_deadline.DdlBase.generate_connection()

print(c.Pools.GetPoolNames())

print(c.Groups.GetGroupNames())
