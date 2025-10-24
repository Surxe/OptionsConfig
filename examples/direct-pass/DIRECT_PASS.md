# Documentation on this specific example
Example of directly passing all arguments to `ArgumentWriter` and `Options`

# Testing the example
```python
cd examples/direct-pass
python run.py --help
python run.py --enable-feature --feature-path path/to/something
python build_docs.py
```

# Check its working
* `--help` should list the options in their argument form
* `.env.example` should match `expected_.env.example`
* `README.md` should match `expected_README.md`
* `default.log` should match `expected_default.log`