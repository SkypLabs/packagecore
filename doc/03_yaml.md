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

* `metadata` (composite, optional):
  While specifying your package's metadata is optional, failing to do so will
  cause package management system to produce warnings.  

* `commands` (composite, required):
  The commands required to compile and install your program.

* `packages` (composite, required):
  The `packages` statement defines the list of distributions to build packages
  for.


