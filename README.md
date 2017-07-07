PackageCore
===========

<img src="https://travis-ci.org/BytePackager/packagecore.svg?branch=master"/>

Python library for building Linux packages. It is distributed under the GPLv2
license.


Requirements
------------

PackageCore is written in `python 3` and uses the `PyYAML` module.

PackageCore currently utilizes Docker to provide the distribution environments
for building and testing packages.


Execution
---------

You can build packages by executing:
```
packagecore <version> [<release num>]
```
from the source directory.

In your source directory if `packagecore.yaml` contains the configuration.
Otherwise, the configuration file can be explicitly specified:
```
packagecore -c myfile.yaml <version> [<release num>]
```


Configuration
-------------

PackageCore uses YAML files for configuration. The basic structure is:

```
name: wx-calc 
metadata:
  maintainer: Dominique LaSalle <dominique@bytepackager.com>
  license: GPL3 
  summary: A simple calculator using wxWidgets.
  homepage: https://solidlake.com
commands:
  compile:
    - mkdir build
    - cd build
    - cmake ../ -DCMAKE_INSTALL_PREFIX=/usr
    - make
  install:
    - make install -C build DESTDIR="${BP_DESTDIR}"
  testinstall:
    - ls /usr/bin/wxcalc
packages:
  archlinux:
    buildeps:
      - gcc
      - cmake
    deps:
      - wxgtk
  centos7.3:
    buildeps:
      - gcc 
      - cmake
      - wxGTK3-devel
    deps:
      - wxGTK3
  fedora25:
    buildeps:
      - gcc 
      - cmake
      - wxGTK3-devel
    deps:
      - wxGTK3
  ubuntu16.04:
    buildeps:
      - gcc 
      - cmake
      - libwxgtk3-dev
    deps:
      - libwxgtk3-0v5
```

When executing `install` commands, the environment variable `BP_DESTDIR` is
defined, and should be used as the root directory for installation (e.g.,
specify things like `install -D -m755 mybin ${BP_DESTDIR}/usr/bin/mybin`).

If a specifc Linux distribution requires special commands to build, you can
override the top-level commands inside of the package listing:
```
  centos7.3:
    commands:
      compile:
        - mkdir build
        - cd build
        - cmake ../ -DCMAKE_INSTALL_PREFIX=/usr -DwxWidgets_CONFIG_EXECUTABLE=/usr/bin/wx-config-3.0
```

