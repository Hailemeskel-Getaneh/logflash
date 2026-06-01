# logflash

A modular **Static Application Security Testing (SAST)** engine for rapid local security auditing.

## Installation

```bash
pip install logflash
```

## Usage

```bash
logflash /path/to/your/project
```

The tool will:
1. Traverse the project (ignoring heavy folders like `node_modules` and `venv`).
2. Scan supported files (`.py`, `.js`, `.java`, `.cpp`, `.php`, …) for common vulnerabilities.
3. Output a nicely formatted, severity‑sorted console report.
4. Export findings to `security_audit_report.json`.

### Mock Sandbox

Run the tool without arguments to see a demo sandbox:

```bash
logflash
```

It creates a temporary sandbox with vulnerable files and scans them.

## Extensibility

- **Rule system** – rules live in `logflash/rules/` as JSON or YAML. They can be overridden or added without touching the source code.
- **Parser plug‑ins** – add a new parser under `src/logflash/parsers/` and register it in `src/logflash/parsers/__init__.py`.

## Documentation

- Full rule schema: `docs/rules.md`
- Usage guide and contribution instructions are in the `docs/` folder.

## Build the package locally

```bash
# Ensure build tools are up‑to‑date
python -m pip install --upgrade build twine

# Build the source and wheel distributions
python -m build
```

The resulting files appear in the `dist/` directory:
- `logflash‑<version>.tar.gz` (source archive)
- `logflash‑<version>-py3-none-any.whl` (wheel)

To verify that the rule files are included:
```bash
python -m zipfile -l dist/logflash-*.whl | grep "rules/"
```
You should see entries such as `logflash/rules/default_rules.json`.

## Publish to PyPI (once version is bumped)

```bash
# Bump version in pyproject.toml (e.g. 0.2.0)
python -m pip install --upgrade twine
python -m twine upload dist/*
```

## CI workflow (GitHub Actions)

The CI runs on Python 3.9 and 3.11, installs the test extra (`pip install -e .[test]`), executes `pytest -q`, and builds the package.

**Note:** The workflow uses `actions/checkout@v3` and `actions/setup-python@v4`. They will automatically migrate to Node.js 24 in June 2026, so no changes are required now.

## Contributing

1. Fork the repo and create a branch.
2. Run the test suite locally: `pytest -q`.
3. Add or update tests for new parsers/rules.
4. Open a Pull Request with a clear description.

## License

MIT License – feel free to use this in commercial or open‑source projects.

---

*Feel free to ⭐ the repository if you find it useful!*
