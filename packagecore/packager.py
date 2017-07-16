##
# @file packager.py
# @brief The top-level Packager class for orchestrating the package builds.
# @author Dominique LaSalle <dominique@bytepackager.com>
# Copyright 2017, Solid Lake LLC
# @version 1
# @date 2017-07-03

import shutil
import os
import traceback

from .builddata import BuildData
from .docker import Docker
from .pkgbuild import PkgBuild
from .dpkg import DebianPackage
from .rpm import RPM
from .distributions import DATA as BUILDS
from .scriptfile import generateScript 


class UnknownPackageTypeError(Exception):
  pass


class PackageNotFoundError(Exception):
  pass


def _stringifyCommands(cmds):
  if isinstance(cmds, list):
    cmds = "\n".join(cmds)
  elif isinstance(cmds, str):
    pass
  else:
    raise TypeError("Expected commands to be a string or list. Not '%s'." % \
        type(cmds))
  return cmds


class Packager(object):
  ##
  # @brief Create a packager object.
  #
  # @param conf The configuration to use.
  # @param outputDir The directory to output packages into.
  # @param srcDir The directory containing the projects source.
  # @param version The version of packages to generate.
  # @param release The release number.
  # @param distribution The distribution to build a package for.
  #
  # @return The new Packager.
  def __init__(self, conf, srcDir, outputDir, version, release,
      distribution=None):
    self._queue = []
    self._outputDir = outputDir
    self._srcDir = srcDir

    if not os.path.exists(self._outputDir):
      os.makedirs(self._outputDir)

    # set globals
    projectPreCompileCommands = ""
    projectCompileCommands = ""
    projectInstallCommands = "" 
    projectPostInstallCommands = ""
    projectTestInstallCommands = ""
    if "commands" in conf:
      commands = conf["commands"]
      if "precompile" in commands:
        projectPreCompileCommands = _stringifyCommands(commands["precompile"])
      if "compile" in commands:
        projectCompileCommands = _stringifyCommands(commands["compile"])
      if "install" in commands:
        projectInstallCommands = _stringifyCommands(commands["install"])
      if "postinstall" in commands:
        projectPostInstallCommands = \
            _stringifyCommands(commands["postinstall"])
      if "testinstall" in commands:
        projectTestInstallCommands = \
            _stringifyCommands(commands["testinstall"])

    # make sure if we're building a specific distribution it exists in this
    # configuration.
    if not distribution is None and not distribution in conf["packages"]:
      raise PackageNotFoundError("No '%s' listed in configuration." % \
          distribution)

    # parse packages 
    for osName, data in conf["packages"].items():
      if not distribution is None and osName != distribution:
        # skip this package
        print("Skipping '%s'." % osName)
        continue

      # set package specific commnds
      preCompileCommands = projectPreCompileCommands
      compileCommands = projectCompileCommands 
      installCommands = projectInstallCommands 
      postInstallCommands = projectPostInstallCommands 
      testInstallCommands = projectTestInstallCommands 
      if not data is None and "commands" in data:
        commands = data["commands"]
        if "precompile" in commands:
          projectPreCompileCommands = \
              _stringifyCommands(commands["precompile"])
        if "compile" in commands:
          compileCommands = _stringifyCommands(commands["compile"])
        if "install" in commands:
          installCommands = _stringifyCommands(commands["install"])
        if "postinstall" in commands:
          postInstallCommands = _stringifyCommands(commands["postinstall"])
        if "testinstall" in commands:
          testInstallCommands = _stringifyCommands(commands["testinstall"])

      # construct it with the required fields
      b = BuildData(
        name=conf["name"],
        version=version,
        releaseNum=release,
        os=osName,
        preCompileCommands=preCompileCommands,
        compileCommands=compileCommands,
        installCommands=installCommands,
        postInstallCommands=postInstallCommands,
        testInstallCommands=testInstallCommands)

      # set metadata fields
      if "maintainer" in conf:
        b.maintainer = conf["maintainer"]
      if "license" in conf:
        b.license = conf["license"]
      if "homepage" in conf:
        b.homepage = conf["homepage"]
      if "summary" in conf:
        b.summary = conf["summary"]

      # set dependencies 
      if "builddeps" in data:
        b.buildDeps = data["builddeps"]
      if "deps" in data:
        b.runDeps = data["deps"]

      self._queue.append(b)


  ##
  # @brief Build each package.
  #
  # @return None 
  def run(self):
    success = True 
    docker = Docker()
    if len(self._queue) == 0:
      print("No packages to build.")
      success = False
    for job in self._queue:
      build = BUILDS[job.os]
      nameFormat = build["formatString"]
      pkgType = build["packageType"]
      if pkgType == "pkgbuild":
        recipe = PkgBuild(job)
      elif pkgType == "debian":
        recipe = DebianPackage(job)
      elif pkgType == "rpm":
        recipe = RPM(job, useYum=False)
      elif pkgType == "rpm-yum":
        recipe = RPM(job, useYum=True)
      else:
        raise UnknownPackageTypeError("Unknown packaging type: %s" % pkgType) 

      # remove package if it exists
      outfile = os.path.join(self._outputDir, \
          nameFormat.format(name=job.name, version=job.version,
          release=job.releaseNum, arch=recipe.getArch()))
      try:
        print("Building package for %s: %s" % (job.os, str(job)))
        tmpfile = os.path.join("/tmp", recipe.getName())

        # build the package
        container = docker.start(build["dockerImage"])

        print("Using shared directory '%s' and source directory '%s'." %
            (container.getSharedDir(), container.getSourceDir()))

        try:
          # copy in source -- we must be in the source directory
          container.copySource(self._srcDir)

          # run the 'pre' commands in the container
          preCmdFile = os.path.join(container.getSharedDir(), ".preCmds")
          generateScript(preCmdFile, job.preCompileCommands)

          recipe.prep(container)
          recipe.build(container)

          # copy out finished package
          shutil.copy(
              os.path.join(container.getSharedDir(), recipe.getName()), \
              tmpfile)
        finally:
          container.stop()

        # spawn a new docker container
        container = docker.start(build["dockerImage"])
        try:
          # copy in the package for installation
          shutil.copy(tmpfile, container.getSharedDir())
          recipe.install(container)
        finally:
          container.stop()

        # move the package to the current directory
        shutil.move(tmpfile, outfile)
      except:
        print("Failed to build package for '%s'." % job.os)
        print(traceback.format_exc())
        success = False
    return success 
        
        


