#!/usr/bin/env python3
"""Simple test for build_all.py"""

import sys
import unittest
from pathlib import Path
import os

# Add paths
src_path = str(Path(__file__).parent.parent.parent.parent / "src")
local_path = str(Path(__file__).parent)
if src_path not in sys.path:
    sys.path.insert(0, src_path)
if local_path not in sys.path:
    sys.path.insert(0, local_path)

from optionsconfig.builders import EnvBuilder, ReadmeBuilder
from integration_schema import OPTIONS_SCHEMA


class TestBuildAll(unittest.TestCase):
    """Test cases for building all documentation."""
    
    def setUp(self):
        """Set up test file paths."""
        self.env_path = Path('tests/builders/integration/test_all.env.example')
        self.readme_path = Path('tests/builders/integration/test_all_README.md')
    
    def test_build_all(self):
        """Test that both builders work together."""
        # Create a test README with markers
        test_readme_content = """# Test README
<!-- BEGIN_GENERATED_OPTIONS -->
<!-- END_GENERATED_OPTIONS -->
"""
        with open(self.readme_path, 'w', encoding='utf-8') as f:
            f.write(test_readme_content)
        
        # Build both
        env_result = EnvBuilder(schema=OPTIONS_SCHEMA, env_example_path=self.env_path).build()
        readme_result = ReadmeBuilder(schema=OPTIONS_SCHEMA, readme_path=self.readme_path).build()
        
        # Verify
        self.assertTrue(env_result and readme_result, "One or both builders failed")
        self.assertTrue(self.env_path.exists() and self.readme_path.exists(), "Files not created")


class TestBuildAllWithToml(unittest.TestCase):
    """Test cases for building all documentation with toml configuration."""
    
    def setUp(self):
        """Set up test environment and save current directory."""
        self.test_dir = Path(__file__).parent
        self.original_cwd = os.getcwd()
        
        # Ensure the test directory has pyproject.toml
        self.toml_path = self.test_dir / 'pyproject.toml'
        self.assertTrue(self.toml_path.exists(), 
                       "pyproject.toml must exist in test directory")
        
        # Set up relative paths from test directory
        self.env_path = Path('test_all_toml.env.example')
        self.readme_path = Path('test_all_toml_README.md')
    
    def tearDown(self):
        """Restore original directory and clean up test files."""
        os.chdir(self.original_cwd)
        
        # Clean up test files
        for path in [self.test_dir / self.env_path, self.test_dir / self.readme_path]:
            if path.exists():
                path.unlink()
    
    def test_build_all_from_toml(self):
        """Test that both builders work together with toml-loaded schema."""
        os.chdir(self.test_dir)
        sys.path.insert(0, str(self.test_dir))
        
        try:
            # Create a test README with markers
            test_readme_content = """# Test README
<!-- BEGIN_GENERATED_OPTIONS -->
<!-- END_GENERATED_OPTIONS -->
"""
            with open(self.readme_path, 'w', encoding='utf-8') as f:
                f.write(test_readme_content)
            
            # Build both without explicit schema (should load from toml)
            env_builder = EnvBuilder(env_example_path=self.env_path)
            readme_builder = ReadmeBuilder(readme_path=self.readme_path)
            
            env_result = env_builder.build()
            readme_result = readme_builder.build()
            
            # Verify
            self.assertTrue(env_result and readme_result, "One or both builders failed")
            self.assertTrue(self.env_path.exists() and self.readme_path.exists(), "Files not created")
            
            # Verify content contains schema elements
            with open(self.env_path, 'r', encoding='utf-8') as f:
                env_content = f.read()
                self.assertIn('SHOULD_PARSE', env_content)
                self.assertIn('GAME_TO_PARSE', env_content)
            
            with open(self.readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
                self.assertIn('**SHOULD_PARSE**', readme_content)
                self.assertIn('**GAME_TO_PARSE**', readme_content)
                
        finally:
            if str(self.test_dir) in sys.path:
                sys.path.remove(str(self.test_dir))
    
    def test_build_all_with_default_toml_paths(self):
        """Test builders using default paths from pyproject.toml."""
        os.chdir(self.test_dir)
        sys.path.insert(0, str(self.test_dir))
        
        try:
            # Use default paths from toml
            default_env = Path('test_toml.env.example')
            default_readme = Path('test_toml_README.md')
            
            # Create README with markers
            test_readme_content = """# Default TOML README
<!-- BEGIN_GENERATED_OPTIONS -->
<!-- END_GENERATED_OPTIONS -->
"""
            with open(default_readme, 'w', encoding='utf-8') as f:
                f.write(test_readme_content)
            
            # Create builders with no parameters (fully from toml)
            env_builder = EnvBuilder()
            readme_builder = ReadmeBuilder()
            
            # Build
            env_result = env_builder.build()
            readme_result = readme_builder.build()
            
            # Verify
            self.assertTrue(env_result and readme_result, "Builders with default toml paths failed")
            self.assertTrue(default_env.exists() and default_readme.exists(), "Default files not created")
            
            # Clean up
            if default_env.exists():
                default_env.unlink()
            if default_readme.exists():
                default_readme.unlink()
                
        finally:
            if str(self.test_dir) in sys.path:
                sys.path.remove(str(self.test_dir))
    
    def test_mixed_toml_and_direct_params(self):
        """Test mixing toml schema with direct path parameters."""
        os.chdir(self.test_dir)
        sys.path.insert(0, str(self.test_dir))
        
        try:
            # Use custom paths but toml schema
            mixed_env = Path('test_mixed.env.example')
            mixed_readme = Path('test_mixed_README.md')
            
            # Create README with markers
            test_readme_content = """# Mixed Config README
<!-- BEGIN_GENERATED_OPTIONS -->
<!-- END_GENERATED_OPTIONS -->
"""
            with open(mixed_readme, 'w', encoding='utf-8') as f:
                f.write(test_readme_content)
            
            # Create builders: schema from toml, paths direct
            env_builder = EnvBuilder(env_example_path=mixed_env)
            readme_builder = ReadmeBuilder(readme_path=mixed_readme)
            
            # Build
            env_result = env_builder.build()
            readme_result = readme_builder.build()
            
            # Verify
            self.assertTrue(env_result and readme_result, "Mixed config builders failed")
            self.assertTrue(mixed_env.exists() and mixed_readme.exists(), "Mixed files not created")
            
            # Verify schema from toml was used
            with open(mixed_env, 'r', encoding='utf-8') as f:
                env_content = f.read()
                self.assertIn('SHOULD_PARSE', env_content, "TOML schema not used")
            
            # Clean up
            if mixed_env.exists():
                mixed_env.unlink()
            if mixed_readme.exists():
                mixed_readme.unlink()
                
        finally:
            if str(self.test_dir) in sys.path:
                sys.path.remove(str(self.test_dir))


if __name__ == "__main__":
    unittest.main()