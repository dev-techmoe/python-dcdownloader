#!/bin/bash

echo "Launch Web Test Server"
pip install flask
python3 -m test.testserver.server &

pip install .
pytest test