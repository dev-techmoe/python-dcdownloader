#!/bin/bash

apt install tree
echo "Install dependencies"
pip install -e .
echo "Build windows executable files"
pyinstaller -F dcdownloader/main.py --distpath pyinstaller/dist --specpath pyinstaller/spec --workpath pyinstaller/build
tree
echo "Rename output file"
mv pyinstaller/dist/main.exe  pyinstaller/dist/dcdownloader_windows_build${TRAVIS_BUILD_NUMBER}.exe