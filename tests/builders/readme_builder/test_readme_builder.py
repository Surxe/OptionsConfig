#!/usr/bin/env python3
"""Test script for ReadmeBuilder functionality"""

import sys
import unittest
import os
from pathlib import Path

# Add paths
src_path = str(Path(__file__).parent.parent.parent.parent / "src")
local_path = str(Path(__file__).parent)
if src_path not in sys.path:
    sys.path.insert(0, src_path)
if local_path not in sys.path:
    sys.path.insert(0, local_path)

from optionsconfig.builders.readme_builder import ReadmeBuilder
from readme_builder_schema import OPTIONS_SCHEMA


class TestReadmeBuilder(unittest.TestCase):
    """Test cases for ReadmeBuilder with direct parameters."""
    
    def setUp(self):
        """Set up test file path."""
        self.test_dir = Path(__file__).parent
        self.readme_path = self.test_dir / 'TEST_README.md'
    
    def tearDown(self):
        """Clean up test files."""
        if self.readme_path.exists():
            self.readme_path.unlink()
    
    def test_build_readme(self):
        """Test that ReadmeBuilder generates correct README content."""
        # Copy mock README with markers
        import shutil
        mock_readme_src = self.test_dir / 'MOCK_README_WITH_MARKERS.md'
        shutil.copy(mock_readme_src, self.readme_path)
        
        # Pass the schema directly and build
        ReadmeBuilder(schema=OPTIONS_SCHEMA, readme_path=self.readme_path).build()
        
        # Read generated README
        with open(self.readme_path, 'r', encoding='utf-8') as f:
            genned_content = f.read()
        
        # Check that markers are present
        self.assertIn("<!-- BEGIN_GENERATED_OPTIONS -->", genned_content, "Start marker not found")
        self.assertIn("<!-- END_GENERATED_OPTIONS -->", genned_content, "End marker not found")
        
        # Check that options are documented
        self.assertIn("**SHOULD_PARSE**", genned_content, "SHOULD_PARSE option not found")
        self.assertIn("**GAME_TO_PARSE**", genned_content, "GAME_TO_PARSE option not found")
        self.assertIn("#### Parse", genned_content, "Parse section not found")
        
        # Check that old content was replaced
        self.assertNotIn("Old content to be replaced", genned_content, "Old content was not replaced")
        
        # Check that surrounding content is preserved
        self.assertIn("Some content here.", genned_content, "Content before markers was lost")
        self.assertIn("More content after.", genned_content, "Content after markers was lost")


