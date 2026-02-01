from optionsconfig import init_options, ArgumentWriter, setup_logging
import argparse
from optionsconfig import logger

# Optionally setup logging first (will read log_file from pyproject.toml), to start logging as soon as possible, even before log_level option is set
setup_logging(log_level="DEBUG")

# Now that logging is configured, add arguments and parse
# Schema will be loaded from pyproject.toml automatically
arg_parser = argparse.ArgumentParser()
arg_writer = ArgumentWriter()  # No schema parameter - loads from pyproject.toml
arg_writer.add_arguments(parser=arg_parser)
args=arg_parser.parse_args()

# Initialize options without setting up logging again
# Schema will be loaded from pyproject.toml automatically
options = init_options(args=args, setup_logger=True)

# Replace logging level with option value
print(f"Changing log level to: {options.log_level}")
setup_logging(log_level=options.log_level)

# Utilize options in your application
logger.debug(f"Example Retrieval of enable_feature: {options.enable_feature}")
logger.debug(f"Example Retrieval of feature_path: {options.feature_path}")

# Test log level statements
logger.debug("This is a DEBUG level message - detailed information for debugging")
logger.info("This is an INFO level message - general information about application progress")
logger.warning("This is a WARNING level message - something unexpected but not fatal")
logger.error("This is an ERROR level message - something went wrong")
logger.critical("This is a CRITICAL level message - serious error occurred")
