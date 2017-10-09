Integrating with a CI/CD service
================================

PackageCore was designed for use both locally, and in remote build services.
Below are instructions on how to setup both [Travis-CI](#travis-ci-usage) and 
[Circle-CI](#circle-ci-usage) with PackageCore.


<a name="travis-ci-usage"></a> Usage in Travis-CI
-------------------------------------------------

To use in `travis-ci`, you must be using at least Ubuntu 14.04 (Trusty) with
`docker` and `sudo`. 

```
sudo: required
services:
  - docker
```

Then, add the following `before_deploy` commands:

```
before_deploy:
  - sudo apt-get update -qy
  - sudo apt-get install -qy python3 python3-pip libyaml-dev
  - sudo python3 -m pip install packagecore
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
  on:
    tags: true
  ...
```

If you want to upload your packages to your GitHub release page, follow the
[Travis-CI](https://docs.travis-ci.com/user/deployment/releases/) instructions
for how to fill out the rest of the deploy section.



<a name="circle-ci-usage"></a>Usage in Circle-CI
------------------------------------------------

To use in `circle-ci`, add the following to your configuration `circle.yaml`
file (assuming version 1).

```
machine:
  services:
    - docker
...
deployment:
  package:
    tag: /^v.*$/
    commands:
      - sudo apt-get update -qy
      - sudo apt-get install -qy python3 python3-pip libyaml-dev
      - sudo python3 -m pip install packagecore
      - packagecore -o "${CIRCLE_ARTIFACTS}" "${CIRCLE_TAG#v}"
```

The above assumes that you prefix your version tags with a `v` (e.g.,
`v1.2.3`).
