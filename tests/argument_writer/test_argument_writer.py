#!/usr/bin/env python3
"""
Test suite for ArgumentWriter class

Tests argument generation for various types:
- Boolean arguments (store_true)
- String arguments
- Integer arguments
- Float arguments
- Path arguments
- Literal (choice) arguments
"""

import sys
import unittest
from pathlib import Path
import argparse

# Add paths - src first so optionsconfig imports work, then local for our schemas
src_path = str(Path(__file__).parent.parent.parent / "src")
local_path = str(Path(__file__).parent)
if src_path not in sys.path:
    sys.path.insert(0, src_path)
if local_path not in sys.path:
    sys.path.insert(0, local_path)

from optionsconfig import ArgumentWriter

# Import the test schema from this directory
from argument_writer_schema import OPTIONS_SCHEMA


class TestArgumentWriter(unittest.TestCase):
    """Test cases for ArgumentWriter class."""
    
    def test_initialization(self):
        """Test ArgumentWriter initialization with schema."""
        writer = ArgumentWriter(schema=OPTIONS_SCHEMA)
        self.assertIsNotNone(writer.schema)
        self.assertEqual(len(writer.schema), 7)
    
    def test_boolean_argument(self):
        """Test that boolean arguments are created with store_true action."""
        parser = argparse.ArgumentParser()
        writer = ArgumentWriter(schema=OPTIONS_SCHEMA)
        writer.add_arguments(parser)
        
        # Test without flag
        args = parser.parse_args([])
        self.assertIsNone(args.verbose)
        
        # Test with flag
        args = parser.parse_args(['--verbose'])
        self.assertTrue(args.verbose)
    
    def test_string_argument(self):
        """Test string argument creation."""
        parser = argparse.ArgumentParser()
        writer = ArgumentWriter(schema=OPTIONS_SCHEMA)
        writer.add_arguments(parser)
        
        # Test default
        args = parser.parse_args([])
        self.assertIsNone(args.output_file)
        
        # Test with value
        args = parser.parse_args(['--output-file', 'test.txt'])
        self.assertEqual(args.output_file, 'test.txt')
    
    def test_integer_argument(self):
        """Test integer argument creation."""
        parser = argparse.ArgumentParser()
        writer = ArgumentWriter(schema=OPTIONS_SCHEMA)
        writer.add_arguments(parser)
        
        # Test default
        args = parser.parse_args([])
        self.assertIsNone(args.max_workers)
        
        # Test with value
        args = parser.parse_args(['--max-workers', '8'])
        self.assertEqual(args.max_workers, 8)
        self.assertIsInstance(args.max_workers, int)
    
    def test_float_argument(self):
        """Test float argument creation."""
        parser = argparse.ArgumentParser()
        writer = ArgumentWriter(schema=OPTIONS_SCHEMA)
        writer.add_arguments(parser)
        
        # Test default
        args = parser.parse_args([])
        self.assertIsNone(args.threshold)
        
        # Test with value
        args = parser.parse_args(['--threshold', '0.75'])
        self.assertEqual(args.threshold, 0.75)
        self.assertIsInstance(args.threshold, float)
    
    def test_path_argument(self):
        """Test Path argument creation (handled as string)."""
        parser = argparse.ArgumentParser()
        writer = ArgumentWriter(schema=OPTIONS_SCHEMA)
        writer.add_arguments(parser)
        
        # Test default
        args = parser.parse_args([])
        self.assertIsNone(args.data_dir)
        
        # Test with value
        args = parser.parse_args(['--data-dir', '/path/to/data'])
        self.assertEqual(args.data_dir, '/path/to/data')
        self.assertIsInstance(args.data_dir, str)
    
    def test_literal_argument(self):
        """Test Literal (choice) argument creation."""
        parser = argparse.ArgumentParser()
        writer = ArgumentWriter(schema=OPTIONS_SCHEMA)
        writer.add_arguments(parser)
        
        # Test default
        args = parser.parse_args([])
        self.assertIsNone(args.log_level)
        
        # Test with valid choice
        args = parser.parse_args(['--log-level', 'DEBUG'])
        self.assertEqual(args.log_level, 'DEBUG')
        
        # Test invalid choice should raise error
        with self.assertRaises(SystemExit):
            parser.parse_args(['--log-level', 'INVALID'])
    
    def test_all_arguments_together(self):
        """Test parsing multiple arguments together."""
        parser = argparse.ArgumentParser()
        writer = ArgumentWriter(schema=OPTIONS_SCHEMA)
        writer.add_arguments(parser)
        
        # Parse multiple arguments
        args = parser.parse_args([
            '--verbose',
            '--output-file', 'results.txt',
            '--max-workers', '12',
            '--threshold', '0.8',
            '--data-dir', '/data',
            '--log-level', 'WARNING'
        ])
        
        self.assertTrue(args.verbose)
        self.assertEqual(args.output_file, 'results.txt')
        self.assertEqual(args.max_workers, 12)
        self.assertEqual(args.threshold, 0.8)
        self.assertEqual(args.data_dir, '/data')
        self.assertEqual(args.log_level, 'WARNING')
    
    def test_help_text(self):
        """Test that help text is generated correctly."""
        parser = argparse.ArgumentParser()
        writer = ArgumentWriter(schema=OPTIONS_SCHEMA)
        writer.add_arguments(parser)
        
        # Get the actions from the parser
        actions = {action.dest: action for action in parser._actions if action.dest != 'help'}
        
        # Check that help text includes default values
        verbose_action = actions['verbose']
        self.assertIn('(default: False)', verbose_action.help)
        
        output_file_action = actions['output_file']
        self.assertIn('(default: output.txt)', output_file_action.help)
        
        max_workers_action = actions['max_workers']
        self.assertIn('(default: 4)', max_workers_action.help)
    
    def test_reinitialization(self):
        """Test creating multiple ArgumentWriter instances."""
        # Create first instance
        writer1 = ArgumentWriter(schema=OPTIONS_SCHEMA)
        parser1 = argparse.ArgumentParser()
        writer1.add_arguments(parser1)
        
        # Create second instance
        writer2 = ArgumentWriter(schema=OPTIONS_SCHEMA)
        parser2 = argparse.ArgumentParser()
        writer2.add_arguments(parser2)
        
        # Both should work independently
        args1 = parser1.parse_args(['--verbose'])
        args2 = parser2.parse_args(['--max-workers', '16'])
        
        self.assertTrue(args1.verbose)
        self.assertEqual(args2.max_workers, 16)


if __name__ == "__main__":
    unittest.main()
