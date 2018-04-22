#!/bin/bash

# NOTICE: this script is only running in the Docker container created by "cdrx/docker-pyinstaller"

echo "Install dependencies"
pip install -e .
echo "Build windows executable files"

# pyinstaller doesn't support to use the wildcard in CLI argument `--hidden-import`, 
# I will try to fix this problem in next version

pyinstaller -F ${BUILD_APP_ENTRY} \
            --distpath pyinstaller/dist \
            --specpath pyinstaller/spec \
            --workpath pyinstaller/build \
            --hidden-import="dcdownloader.parser.DmzjParser" \
            --hidden-import="dcdownloader.parser.EhentaiParser"

echo "Rename output file"
mv pyinstaller/dist/main.exe  pyinstaller/dist/${BUILD_OUTPUT_FILE_NAME}