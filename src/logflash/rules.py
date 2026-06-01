import json
import os
import re

# Optional YAML support
try:
    import yaml
except ImportError:
    yaml = None

# Severity Levels
SEVERITY_CRITICAL = "CRITICAL"
SEVERITY_HIGH = "HIGH"
SEVERITY_MEDIUM = "MEDIUM"
SEVERITY_LOW = "LOW"

# Path to default rule directory
_RULES_DIR = os.path.join(os.path.dirname(__file__), "rules")

def _load_json_rules(json_path: str):
    """Load rules from a JSON file and compile regexes."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for rule in data:
        rule["regex"] = re.compile(rule["regex"])  # compile pattern
    return data

def _load_yaml_rules(yaml_path: str):
    """Load rules from a YAML file and compile regexes (if yaml lib is available)."""
    if yaml is None:
        return []
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    for rule in data:
        rule["regex"] = re.compile(rule["regex"])  # compile pattern
    return data

def _load_all_rules():
    """Load all rule files (JSON and optionally YAML) from the rules directory."""
    rules = []
    # Load JSON files
    for entry in os.listdir(_RULES_DIR):
        path = os.path.join(_RULES_DIR, entry)
        if entry.lower().endswith('.json') and os.path.isfile(path):
            rules.extend(_load_json_rules(path))
        elif entry.lower().endswith(('.yaml', '.yml')) and os.path.isfile(path):
            rules.extend(_load_yaml_rules(path))
    return rules

# Load the default rule set at import time
VULNERABILITY_RULES = _load_all_rules()
