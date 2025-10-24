from optionsconfig import EnvBuilder, ReadmeBuilder
from options_schema import OPTIONS_SCHEMA

def build_docs() -> None:
    """Build documentation files like .env.example and README.md based on the options schema."""
    EnvBuilder(schema=OPTIONS_SCHEMA, env_example_path=".env.example").build()
    ReadmeBuilder(schema=OPTIONS_SCHEMA, readme_path="README.md").build()

if __name__ == "__main__":
    build_docs()