import os
import re
import pathlib
from logflash.parsers import get_parser_for_ext
from logflash.rules import VULNERABILITY_RULES

class AegisScanner:
    def __init__(self, target_path):
        self.target_path = target_path
        self.findings = []
        self.files_scanned = 0

    def get_supported_extensions(self):
        extensions = set()
        for rule in VULNERABILITY_RULES:
            extensions.update(rule["target_extensions"])
        return list(extensions)

    def crawl_and_filter(self):
        """Recursively walks through subfolders and filters by extension."""
        supported_extensions = self.get_supported_extensions()
        target_files = []
        
        # Standard directories to skip (prevents scanning thousands of dependency files)
        ignore_dirs = {'.git', 'node_modules', 'venv', 'env', '__pycache__', '.pytest_cache', 'dist', 'build', 'vendor'}

        if os.path.isfile(self.target_path):
            if any(self.target_path.endswith(ext) for ext in supported_extensions):
                target_files.append(self.target_path)
            return target_files

        for root, dirs, files in os.walk(self.target_path):
            # Modify dirs in-place to skip ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for file in files:
                if any(file.endswith(ext) for ext in supported_extensions):
                    target_files.append(os.path.join(root, file))
        return target_files

    def _is_comment(self, line, in_block_comment, ext):
        """Checks if a line is a comment or inside a block comment."""
        line_stripped = line.strip()

        # Handle block comments
        if ext in ['.c', '.cpp', '.h', '.java', '.php', '.js']:
            if '/*' in line_stripped:
                in_block_comment = True
            if '*/' in line_stripped:
                in_block_comment = False
                return True, in_block_comment # The line ending the block comment is considered a comment
        elif ext in ['.py']:
            if line_stripped.startswith("'''") or line_stripped.startswith('"""'):
                in_block_comment = not in_block_comment
                return True, in_block_comment

        if in_block_comment:
            return True, in_block_comment

        # Handle single-line comments
        if ext in ['.c', '.cpp', '.h', '.java', '.php', '.js']:
            if line_stripped.startswith('//'):
                return True, in_block_comment
        if ext in ['.py', '.env', '.yml']:
            if line_stripped.startswith('#'):
                return True, in_block_comment

        return False, in_block_comment

    def scan_file(self, file_path):
        """Scans a file using a language‑specific parser and applies the rule set.

        The parser returns a list of raw findings (line number, snippet, type).
        Each finding is then matched against all loaded vulnerability rules.
        """
        _, ext = os.path.splitext(file_path)
        parser = get_parser_for_ext(ext)
        if not parser:
            # Unsupported file type – skip
            return
        try:
            self.files_scanned += 1
            raw_findings = parser(pathlib.Path(file_path))
            for raw in raw_findings:
                for rule in self.rules:
                    if ext in rule.get("target_extensions", []):
                        if rule["regex"].search(raw["snippet"]):
                            self.findings.append({
                                "rule_id": rule["rule_id"],
                                "vulnerability_name": rule["vulnerability_name"],
                                "severity_rating": rule["severity_rating"],
                                "target_file": file_path,
                                "line_number": raw["line"],
                                "offending_code_snippet": raw["snippet"],
                                "vulnerability_description": rule["vulnerability_description"],
                                "remediation_guideline": rule["remediation_guideline"],
                            })
        except Exception as e:
            print(f"[ERROR] Parser error for {file_path}: {e}")
            return
        except OSError as e:
            print(f"Error reading file {file_path}: {e}")

    def run(self, progress_callback=None):
        """Executes the scanning pipeline."""
        files_to_scan = self.crawl_and_filter()
        total_files = len(files_to_scan)
        for index, file in enumerate(files_to_scan, start=1):
            if progress_callback:
                progress_callback(index, total_files, file)
            self.scan_file(file)
        return self.findings
