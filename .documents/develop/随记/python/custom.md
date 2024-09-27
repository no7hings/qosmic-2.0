```
os.path.isfile非常的消耗时间，尽量不要频繁判定
```

```
subprocess.Popen执行的命令中文件名包含中文的处理方式


def ensure_unicode(s):  
    if isinstance(s, six.text_type):  
        return s  
    elif isinstance(s, bytes):  
        return s.decode('utf-8')  
    else:  
        return s

path = _cor_base.ensure_unicode(path)  
path = path.encode('mbcs')

```