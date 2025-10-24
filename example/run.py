from optionsconfig import init_options, ArgumentWriter
from options_schema import OPTIONS_SCHEMA
import argparse

arg_parser = argparse.ArgumentParser()
arg_writer = ArgumentWriter(schema=OPTIONS_SCHEMA)
arg_writer.add_arguments(parser=arg_parser)
args=arg_parser.parse_args()
global logger
options = init_options(args=args, schema=OPTIONS_SCHEMA, log_file="default.log")
from optionsconfig import logger