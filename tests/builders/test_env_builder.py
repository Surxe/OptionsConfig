#!/usr/bin/env python3
"""Test script for core.py functionality"""

import sys
from pathlib import Path

# Add src to path for local testing
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from optionsconfig.core import get_schema
import argparse
from optionsconfig.builders.env_builder import EnvBuilder

def test_with_args():
    schema = get_schema()
    env_builder = EnvBuilder(schema)

if __name__ == "__main__":
    test_with_args()
    print("All tests completed!")