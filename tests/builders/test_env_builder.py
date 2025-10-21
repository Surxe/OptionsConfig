#!/usr/bin/env python3
"""Test script for core.py functionality"""

import sys
from pathlib import Path

# Add src to path for local testing
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from optionsconfig.builders.env_builder import EnvBuilder

# Import the test schema from this directory
from options_schema import OPTIONS_SCHEMA

def test_with_args():
    # Pass the schema directly instead of relying on auto-discovery
    EnvBuilder(OPTIONS_SCHEMA).build()

if __name__ == "__main__":
    test_with_args()
    print("All tests completed!")