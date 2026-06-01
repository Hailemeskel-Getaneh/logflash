import os
import sys
import json
import argparse
from logflash.engine import AegisScanner
from logflash.rules import SEVERITY_CRITICAL, SEVERITY_HIGH, SEVERITY_MEDIUM, SEVERITY_LOW
from rich.console import Console
console = Console()
from importlib import metadata

def setup_mock_sandbox():
    """Programmatically creates a temporary folder with mock vulnerable files."""
    sandbox_dir = "mock_sandbox"
    os.makedirs(sandbox_dir, exist_ok=True)

    # 1. C++ Buffer Overflow (And a commented one to test comment handling)
    with open(os.path.join(sandbox_dir, "vulnerable.cpp"), "w") as f:
        f.write("#include <iostream>\n")
        f.write("int main() {\n")
        f.write("    char buffer[10];\n")
        f.write("    // gets(buffer); // Safely commented out\n")
        f.write("    gets(buffer); // Vulnerability here\n")
        f.write("    return 0;\n")
        f.write("}\n")

    # 2. Python SQL Injection
    with open(os.path.join(sandbox_dir, "db.py"), "w") as f:
        f.write("def get_user(user_id):\n")
        f.write("    query = f\"SELECT * FROM users WHERE id = {user_id}\"\n")
        f.write("    # execute(query)\n")
        f.write("    return query\n")

    # 3. PHP XSS
    with open(os.path.join(sandbox_dir, "index.php"), "w") as f:
        f.write("<?php\n")
        f.write("    $name = $_GET['name'];\n")
        f.write("    /* echo $_GET['name']; */\n")
        f.write("    echo $_GET['name'];\n")
        f.write("?>\n")

    # 4. JS Exposed Secrets
    with open(os.path.join(sandbox_dir, "config.js"), "w") as f:
        f.write("const config = {\n")
        f.write("    api_key: 'A1b2C3d4E5f6G7h8I9j0',\n")
        f.write("    // password: 'my_secret_password'\n")
        f.write("};\n")

    return sandbox_dir

def sort_severity(severity):
    """Helper for sorting by severity (High -> Low)."""
    order = {SEVERITY_CRITICAL: 0, SEVERITY_HIGH: 1, SEVERITY_MEDIUM: 2, SEVERITY_LOW: 3}
    return order.get(severity, 4)

def generate_console_report(findings, files_scanned):
    """Prints a formatted summary to the console, grouped by file and sorted by severity."""
    print("\n" + "="*80)
    print(" logflash - Security Audit Report")
    print("="*80)
    
    # Calculate metrics
    total_findings = len(findings)
    severity_counts = {SEVERITY_CRITICAL: 0, SEVERITY_HIGH: 0, SEVERITY_MEDIUM: 0, SEVERITY_LOW: 0}
    for finding in findings:
        severity_counts[finding['severity_rating']] += 1

    print(f"\n EXECUTIVE METRICS SUMMARY")
    print("-" * 30)
    print(f" Total Files Scanned: {files_scanned}")
    print(f" TOTAL FINDINGS:      {total_findings} | " + 
          f"[CRITICAL]: {severity_counts[SEVERITY_CRITICAL]} | " +
          f"[HIGH]: {severity_counts[SEVERITY_HIGH]} | " +
          f"[MEDIUM]: {severity_counts[SEVERITY_MEDIUM]} | " +
          f"[LOW]: {severity_counts[SEVERITY_LOW]}")
    print("="*80)

    # Group findings by file
    grouped_findings = {}
    for finding in findings:
        file_path = finding['target_file']
        if file_path not in grouped_findings:
            grouped_findings[file_path] = []
        grouped_findings[file_path].append(finding)

    # Print grouped findings
    for file_path, file_findings in grouped_findings.items():
        print(f"\n [FILE] {file_path}")
        print("-" * 80)
        
        # Sort findings within the file by severity
        sorted_findings = sorted(file_findings, key=lambda x: sort_severity(x['severity_rating']))
        
        for finding in sorted_findings:
            print(f" [{finding['severity_rating']}] {finding['vulnerability_name']}")
            print(f"   - Location: Line {finding['line_number']}")
            print(f"   - Snippet: {finding['offending_code_snippet']}")
            print(f"   - Remediation: {finding['remediation_guideline']}\n")

def export_json_report(findings):
    """Serializes the findings array into a JSON file."""
    output_file = "security_audit_report.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(findings, f, indent=4)
    print(f"\n [INFO] Detailed JSON report exported to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="logflash: A Modular SAST Engine")
    parser.add_argument("target", nargs="?", help="Target directory or file to scan (Leave empty to run mock sandbox)")
    parser.add_argument("--rules", help="Path to a directory containing .json rule files (overrides built-in rules).")
parser.add_argument("-v", "--version", action="store_true", help="Show package version and exit")
    args = parser.parse_args()
if args.version:
    console.print(f"logflash {metadata.version('logflash')}")
    sys.exit(0)

    # Load custom rules if provided
    if args.rules:
        import json, pathlib, re
        custom_rules = []
        rules_dir = pathlib.Path(args.rules)
        for rule_file in rules_dir.glob("*.json"):
            with rule_file.open(encoding="utf-8") as f:
                data = json.load(f)
                for rule in data:
                    rule["regex"] = re.compile(rule["regex"])
                custom_rules.extend(data)
        # Override the default rule set
        from logflash import rules as rules_module
        rules_module.VULNERABILITY_RULES = custom_rules


    target_path = args.target

    if not target_path:
        console.print("[INFO] No target path provided. Initializing Mock Sandbox...")
        target_path = setup_mock_sandbox()

    if not os.path.exists(target_path):
        console.print(f"[ERROR] Target path '{target_path}' does not exist.")
        sys.exit(1)

    console.print(f"\n[INFO] Starting logflash on target: {target_path}\n")
    
    def print_progress(current, total, file_path):
        # Simple progress bar – same as before but with a rotating spinner
        spinner = "|/-\\"
        spin_char = spinner[(current) % len(spinner)]
        term_width = 80
        base_msg = f"Scanning [{current}/{total}] {spin_char}: {os.path.basename(file_path)}"
        if len(base_msg) > term_width - 5:
            base_msg = base_msg[:term_width-8] + "..."
        msg = base_msg.ljust(term_width)
        sys.stdout.write(f"\r{msg}")
        sys.stdout.flush()

    scanner = AegisScanner(target_path)
    findings = scanner.run(progress_callback=print_progress)
    
    # Clear the progress line before printing the report
    # Clear progress line
sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.flush()
    
    generate_console_report(findings, scanner.files_scanned)
    export_json_report(findings)

if __name__ == "__main__":
    main()
