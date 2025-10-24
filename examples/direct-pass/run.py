from optionsconfig import init_options, ArgumentWriter
from options_schema import OPTIONS_SCHEMA
import argparse
example_args = ['--enable-feature', '--feature-path', '/path/to/something']
arg_parser = argparse.ArgumentParser()
arg_writer = ArgumentWriter(schema=OPTIONS_SCHEMA)
arg_writer.add_arguments(parser=arg_parser)
args=arg_parser.parse_args(example_args) # can use `python example/run.py --arg1 value1 --arg2 value2 etc.` then remove example_args here
global logger
options = init_options(args=args, schema=OPTIONS_SCHEMA, log_file="default.log")
from optionsconfig import logger