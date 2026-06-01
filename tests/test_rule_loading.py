# Test suite for logflash

import json
import pathlib

from logflash.rules import VULNERABILITY_RULES

def test_rules_loaded():
    assert isinstance(VULNERABILITY_RULES, list)
    assert len(VULNERABILITY_RULES) > 0
    # Ensure each rule has required keys
    required_keys = {
        "rule_id",
        "vulnerability_name",
        "severity_rating",
        "regex",
        "target_extensions",
        "vulnerability_description",
        "remediation_guideline",
    }
    for rule in VULNERABILITY_RULES:
        assert required_keys.issubset(rule.keys())
