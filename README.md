PackageCore
===========

<img src="https://travis-ci.org/BytePackager/packagecore.svg?branch=master"/>

<img src="https://circleci.com/gh/BytePackager/packagecore/tree/master.svg?style=svg"/>

Python 3 library for building Linux packages. Works in [Travis-CI](#travis-ci-usage) and [Circle-CI](#circle-ci-usage).



Requirements
------------

PackageCore is written in `python 3` and uses the `PyYAML` module.

PackageCore currently utilizes Docker to provide the distribution environments
for building and testing packages.



Installation
------------

The easiest way to get PackageCore is via `pip`.

```
pip3 install packagecore
```

Alternatively, Linux packages are provided on our release page or you can
install in manually from this repo using the `setup.py` module.

```
./setup.py install
```



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

Use the `-h` flag to get a full list of options:
```
packagecore -h
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


<a name="travis-ci-usage"></a> Usage in Travis-CI
-------------------------------------------------

To use in `travis-ci`, you must be using at least Ubuntu 14.04 (Trusty) with
`sudo`. Then, add the following `before_deploy` commands:

```
before_deploy:
  - sudo apt-get update -qy
  - sudo apt-get install -qy python3 python3-pip
  - python3 -m pip install packagecore
  - packagecore -o dist "${TRAVIS_TAG#v}"
```

Which will build your packages with the version defined by your tag (assumes
you prefixed it with a `v`), and place the packages in a `dist` directory. Then
add the following to the `deploy` section:

```
deploy:
  ...
  file_glob: true
  file:
    - dist/*
  ...
```

Assuming you name your tags `v1.2.3`


<a name="circle-ci-usage"></a>Usage in Circle-CI
------------------------------------------------

To use in `circle-ci`, add the following to your configuration.

```
machine:
  services:
    - docker
...
deployment:
  package:
    tag: /^v.*$/
    commands:
      - sudo apt-get install python3 python3-pip 
      - sudo python3 -m pip install packagecore
      - packagecore -o "${CIRCLE_ARTIFACTS}" "${CIRCLE_TAG}"
```
