from optionsconfig import EnvBuilder, ReadmeBuilder

def build_docs() -> None:
    """Build documentation files like .env.example and README.md based on the options schema."""
    # Schema will be loaded from pyproject.toml automatically
    EnvBuilder().build()
    ReadmeBuilder().build()

if __name__ == "__main__":
    build_docs()
