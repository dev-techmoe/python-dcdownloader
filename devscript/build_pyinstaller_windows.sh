#!/bin/bash

# NOTICE: this script is only running in the Docker container created by "cdrx/docker-pyinstaller"

echo "Install dependencies"
pip install -e .
echo "Build windows executable files"
pyinstaller -F ${BUILD_APP_ENTRY} --distpath pyinstaller/dist --specpath pyinstaller/spec --workpath pyinstaller/build
echo "Rename output file"
mv pyinstaller/dist/main.exe  pyinstaller/dist/${BUILD_OUTPUT_FILE_NAME}