#!/bin/bash

failTest() {
  echo "ERROR: $(pwd)/${@} failed."
  R=1
}

failCheck() {
  echo "ERROR: $(pwd)/${@} failed to compile."
  # if we find an error in the file, we should just exit
  exit 1
}


PYLINT_CMD="pylint -E --disable=not-context-manager"


pushd "packagecore"

# run pylint
echo "Checking python files"
for file in *.py; do
  ${PYLINT_CMD} "${file}" && echo "${file} passed." || failCheck "${file}"
done
echo "Finished checking files"

R=0
# run local unit tests
echo "Running unit tests"
for unitTest in *_test.py; do
  /usr/bin/python3 "${unitTest}" && echo "$(pwd)/${unitTest} passed." || \
      failTest "${unitTest}"
done
echo "Finished running unit tests"

popd

exit "${R}"
