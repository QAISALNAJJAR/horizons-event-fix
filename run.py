#!/usr/bin/env python3
import sys
import os
import importlib.util

# Load the compiled module
script_dir = os.path.dirname(os.path.abspath(__file__))
pyc_path = os.path.join(script_dir, '__pycache__/main.cpython-*.pyc')

import glob
pyc_files = glob.glob(pyc_path)

if pyc_files:
    # Use the most recent .pyc file
    pyc_file = sorted(pyc_files)[-1]
    spec = importlib.util.spec_from_file_location("main", pyc_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
else:
    print("❌ Compiled module not found!")
    sys.exit(1)
