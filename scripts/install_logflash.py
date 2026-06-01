"""install_logflash.py
A small helper script that installs the latest `logflash` package from PyPI while providing a colorful, spinner‑styled user experience.

Usage (from the command line):
    python install_logflash.py

The script:
- Ensures `rich` is installed (used for colors & spinner).
- Runs `pip install --upgrade logflash` in a subprocess.
- Shows a live spinner with the message "Installing logflash…".
- Streams pip's stdout/stderr to the console with color coding.
- Prints a final success or error message.
"""

import sys
import subprocess
import shutil
from pathlib import Path

def ensure_rich():
    """Install the `rich` library if it is not already available."""
    try:
        import rich  # noqa: F401
    except ImportError:
        print("[bold yellow]Installing missing dependency: rich[/]")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "rich"])

ensure_rich()
from rich.console import Console
from rich.spinner import Spinner
from rich.text import Text
from rich.panel import Panel

console = Console()

def run_pip_install():
    """Execute `pip install --upgrade logflash` and stream its output.
    Returns the subprocess exit code.
    """
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "logflash"]
    # Use subprocess.Popen to capture stdout/stderr line‑by‑line
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    for line in process.stdout:
        # Remove trailing newline and apply simple color logic
        line = line.rstrip()
        if "Downloading" in line or "Collecting" in line:
            console.print(f"[cyan]{line}[/]")
        elif "Successfully installed" in line:
            console.print(f"[green]{line}[/]")
        elif "Requirement already satisfied" in line:
            console.print(f"[magenta]{line}[/]")
        elif "error" in line.lower() or "failed" in line.lower():
            console.print(f"[red]{line}[/]")
        else:
            console.print(line)
    process.wait()
    return process.returncode

with console.status("[bold blue]Installing logflash…", spinner="dots") as status:
    exit_code = run_pip_install()

if exit_code == 0:
    console.print(Panel(Text("logflash installed successfully!", style="bold green"), border_style="green"))
    # Show version info using the package's CLI if available
    try:
        subproc = subprocess.run(["logflash", "-h"], capture_output=True, text=True)
        console.print(Panel(Text(subproc.stdout, style="white"), title="logflash help", border_style="blue"))
    except FileNotFoundError:
        console.print("[yellow]logflash command not found in PATH – you may need to restart your shell.[/]")
else:
    console.print(Panel(Text(f"Installation failed with exit code {exit_code}", style="bold red"), border_style="red"))
