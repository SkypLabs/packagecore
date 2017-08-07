The packagecore.yaml File
=========================

The configuration file for each project species how to compile, install, and
test your software, as well as an dependencies it needs at both compile and
runtime.


The Fields
----------

* `name` (string, required):

    The name of the package to create. For most distributions this will be
    converted to all lower case.

* `maintainer` (string, optional):

    The name and email address of the package maintainer (e.g.,
    `John Doe <john@doe.org>`). Failing to specify this field will generate
    warnings in most package managers.

* `license` (string, optional):
    
    The name of the license the software included in the package is
    distributed under (e.g., `GPL2`, `MIT`, `Apache 2.0`).  Use `Custom`
    for proprietary and non-standard licenses. Failing to specify this field
    will generate warnings in most package managers.

* `summary` (string, optional):

    A short description of the package. Failing to specify this field
    will generate warnings in most package managers.


* `homepage` (string, optional):

    The home URL of the package.


* `commands` (composite, required):

    The commands required to compile and install your program. If one of your
    commands encounters a fatal error, you should make sure your series of
    commands returns a `1`. You can accomplish this by chaining separate
    commands together with `&&` or by suffixing critical commands with
    `|| exit 1`.

    - `precompile` (string, optional):

        The commands to execute inside of the container before installing build
        dependencies. Most projects will not require `precompile` commands.

    - `compile` (string, optional):

        The commands to execute in order to build the program. These are
        executed after the build dependencies are installed. For many projects
        `compile` commands will be:

        ```
        compile: |
          ./configure --prefix=/usr && make
        ```
        For projects without compiled code, the `compile` statement may be
        omitted.

    - `install` (string, required):

        The commands to execute in order to install the program. Your program
        should be installed in the root directory specified by the
        `${BP_DESTDIR}` environment variable. For many projects, the `install`
        command will simply be:

        ```
        install: |
          make install DESTDIR="${BP_DESTDIR}"
        ```

    - `postinstall` (string, optional):

        The commands the package should execute after it installs on a system.
        Most packages will not need to specify this field. Packages which need
        to add users should do so here. 

        The environment variable
        `${BP_UPGRADE}` is set to `"true"` when the package is being upgraded
        (replacing a previous version), and set to `"false"` when it is a fresh
        installation.

        If your package needs to add the user `specialuser` to the system with
        the `uid` `1234`:

        ```
        [ "${BP_UPGRADE}" == "true" ] || useradd -m "newuser" -u 1234
        ```

    - `testinstall` (string, optional):

        The commands to execute in order to test that the package is correct.
        These commands will be executed after the built package has been
        installed inside of a fresh container. The package itself will also be
        available inside of the container, pointed to by the
        `${BP_PACKAGE_FILE}` variable. You can check to make sure files
        got installed in the correct locations:

        ```
          testinstall: |
            ls /usr/bin/myprog
        ```

        or can execute your program to ensure linking has been done correctly:

        ```
          testinstall: |
            /usr/bin/myprog --version
        ```

* `packages` (composite, required):

    The `packages` statement defines the list of distributions to build packages
    for.

    Each package statement has the following sub statements:

    - `deps` (list, optional):

        A list of the runtime dependencies for the
        package on this distribution.

        ```
        ubuntu16.04:
          deps:
            - libwxgtk3.0-0v5
        ```

    - `builddeps` (list, optional):

        A list of the packages that need to be
        installed in order to compile and build the package.
        Note that the packages listed in `deps` are not installed at build
        time, and thus in many cases must be listed here too.

        ```
        ubuntu16.04:
          builddeps:
            - gcc
            - make
            - libwxgtk3.0-dev
            - libwxgtk3.0-0v5
        ```

    - `commands` (composite, optional):

        Same as the `commands` statement at the top-level. Used to override
        top-level commands for this distribution. For example, on CentOS, when
        building against `libwxgtk3-devel` with `CMake`, you need to specify
        `-DwxWidgets_CONFIG_EXECUTABLE=/usr/bin/wx-config-3` when running
        `CMake`.


