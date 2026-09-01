#!/usr/bin/env python3
"""
Run the compiled Horizons Event Checker
"""

import sys
import os

# Add script directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the compiled module
import main
