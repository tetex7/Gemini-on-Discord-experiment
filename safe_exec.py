#
# Copyright (C) 2025 Tetex7
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import re
import io
import sys

ALLOWED_BUILTINS = {
    "print": print,
    "len": len,
    "range": range,
    "int": int,
    "float": float,
    "str": str,
}

ALLOWED_MODULES = {"time", "math"}  # safe modules you want AI to access

FORBIDDEN_PATTERNS = [
    r"import\s+os",
    r"import\s+sys",
    r"open\s*\(",
    r"exec\s*\(",
    r"eval\s*\(",
    r"__.*__"
]

def safe_exec(code: str) -> str:
    # pre-check for forbidden patterns
    if any(re.search(pat, code, re.IGNORECASE) for pat in FORBIDDEN_PATTERNS):
        raise ValueError("Unsafe code detected!")

    # redirect output to a string buffer
    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer

    try:
        # create a safe execution environment
        safe_globals = {"__builtins__": ALLOWED_BUILTINS}
        for mod in ALLOWED_MODULES:
            safe_globals[mod] = __import__(mod)
        
        exec(code, safe_globals, {})  # run the AI code safely
    finally:
        sys.stdout = old_stdout  # restore stdout

    return buffer.getvalue()  # return everything that was printed
