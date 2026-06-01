from .python_parser import parse_python
from .js_parser import parse_js

def get_parser_for_ext(ext: str):
    return {
        ".py": parse_python,
        ".js": parse_js,
        # Add more extensions as parsers are implemented
    }.get(ext.lower())
