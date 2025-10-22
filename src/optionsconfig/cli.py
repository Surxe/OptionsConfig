#!/usr/bin/env python3
"""
Command-line interface for OptionsConfig

Provides commands to generate documentation and validate schemas.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from .builders.env_builder import EnvBuilder
from .builders.readme_builder import ReadmeBuilder
from .schema import load_schema, validate_schema


def build_env(args: argparse.Namespace) -> int:
    """Generate .env.example file from schema."""
    try:
        print("Building .env.example...")
        builder = EnvBuilder()
        builder.build()
        print("✓ Successfully generated .env.example")
        return 0
    except Exception as e:
        print(f"✗ Error generating .env.example: {e}", file=sys.stderr)
        return 1


def build_readme(args: argparse.Namespace) -> int:
    """Generate README options section from schema."""
    try:
        print("Building README options section...")
        builder = ReadmeBuilder()
        builder.build()
        print("✓ Successfully updated README.md")
        return 0
    except Exception as e:
        print(f"✗ Error updating README.md: {e}", file=sys.stderr)
        return 1


def build_all(args: argparse.Namespace) -> int:
    """Generate all documentation files."""
    print("Building all documentation...\n")
    
    results = []
    
    # Build .env.example
    env_result = build_env(args)
    results.append(env_result)
    print()
    
    # Build README
    readme_result = build_readme(args)
    results.append(readme_result)
    print()
    
    # Summary
    if all(r == 0 for r in results):
        print("✓ All documentation generated successfully!")
        return 0
    else:
        print("✗ Some documentation generation failed")
        return 1


def validate(args: argparse.Namespace) -> int:
    """Validate the OPTIONS_SCHEMA."""
    try:
        print("Validating schema...")
        
        # Load schema
        schema = load_schema()
        
        if not schema:
            print("✗ No schema found", file=sys.stderr)
            return 1
        
        # Validate schema
        errors = validate_schema(schema)
        
        if errors:
            print(f"✗ Schema validation failed with {len(errors)} error(s):", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
            return 1
        
        print(f"✓ Schema is valid ({len(schema)} options)")
        
        # Show summary
        sections = set(details.get("section", "Other") for details in schema.values())
        print(f"  Sections: {', '.join(sorted(sections))}")
        
        return 0
        
    except Exception as e:
        print(f"✗ Error validating schema: {e}", file=sys.stderr)
        return 1


def info(args: argparse.Namespace) -> int:
    """Display information about the current schema."""
    try:
        schema = load_schema()
        
        if not schema:
            print("No schema found")
            return 1
        
        print(f"Schema Information")
        print("=" * 50)
        print(f"Total options: {len(schema)}")
        
        # Group by section
        sections_data = {}
        for option_name, details in schema.items():
            section = details.get("section", "Other")
            if section not in sections_data:
                sections_data[section] = []
            sections_data[section].append(option_name)
        
        print(f"\nSections ({len(sections_data)}):")
        for section, options in sorted(sections_data.items()):
            print(f"  {section}: {len(options)} option(s)")
            if args.verbose:
                for opt in sorted(options):
                    print(f"    - {opt}")
        
        # Count dependent options
        dependent_count = sum(
            1 for details in schema.values()
            if "depends_on" in details
        )
        
        print(f"\nDependencies:")
        print(f"  Root options: {len(schema) - dependent_count}")
        print(f"  Dependent options: {dependent_count}")
        
        # Count sensitive options
        sensitive_count = sum(
            1 for details in schema.values()
            if details.get("sensitive", False)
        )
        
        if sensitive_count > 0:
            print(f"\nSensitive options: {sensitive_count}")
        
        return 0
        
    except Exception as e:
        print(f"Error loading schema: {e}", file=sys.stderr)
        return 1


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="optionsconfig",
        description="OptionsConfig CLI - Generate documentation and validate schemas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  optionsconfig build env      Generate .env.example
  optionsconfig build readme   Update README.md
  optionsconfig build all      Generate all documentation
  optionsconfig validate       Validate your schema
  optionsconfig info           Show schema information
  optionsconfig info -v        Show detailed schema information
        """
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    
    subparsers = parser.add_subparsers(
        title="commands",
        description="Available commands",
        dest="command",
        required=True
    )
    
    # Build command
    build_parser = subparsers.add_parser(
        "build",
        help="Generate documentation files"
    )
    build_subparsers = build_parser.add_subparsers(
        title="build targets",
        description="What to build",
        dest="target",
        required=True
    )
    
    # Build env
    build_subparsers.add_parser(
        "env",
        help="Generate .env.example file"
    )
    
    # Build readme
    build_subparsers.add_parser(
        "readme",
        help="Update README.md with options documentation"
    )
    
    # Build all
    build_subparsers.add_parser(
        "all",
        help="Generate all documentation files"
    )
    
    # Validate command
    subparsers.add_parser(
        "validate",
        help="Validate OPTIONS_SCHEMA"
    )
    
    # Info command
    info_parser = subparsers.add_parser(
        "info",
        help="Display schema information"
    )
    info_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed information"
    )
    
    return parser


def main() -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Route to appropriate handler
    if args.command == "build":
        if args.target == "env":
            return build_env(args)
        elif args.target == "readme":
            return build_readme(args)
        elif args.target == "all":
            return build_all(args)
    elif args.command == "validate":
        return validate(args)
    elif args.command == "info":
        return info(args)
    
    # Should never reach here due to required=True
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
