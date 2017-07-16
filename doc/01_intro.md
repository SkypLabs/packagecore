Building your first package with PackageCore
============================================

Lets assume you have a program the follow the normal Linux build process of
`./configure`, `make`, and `make install`.

```
name: mypackage 
commands:
  compile: |
    ./configure --prefix="/usr" && \
    make
  install: |
    make install DESTDIR="${BP_DESTDIR}"
packages:
  archlinux:
    builddeps:
      - gcc
  centos7.3:
    builddeps:
      - gcc
    commands:
      pre:
        - yum install epel-release
  debian9:
    builddeps:
      - gcc
  fedora25:
    builddeps:
      - gcc
  ubuntu16.04:
    builddeps:
      - gcc
  ubuntu17.10:
    builddeps:
      - gcc
    
    
```
