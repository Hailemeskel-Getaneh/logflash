import re

# Severity Levels
SEVERITY_CRITICAL = "CRITICAL"
SEVERITY_HIGH = "HIGH"
SEVERITY_MEDIUM = "MEDIUM"
SEVERITY_LOW = "LOW"

# Vulnerability Definitions
VULNERABILITY_RULES = [
    {
        "rule_id": "SEC-CWE-120",
        "vulnerability_name": "Buffer Overflow (Unbounded Copy)",
        "severity_rating": SEVERITY_CRITICAL,
        "target_extensions": [".c", ".cpp", ".h"],
        # Match gets(), strcpy(), sprintf(), strcat() ignoring leading spaces and spaces before '('
        "regex": re.compile(r'\b(gets|strcpy|sprintf|strcat)\s*\('),
        "vulnerability_description": "Use of low-level, non-bounds-checking memory allocation or string array operations.",
        "remediation_guideline": "CRITICAL: Replace with safe, length-enforced bounds checking execution boundaries (e.g., fgets(), strncpy(), snprintf())."
    },
    {
        "rule_id": "SEC-CWE-89",
        "vulnerability_name": "SQL Injection (Dynamic Query)",
        "severity_rating": SEVERITY_HIGH,
        "target_extensions": [".py", ".java", ".php", ".js"],
        # Match "SELECT ... " + var, f"SELECT ... {var}", or query("... $_GET ...")
        # Match SQL clauses combined with concatenation (+ or .), f-strings ({...}), or PHP superglobals
        "regex": re.compile(r'(?i)(?:SELECT\s+.+\s+FROM|INSERT\s+INTO|UPDATE\s+.+\s+SET|DELETE\s+FROM).*(?:\+[\s]*[a-zA-Z_]|\.[\s]*\$|\{.*\}|\$\{.*\}|\$_(GET|POST|REQUEST))'),
        "vulnerability_description": "Dynamic construction of database query commands utilizing string concatenation or direct variable interpolation.",
        "remediation_guideline": "HIGH: Structural security failure. Abandon dynamic string parsing. Enforce the implementation of Parameterized Queries or Prepared Statement Interfaces exclusively."
    },
    {
        "rule_id": "SEC-CWE-79",
        "vulnerability_name": "Cross-Site Scripting (XSS)",
        "severity_rating": SEVERITY_MEDIUM,
        "target_extensions": [".php", ".html", ".js", ".py"],
        # Match .innerHTML, document.write, echo $_GET, echo $_POST
        "regex": re.compile(r'(\.innerHTML\s*=|document\.write\s*\(|echo\s+\$_(GET|POST))'),
        "vulnerability_description": "Unsanitized rendering sinks where user-controlled input parameter streams are passed directly into the DOM or echoed to the client.",
        "remediation_guideline": "MEDIUM: Apply context-aware HTML entity output encoding or run data payloads through a trusted sanitization abstraction layer before browser serialization."
    },
    {
        "rule_id": "SEC-CWE-798",
        "vulnerability_name": "Exposed Secrets / Hardcoded Credentials",
        "severity_rating": SEVERITY_HIGH,
        "target_extensions": [".env", ".py", ".js", ".json", ".yml"],
        # Match variables like api_key, secret_key, password being assigned a string > 6 chars
        "regex": re.compile(r'(?i)(api_key|secret_key|password|db_password|private_key)\s*[:=]\s*["\'][a-zA-Z0-9_-]{7,}["\']'),
        "vulnerability_description": "Hardcoded assignment strings where variables indicative of secrets are directly assigned literal string values longer than 6 alphanumeric characters.",
        "remediation_guideline": "HIGH: Private credential exposed in raw code layout. Migrate token parameters out of code assets and securely inject them via System Environment Variables or Secrets Vaults."
    }
]
