#!/usr/bin/python3
##
# @file main.py
# @brief The main function.
# @author Dominique LaSalle <dominique@bytepackager.com>
# Copyright 2017, Solid Lake LLC
# @version 1
# @date 2017-07-03


import sys
import optparse


from .configfile import YAMLConfigFile
from .packager import Packager
from .distributions import DATA


def showDistributions():
  print("Available distributions to use as targets in the 'packages' section:")
  for distname, data in DATA.items():
    print("\t%s" % distname)


def main():
  # defaults
  release=1
  configFilename="packagecore.yaml"
  outputdir="./"

  usage = "usage: %prog [options] <version> [<release number>]"
  parser = optparse.OptionParser(usage=usage)

  parser.add_option("-c", "--config", dest="configfile", \
      metavar="<yaml file>", \
      default=configFilename, help="The path to the yaml configuration " \
      "file. Defaults to %default.")

  parser.add_option("-o", "--outputdir", dest="outputdir", \
      metavar="<output directory>", default=outputdir, \
      help="The directory to " \
      "put generated packages into. If the directory does not exist, it " \
      "will be created. Defaults to %default.")

  parser.add_option("-d", "--distributions", action="store_true", \
      dest="showdistributions", help="Show a list of available Linux " \
      "distributions to use as targets in the 'packages' section.")

  (options, args) = parser.parse_args()

  if not options.showdistributions is None:
    showDistributions()
    return 0
  else:
    if len(args) == 0:
      print("Must supply a version string." ,file=sys.stderr)
      parser.print_help(file=sys.stderr)
      return -1
    elif len(args) > 2:
      print("Too many arguments.", file=sys.stderr)
      parser.print_help(file=sys.stderr)
      return -1

    version=args[0]
    if len(args) == 2:
      release=int(args[1])
    print("Building version '%s' release '%d'." % (version, release))

    conf = YAMLConfigFile(options.configfile)
    print("Parse '%s' configuration." % configFilename)

    p = Packager(conf=conf.getData(), outputDir=options.outputdir, \
        version=version, release=release)
    if p.run():
      return 0
    else:
      return 1


if __name__ == "__main__":
  ret = main()
  sys.exit(ret)
