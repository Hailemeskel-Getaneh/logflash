import pathlib
import re

def parse_js(file_path: pathlib.Path):
    """Lightweight parser for JavaScript files.

    Detects common risky patterns such as exec calls and innerHTML assignments.
    Returns a list of dicts with line, snippet and type.
    """
    findings = []
    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return findings
    for i, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        # Detect exec (Node.js child_process.exec)
        if re.search(r"\bexec\s*\(", line):
            findings.append({"line": i, "snippet": stripped, "type": "exec"})
        # Detect innerHTML assignment
        if re.search(r"\.innerHTML\s*=", line):
            findings.append({"line": i, "snippet": stripped, "type": "innerhtml"})
        # Detect eval usage
        if re.search(r"\beval\s*\(", line):
            findings.append({"line": i, "snippet": stripped, "type": "eval"})
    return findings
