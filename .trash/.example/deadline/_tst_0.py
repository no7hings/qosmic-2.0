# coding:utf-8
from Deadline import DeadlineConnect

import json

con = DeadlineConnect.DeadlineCon("192.168.16.240", 8082)

jobId = "60374ab2179787b779e93af5"

# j = con.Tasks.connectionProperties.__get__("/api/tasks?JobID={}".format(jobId))
# print json.dumps(
#     j,
#     indent=4
# )

j = con.Tasks.connectionProperties.__get__("/api/jobreports?JobID="+jobId)
print len(j)
print json.dumps(
    j,
    indent=4
)
print len(con.Tasks.connectionProperties.__get__("/api/taskreports?JobID="+jobId+"&TaskID="+str(97)+"&Data=alllogcontents"))

# print a
# raw = a[0]
#
# for i in raw.split('\n'):
#     print i

