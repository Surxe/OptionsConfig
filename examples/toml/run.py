from optionsconfig import init_options, ArgumentWriter, setup_logging
import argparse
from optionsconfig import logger

# Setup logging first (will read log_file from pyproject.toml), such that the logs for arg writer will be captured
setup_logging(log_level="DEBUG")

# Now that logging is configured, add arguments and parse
# Schema will be loaded from pyproject.toml automatically
arg_parser = argparse.ArgumentParser()
arg_writer = ArgumentWriter()  # No schema parameter - loads from pyproject.toml
arg_writer.add_arguments(parser=arg_parser)
args=arg_parser.parse_args()

# Initialize options without setting up logging again
# Schema will be loaded from pyproject.toml automatically
options = init_options(args=args, setup_logger=False)

# Utilize options in your application
logger.debug(f"Example Retrieval of enable_feature: {options.enable_feature}")
logger.debug(f"Example Retrieval of feature_path: {options.feature_path}")
