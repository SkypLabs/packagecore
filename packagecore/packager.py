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


class UnknownPackageTypeError(Exception):
  pass


class Packager(object):
  ##
  # @brief Create a packager object.
  #
  # @param conf The configuration to use.
  # @param outputDir The directory to output packages into.
  # @param version The version of packages to generate.
  # @param release The release number.
  #
  # @return The new Packager.
  def __init__(self, conf, outputDir, version, release):
    self._queue = []
    self._outputDir = outputDir

    if not os.path.exists(self._outputDir):
      os.makedirs(self._outputDir)

    # set globals
    projectCompileCommands = []
    projectInstallCommands = [] 
    projectPostInstallCommands = []
    projectTestInstallCommands = []
    if "commands" in conf:
      commands = conf["commands"]
      if "compile" in commands:
        projectCompileCommands = commands["compile"]
      if "install" in commands:
        projectInstallCommands = commands["install"]
      if "postInstall" in commands:
        projectPostInstallCommands = commands["postInstall"]
      if "testInstall" in commands:
        projectTestInstallCommands = commands["testInstall"]

    # parse packages 
    for osName, data in conf["packages"].items():
      # set package specific commnds
      compileCommands = projectCompileCommands 
      installCommands = projectInstallCommands 
      postInstallCommands = projectPostInstallCommands 
      testInstallCommands = projectTestInstallCommands 
      if not data is None and "commands" in data:
        commands = data["commands"]
        if "compile" in commands:
          compileCommands = commands["compile"]
        if "install" in commands:
          installCommands = commands["install"]
        if "postInstall" in commands:
          postInstallCommands = commands["postInstall"]
        if "testInstall" in commands:
          testInstallCommands = commands["testInstall"]

      # construct it with the required fields
      b = BuildData(
        name=conf["name"],
        version=version,
        releaseNum=release,
        os=osName,
        compileCommands=compileCommands,
        installCommands=installCommands,
        postInstallCommands=postInstallCommands,
        testInstallCommands=testInstallCommands)

      # set optional fields
      if "maintainer" in conf:
        b.maintainer = conf["maintainer"]
      if "license" in conf:
        b.license = conf["license"]
      if "homepage" in conf:
        b.homepage = conf["homepage"]
      if "summary" in conf:
        b.summary = conf["summary"]
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
      pkgType = build["packageType"]
      if pkgType == "pkgbuild":
        recipe = PkgBuild(job)
      elif pkgType == "debian":
        recipe = DebianPackage(job)
      elif pkgType == "rpm":
        recipe = RPM(job, build["formatString"], useYum=False)
      elif pkgType == "rpm-yum":
        recipe = RPM(job, build["formatString"], useYum=True)
      else:
        raise UnknownPackageTypeError("Unknown packaging type: %s" % pkgType) 

      try:
        print("Building package for %s: %s" % (job.os, str(job)))
        tmpfile = os.path.join("/tmp", recipe.getName())

        # build the package
        container = docker.start(build["dockerImage"])

        print("Using shared directory '%s' and source directory '%s'." %
            (container.getSharedDir(), container.getSourceDir()))

        try:
          # copy in source -- we must be in the source directory
          container.copySource("./")

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
        shutil.move(tmpfile, self._outputDir)
      except:
        print("Failed to build package for '%s'." % job.os)
        print(traceback.format_exc())
        success = False
    return success 
        
        


