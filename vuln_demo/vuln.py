import os
import subprocess

# Example of command injection vulnerability
user_input = input('Enter a filename to list: ')
# BAD: directly concatenating user input into a shell command
subprocess.call('dir ' + user_input, shell=True)

# Hardcoded secret (should be flagged)
API_KEY = "12345-SECRET-KEY"
print('Using API key:', API_KEY)

# Use of eval (code injection)
code = input('Enter python code to execute: ')
result = eval(code)  # BAD: evaluating arbitrary code
print('Result:', result)
