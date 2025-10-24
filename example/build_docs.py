from optionsconfig import EnvBuilder, ReadmeBuilder

def build_docs() -> None:
    """Build documentation files like .env.example and README.md based on the options schema."""
    EnvBuilder().build()
    ReadmeBuilder().build()

if __name__ == "__main__":
    build_docs()