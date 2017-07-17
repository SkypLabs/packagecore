Building your first package with PackageCore
============================================

Lets assume you have a program the follow the normal Linux build process of
`./configure`, `make`, and `make install`.

Add the file `packagecore.yaml` to the root of the programs source code with
the following contents:

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
      - make
      - gcc
  ubuntu16.04:
    builddeps:
      - make
      - gcc
```

This configuration will generate one package for Arch Linux and one package for
Ubuntu 16.04.

To do so, execute:
```
packagecore 0.1.0 1
```
in the same directory. This will generate the packages
`mypackage_0.1.0-1_ubuntu1604.amd64.deb` and
`mypackage-0.1.0-1.x86_64.pkg.tar.xz`.
