>python包中的.pth文件只会在"{python-root}/Lib/site-packages"下起作用

## Maya 2019 Numpy
> 用管理员权限打开cmd命令窗口
```
cd C:\Program Files\Autodesk\Maya2019\bin
mayapy -m pip install package-name/wheel

mayapy -m pip install numpy==1.9.2

```

## Maya 2020 Numpy

```
cd C:\Program Files\Autodesk\Maya2020\bin

mayapy -m pip install numpy==1.9.2

mayapy -m pip install opencv-python==2.9.0
```
## OpenCv

| OpenCV | NumPy  |
| ------ | ------ |
| 2.x    | 1.6.x  |
| 3.x    | 1.11.x |
| 4.x    | 1.16.x |
## Maya破解失败
```
C:\Program Files (x86)\Common Files\Autodesk Shared\AdskLicensing
uninstall.exe
重新安装
{root}\Autodesk Maya 2020.4 Win\x86\Licensing\AdskLicensing-installer.exe
```

## psutil

```
cd C:\Program Files\Autodesk\Maya2020\bin

mayapy -m pip install psutil==2.2.1

mayapy -m pip install C:/Users/nothings/Downloads/psutil-2.2.1-cp27-none-win_amd64.whl
```