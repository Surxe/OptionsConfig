#!/usr/bin/env python3
"""Test script for core.py functionality"""

import sys
from pathlib import Path

# Add src to path for local testing
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from optionsconfig.core import Options, ArgumentWriter, init_options
import argparse

def test_basic_options():
    print("=" * 60)
    print("Test 1: Basic Options (no args)")
    print("=" * 60)
    options = Options()
    print()

def test_with_args():
    print("=" * 60)
    print("Test 2: Options with CLI args")
    print("=" * 60)
    parser = argparse.ArgumentParser()
    writer = ArgumentWriter()
    writer.add_arguments(parser)
    
    # Simulate command line args
    args = parser.parse_args(['--should-parse', '--game-to-parse', 'TestGame'])
    options = Options(args)
    print()

def test_init_options():
    print("=" * 60)
    print("Test 3: Using init_options()")
    print("=" * 60)
    options = init_options()
    print(f"Options initialized: {type(options)}")
    print()

if __name__ == "__main__":
    test_basic_options()
    test_with_args()
    test_init_options()
    print("All tests completed!")