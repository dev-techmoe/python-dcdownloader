#!/bin/bash

DOCKER_IMAGE="cdrx/pyinstaller-windows:python3-32bit"

chmod +x ./devscript/*.sh

echo "TRAVIS_BUILD_NUMBER=${TRAVIS_BUILD_NUMBER}"
echo "BUILD_APP_ENTRY=${BUILD_APP_ENTRY}"
echo "BUILD_OUTPUT_FILE_NAME=${BUILD_OUTPUT_FILE_NAME}"
echo "DOCKER_IMAGE=${DOCKER_IMAGE}"

# pull the docker images and create the container for build
docker pull ${DOCKER_IMAGE}
docker run -v "$(pwd):/src/" \
        -e "TRAVIS_BUILD_NUMBER=${TRAVIS_BUILD_NUMBER}" \
        -e "BUILD_APP_ENTRY=${BUILD_APP_ENTRY}" \
        -e "BUILD_OUTPUT_FILE_NAME=${BUILD_OUTPUT_FILE_NAME}" \
        ${DOCKER_IMAGE} "chmod +x devscript/build_pyinstaller_windows.sh && devscript/build_pyinstaller_windows.sh"