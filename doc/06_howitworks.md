How PackageCore Works
=====================

PackageCore works by using Docker to create a container for each distribution a
package is being built for. 


Package Creation
----------------
PackageCore generate the required package files (e.g., .`spec`, `DEBIAN/control`,
`PKGBUILD`, etc.) based on the information in `packagecore.yaml`.

Then, the native package creation tools for each distribution are used to
generate the packages, which mean the build process differs slightly depending
on the distribution being built for.

The basic stages of package creation are as follows:

1. Execute `precompile` commands in the container.

2. Install `builddeps` in the container.

3. Execute `compile` commands in the container.

4. Execute `install` commands in the container to create an installation under
the `${BP_DESTDIR}` directory.

5. Generate the package file.


Package Testing
---------------

The built packages are then installed on a fresh Docker container to ensure the
package is usable. Users of PackageCore should also specify `testinstall`
commands to ensure their binaries are in working order on each distribution.
