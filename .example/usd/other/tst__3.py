# coding:utf-8
import parse


fs = [
    "extra.texture_directory+'/tx'+'/texture_name.<udim>.%04d.tx'%(frame)",
    "'/temp/texture_name.<udim>.%04d.tx'%(frame)",
]

f = "extra.texture_directory+'/tx'+'/texture_name.<udim>.%04d.tx'%(frame)"

patterns = [
    ("'{base}'%{argument}", ""),
    ("{extra}'{base}'%{argument}", "")
]

for i_f in fs:
    for i_pattern in patterns:
        i_p = parse.parse(
            i_pattern, i_f
        )
        if i_p:
            i_base = i_p['base']
            i_file_name = i_base.split('/')[-1]
            print i_file_name
            break
