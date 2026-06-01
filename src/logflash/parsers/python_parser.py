import pathlib
import re

def parse_python(file_path: pathlib.Path):
    """Lightweight parser for Python files.

    Returns a list of finding dicts with ``line``, ``snippet`` and ``type``.
    Currently it looks for ``subprocess`` calls and ``eval`` usage, which are
    common sources of command injection and code execution vulnerabilities.
    """
    findings = []
    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return findings
    for i, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        # Detect subprocess calls that may execute shell commands
        if re.search(r"\bsubprocess\.(call|run|Popen)\s*\(", line):
            findings.append({"line": i, "snippet": stripped, "type": "subprocess_call"})
        # Detect eval usage
        if re.search(r"\beval\s*\(", line):
            findings.append({"line": i, "snippet": stripped, "type": "eval"})
        # Detect os.system
        if re.search(r"\bos\.system\s*\(", line):
            findings.append({"line": i, "snippet": stripped, "type": "os_system"})
    return findings
