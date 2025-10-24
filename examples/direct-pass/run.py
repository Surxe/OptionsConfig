from optionsconfig import init_options, ArgumentWriter, setup_logging
from options_schema import OPTIONS_SCHEMA
import argparse
global logger
from optionsconfig import logger

# Setup logging first
setup_logging(log_file="default.log", log_level="DEBUG")

# Now that logging is configured, add arguments and parse
arg_parser = argparse.ArgumentParser()
arg_writer = ArgumentWriter(schema=OPTIONS_SCHEMA)
arg_writer.add_arguments(parser=arg_parser)
args=arg_parser.parse_args()

# Initialize options without setting up logging again
options = init_options(args=args, schema=OPTIONS_SCHEMA, log_file="default.log", setup_logger=False)

logger.debug(f"Example Retrieval of enable_feature: {options.enable_feature}")
logger.debug(f"Example Retrieval of feature_path: {options.feature_path}")