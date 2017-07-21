PackageCore
===========

PackageCore is a utility for building native Linux packages for multiple
distributions. It aims to make it easy for upstream developers to
release their software for all Linux distributions. 

It works by
spinning up docker containers for each distribution, compiling, packaging, and
testing the package from within the container.

It is designed to work with existing build services, such that creating Linux
packages can be part of your normal work flow.
