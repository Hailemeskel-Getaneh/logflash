
# logflash
**logflash** – a modular, extensible **Static Application Security Testing (SAST)** engine for developers.  
Install it from PyPI with a single command and scan any codebase (Python, JavaScript, PHP, C/C++, Java, …) for high‑impact vulnerabilities such as command injection, hard‑coded secrets, XSS, buffer overflows, and more.
### 🎯 Why logflash?
- **One‑liner installation**: `pip install logflash`
- **Zero‑configuration scanning** – just point it at a folder.
- **Rich rule set** stored as JSON/YAML files that can be **overridden or extended** without touching the source code.
- **Language‑agnostic architecture** – plug in new parsers for any language in minutes.
- **Beautiful console UI** with a live spinner, grouped findings, and a summary dashboard.
- **Exportable reports**: JSON, SARIF (for CI/CD), or a plain‑text console view.
- **Fully open source** – perfect for portfolios, teaching, or integrating into CI pipelines.
---
## 📦 Installation
```bash
# Install the latest release from PyPI
pip install logflash
Tip: Use a virtual environment (python -m venv .venv && .\.venv\Scripts\Activate.ps1) to keep dependencies isolated.

🚀 Quick Start
bash


# Scan a project directory
logflash path/to/your/project
Output (example):



================================================================================
 logflash - Security Audit Report
================================================================================
 EXECUTIVE METRICS SUMMARY
------------------------------
 Total Files Scanned: 27
 TOTAL FINDINGS: 12 | [CRITICAL]: 0 | [HIGH]: 5 | [MEDIUM]: 5 | [LOW]: 2
================================================================================
[FILE] src/auth.py
 ├─ [HIGH] OS Command Injection
 │   - Location: Line 42
 │   - Snippet: subprocess.call('rm -rf ' + user_input, shell=True)
 │   - Remediation: Validate inputs or use argument‑list APIs.
 └─ [HIGH] Exposed Secrets / Hardcoded Credentials
     - Location: Line 8
     - Snippet: API_KEY = "12345-SECRET-KEY"
     - Remediation: Move secrets to environment variables or a vault.
...
[INFO] Detailed JSON report exported to: security_audit_report.json
Exporting in other formats
bash


# JSON (default)
logflash path/to/project
# SARIF (for GitHub Actions, Azure DevOps, etc.)
logflash path/to/project --sarif > findings.sarif
# Plain JSON only (no console banner)
logflash path/to/project --json > findings.json
📂 Rule System
Rules live in logflash/rules/*.json. Each rule follows this schema:

json


{
  "rule_id": "SEC-CWE-798",
  "vulnerability_name": "Exposed Secrets / Hardcoded Credentials",
  "severity_rating": "HIGH",
  "pattern": "(?i)\\b(?:api[_-]?key|secret|password)\\s*=\\s*['\\\"]\\w{6,}['\\\"]",
  "description": "...",
  "remediation": "..."
}
Add your own rule files – drop a JSON/YAML file into a folder and point logflash at it:
bash


logflash --rules ./my_custom_rules path/to/code
Built‑in language parsers (Python, JavaScript, PHP, C/C++, Java) feed the scanner with language‑specific findings; the generic rule engine then matches those findings against the rule set.
🛠️ Extending logflash
Write a new parser under src/logflash/parsers/ that returns a list of dictionaries:

python


[{"line": 12, "snippet": "exec(user_input)", "type": "exec"}]
Register it in src/logflash/parsers/__init__.py with the file extension you want to support.

Add rules for the new language in a JSON file placed alongside the existing ones.

That’s all – no changes to the core engine are required.

📚 Documentation
Full docs are hosted in the docs/ folder (and will be published on GitHub Pages):

Usage guide – detailed CLI options, environment variables, and CI integration.
Rule authoring – how to write safe regexes, severity conventions, and versioning.
Parser development – step‑by‑step for adding support for new languages.
Contribution guide – coding standards, testing, and release workflow.
🤝 Contributing
We welcome contributions! Please:

Fork the repo and create a new branch.
Run the test suite locally: pytest -q.
Add or update tests for any new parser/rule.
Open a Pull Request with a clear description of the change.
Refer to CONTRIBUTING.md for the full workflow (including linting, pre‑commit hooks, and release automation).

📦 Release & Versioning
Semantic versioning (MAJOR.MINOR.PATCH).
The rule set is versioned together with the package, but you can also publish a separate data package (logflash‑rules) if you want to decouple rule updates from code releases.
📢 License
logflash is released under the MIT License – feel free to use it in commercial or open‑source projects.

⭐️ Show your support
If you find logflash useful, give it a ⭐ on GitHub, or drop us a line on Twitter 👉 @logflash_sast.

Happy scanning! 🚀

10:44 PM



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
