# Documentation on this specific example
Example of directly passing all arguments to `ArgumentWriter` and `Options`

# Testing the example
```python
cd examples/direct-pass
python run.py --help
python run.py --enable-feature
python build_docs.py
```

# Check its working
* `--help` should list the options in their argument form
* `examples/direct-pass/.env.example` should match `examples/expected_.env.example`
* `examples/direct-pass/README.md` should match `examples/expected_README.md`
* `examples/direct-pass/default.log` should match `examples/direct-pass/expected_default.log`

# Overview
1. Default values are loaded, setting `enable_feature` to `true`, and `feature_path` to `[blank]`
1. `.env` is loaded, overriding the default values, setting `enable_feature` to `false` and `feature_path` to `path/to/something`
2. arguments are loaded, overriding the env values, setting `enable_feature` to `true`
3. Result is `enable_feature=true`, `feature_path=path/to/something` stored in `options`