class TestReadmeBuilderWithToml(unittest.TestCase):
    """Test cases for ReadmeBuilder loading configuration from pyproject.toml."""
    
    def setUp(self):
        """Set up test environment and save current directory."""
        self.test_dir = Path(__file__).parent
        self.original_cwd = os.getcwd()
        
        # Ensure the test directory has pyproject.toml
        self.toml_path = self.test_dir / 'pyproject.toml'
        self.assertTrue(self.toml_path.exists(), 
                       "pyproject.toml must exist in test directory")
    
    def tearDown(self):
        """Restore original directory and clean up test files."""
        os.chdir(self.original_cwd)
        # Clean up generated test files
        readme = self.test_dir / 'TEST_README.md'
        if readme.exists():
            readme.unlink()
    
    def test_build_readme_from_toml(self):
        """Test that ReadmeBuilder loads schema and path from pyproject.toml and generates correct content."""
        # Change to test directory where pyproject.toml is located
        os.chdir(self.test_dir)
        
        # Copy mock README with markers
        import shutil
        readme_path = self.test_dir / 'TEST_README.md'
        mock_readme_src = self.test_dir / 'MOCK_README_WITH_MARKERS.md'
        shutil.copy(mock_readme_src, readme_path)
        
        # Create ReadmeBuilder without passing schema or path - should load both from pyproject.toml
        builder = ReadmeBuilder()
        builder.build()
        
        # Verify file was updated
        self.assertTrue(readme_path.exists(), 
                       "README file was not found")
        
        # Read generated content
        with open(readme_path, 'r', encoding='utf-8') as f:
            genned_content = f.read()
        
        # Check that markers are present
        self.assertIn("<!-- BEGIN_GENERATED_OPTIONS -->", genned_content, "Start marker not found")
        self.assertIn("<!-- END_GENERATED_OPTIONS -->", genned_content, "End marker not found")
        
        # Check that options are documented
        self.assertIn("**SHOULD_PARSE**", genned_content, "SHOULD_PARSE option not found")
        self.assertIn("**GAME_TO_PARSE**", genned_content, "GAME_TO_PARSE option not found")
        self.assertIn("#### Parse", genned_content, "Parse section not found")
        
        # Check that old content was replaced
        self.assertNotIn("Old content to be replaced", genned_content, "Old content was not replaced")
        
        # Check that surrounding content is preserved
        self.assertIn("Some content here.", genned_content, "Content before markers was lost")
        self.assertIn("More content after.", genned_content, "Content after markers was lost")
    
    def test_build_readme_toml_no_path_param(self):
        """Test that ReadmeBuilder raises error when markers are not present."""
        # Create a temp subdirectory without readme_path in config
        temp_dir = self.test_dir / 'temp_test'
        temp_dir.mkdir(exist_ok=True)
        
        # Copy the schema file to temp directory
        import shutil
        schema_src = self.test_dir / 'readme_builder_schema.py'
        schema_dst = temp_dir / 'readme_builder_schema.py'
        shutil.copy(schema_src, schema_dst)
        
        # Create a minimal pyproject.toml with only schema_module and explicit readme_path
        temp_toml = temp_dir / 'pyproject.toml'
        with open(temp_toml, 'w') as f:
            f.write('[tool.optionsconfig]\n')
            f.write('schema_module = "readme_builder_schema"\n')
            f.write('readme_path = "README.md"\n')  # Explicit path in temp dir
        
        # Copy mock README without markers to temp directory
        mock_readme_src = self.test_dir / 'MOCK_README_NO_MARKERS.md'
        default_readme = temp_dir / 'README.md'
        shutil.copy(mock_readme_src, default_readme)
        
        # Save current directory
        original_cwd = os.getcwd()
        
        try:
            # Change to temp directory so ReadmeBuilder finds local pyproject.toml
            os.chdir(temp_dir)
            
            # Create builder - should raise ValueError when markers are missing
            builder = ReadmeBuilder()
            
            with self.assertRaises(ValueError) as context:
                builder.build()
            
            # Verify the error message mentions markers
            self.assertIn('Markers not found', str(context.exception))
            self.assertIn('BEGIN_GENERATED_OPTIONS', str(context.exception))
            self.assertIn('END_GENERATED_OPTIONS', str(context.exception))
        
        finally:
            # Clean up temp directory
            os.chdir(original_cwd)
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
    
    def test_toml_schema_content_matches_direct_param(self):
        """Test that schema loaded from toml produces identical output to direct parameter."""
        os.chdir(self.test_dir)
        
        # Copy mock README with markers for both tests
        import shutil
        mock_readme_src = self.test_dir / 'MOCK_README_WITH_MARKERS.md'
        
        # Build with toml (no parameters at all)
        toml_readme = self.test_dir / 'TEST_README.md'
        shutil.copy(mock_readme_src, toml_readme)
        
        builder_toml = ReadmeBuilder()
        builder_toml.build()
        
        # Build with direct parameter
        direct_readme = self.test_dir / 'TEST_README_DIRECT.md'
        shutil.copy(mock_readme_src, direct_readme)
        
        builder_direct = ReadmeBuilder(schema=OPTIONS_SCHEMA, readme_path=direct_readme)
        builder_direct.build()
        
        try:
            # Read both files
            with open(toml_readme, 'r', encoding='utf-8') as f:
                toml_content = f.read()
            with open(direct_readme, 'r', encoding='utf-8') as f:
                direct_content = f.read()
            
            # Should be identical
            self.assertEqual(toml_content, direct_content,
                           "Output from toml-loaded schema should match direct parameter schema")
        
        finally:
            # Clean up
            if direct_readme.exists():
                direct_readme.unlink()


if __name__ == "__main__":
    unittest.main()
