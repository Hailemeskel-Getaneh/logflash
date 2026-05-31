# logflash

A Modular Static Application Security Testing (SAST) Engine for rapid local security auditing.

## Installation

You can install `logflash` directly from PyPI:

```bash
pip install logflash
```

## Usage

Simply run `logflash` against any project directory or file:

```bash
logflash /path/to/your/project
```

The tool will automatically:
1. Traverse your project (ignoring heavy dependency folders like `node_modules` and `venv`).
2. Scan supported files (`.py`, `.js`, `.java`, `.cpp`, `.php`, etc.) for vulnerabilities like SQL Injection, Buffer Overflows, XSS, and Hardcoded Secrets.
3. Output a beautiful, severity-sorted console report.
4. Export the findings to a `security_audit_report.json` file.

### Mock Sandbox

If you want to see how the tool works without scanning your own code, run it with no arguments:

```bash
logflash
```

It will automatically generate a mock sandbox directory containing vulnerable files and scan it to demonstrate its capabilities.
