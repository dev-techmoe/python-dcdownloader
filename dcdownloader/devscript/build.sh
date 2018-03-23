#!/bin/sh

pip install aiohttp
pip install .
pyinstaller -F dcdownloader/main.py --distpath pyinstaller/dist --specpath pyinstaller/spec --workpath pyinstaller/build
mv pyinstaller/dist/main.exe  pyinstaller/dist/dcdownloader_windows.exe