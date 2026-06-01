# Rules Documentation

This document describes the rule format used by **logflash**. Rules can be provided as **JSON** or **YAML** files placed in a directory and passed to the CLI via the `--rules` flag.

## Rule Schema
Each rule is a JSON/YAML object with the following keys:

- `rule_id` (string): Unique identifier, e.g., `SEC-CWE-798`.
- `vulnerability_name` (string): Human‑readable name.
- `severity_rating` (string): One of `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`.
- `regex` (string): Regular expression (Python syntax) that matches offending code snippets.
- `target_extensions` (list of strings): File extensions the rule applies to, e.g., `[".py", ".js"]`.
- `vulnerability_description` (string): Explanation of the issue.
- `remediation_guideline` (string): Suggested fix.

## Example Rule (JSON)
```json
{
  "rule_id": "SEC-CWE-798",
  "vulnerability_name": "Exposed Secrets / Hardcoded Credentials",
  "severity_rating": "HIGH",
  "regex": "(?i)api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9-_]{6,}['\"]?",
  "target_extensions": [".py", ".js"],
  "vulnerability_description": "Hardcoded credential strings longer than six alphanumeric characters.",
  "remediation_guideline": "Store secrets outside source code, e.g., environment variables or secret vaults."
}
```

## Example Rule (YAML)
```yaml
rule_id: SEC-CWE-798
vulnerability_name: Exposed Secrets / Hardcoded Credentials
severity_rating: HIGH
regex: "(?i)api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9-_]{6,}['\"]?"
target_extensions:
  - .py
  - .js
vulnerability_description: Hardcoded credential strings longer than six alphanumeric characters.
remediation_guideline: Store secrets outside source code, e.g., environment variables or secret vaults.
```

## Adding Custom Rules
1. Create a `rules/` directory at the project root (or any location you prefer).
2. Add one or more `.json`/`.yaml` files following the schema above.
3. Run `logflash --rules path/to/your/rules <target>`.

The scanner will automatically load **all** JSON and YAML files in the provided directory.
