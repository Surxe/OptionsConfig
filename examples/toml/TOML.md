# Documentation on this specific example
Example of using `pyproject.toml` to configure schema module and log file path, without directly passing arguments to `ArgumentWriter` and `Options`

First, create a virtual environment with optionsconfig installed.

# Testing the example
```python
cd examples/toml
python run.py --help
python run.py --enable-feature
python build_docs.py
```

# Check its working
* `--help` should list the options in their argument form
* `examples/toml/.env.example` should match `examples/expected_.env.example`
* `examples/toml/README.md` should match `examples/expected_README.md`
* `examples/toml/default.log` should match `examples/toml/expected_default.log`

# Overview
1. `pyproject.toml` specifies `schema_module = "options_schema"` and `log_file = "default.log"`
2. Default values are loaded, setting `enable_feature` to `true`, and `feature_path` to `[blank]`
3. `.env` is loaded, overriding the default values, setting `enable_feature` to `true` and `feature_path` to `path/to/something`
4. Arguments are loaded, overriding the env values if provided
5. Result is stored in `options` object