"""
ArgumentWriter class for generating command line arguments from OPTIONS_SCHEMA
"""

from argparse import ArgumentParser
from typing import Literal, get_origin, get_args
from pathlib import Path
from loguru import logger

from .schema import get_schema


class ArgumentWriter:
    """
    Helper class to write command line arguments based on OPTIONS_SCHEMA
    """

    def __init__(self, schema: dict | None = None):
        self.schema = get_schema(schema=schema)

    def add_arguments(self, parser: ArgumentParser):
        for option_name, details in self.schema.items():
            arg_name = details["arg"]
            arg_type = details["type"]
            default = details["default"]
            help_text = details.get("help", "") + f" (default: {default})"
            
            if arg_type == bool:
                parser.add_argument(arg_name, action='store_true', default=None, help=help_text)
                logger.debug(f"Added boolean argument {arg_name} with action 'store_true'")
            elif get_origin(arg_type) is Literal:
                # Handle Literal types by extracting the choices
                choices = list(get_args(arg_type))
                parser.add_argument(arg_name, choices=choices, default=None, help=help_text)
                logger.debug(f"Added choice argument {arg_name} with choices {choices} and default {default}")
            elif arg_type == Path:
                # Handle Path types
                parser.add_argument(arg_name, type=str, default=None, help=help_text)
                logger.debug(f"Added path argument {arg_name} with default {default}")
            else:
                parser.add_argument(arg_name, type=arg_type, default=None, help=help_text)
                logger.debug(f"Added argument {arg_name} with type {arg_type} and default {default}")
