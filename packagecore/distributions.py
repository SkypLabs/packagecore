##
# @file distributions.py
# @brief List of configurations for different distributions.
# @author Dominique LaSalle <dominique@bytepackager.com>
# Copyright 2017, Solid Lake LLC
# @version 1
# @date 2017-07-08


# TODO: this should be editable and expandable by users in the future.

DATA = {
  "archlinux": {
    "dockerImage": "packagecore/archlinux:latest",
    "packageType": "pkgbuild"
  },
  "centos6.9": {
    "dockerImage": "centos:6.9",
    "packageType": "rpm-yum",
    # centos 6 doesn't generate a 'centos' as part of the arch
    "formatString": "%s-%s-%d.el6.x86_64.rpm"
  },
  "centos7.0": {
    "dockerImage": "centos:7.0.1406",
    "packageType": "rpm-yum",
    "formatString": "%s-%s-%d.el7.centos.x86_64.rpm"
  },
  "centos7.1": {
    "dockerImage": "centos:7.1.1503",
    "packageType": "rpm-yum",
    "formatString": "%s-%s-%d.el7.centos.x86_64.rpm"
  },
  "centos7.2": {
    "dockerImage": "centos:7.2.1511",
    "packageType": "rpm-yum",
    "formatString": "%s-%s-%d.el7.centos.x86_64.rpm"
  },
  "centos7.3": {
    "dockerImage": "centos:7.3.1611",
    "packageType": "rpm-yum",
    "formatString": "%s-%s-%d.el7.centos.x86_64.rpm"
  },
  "debian9": {
    "dockerImage": "debian:stretch",
    "packageType": "debian",
  },
  "debian8": {
    "dockerImage": "debian:jessie",
    "packageType": "debian",
  },
  "fedora22": {
    "dockerImage": "fedora:22",
    "packageType": "rpm",
    "formatString": "%s-%s-%d.fc22.x86_64.rpm"
  },
  "fedora23": {
    "dockerImage": "fedora:23",
    "packageType": "rpm",
    "formatString": "%s-%s-%d.fc23.x86_64.rpm"
  },
  "fedora24": {
    "dockerImage": "fedora:24",
    "packageType": "rpm",
    "formatString": "%s-%s-%d.fc24.x86_64.rpm"
  },
  "fedora25": {
    "dockerImage": "fedora:25",
    "packageType": "rpm",
    "formatString": "%s-%s-%d.fc25.x86_64.rpm"
  },
  "ubuntu14.04": {
    "dockerImage": "ubuntu:14.04",
    "packageType": "debian"
  },
  "ubuntu16.04": {
    "dockerImage": "ubuntu:16.04",
    "packageType": "debian"
  },
  "ubuntu16.10": {
    "dockerImage": "ubuntu:16.10",
    "packageType": "debian"
  },
  "ubuntu17.04": {
    "dockerImage": "ubuntu:17.04",
    "packageType": "debian"
  },
  "ubuntu17.10": {
    "dockerImage": "ubuntu:17.10",
    "packageType": "debian"
  }
}
