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
from collections import deque
_ai_syscalls = {}
ai_requests = deque()

def _ai_syscall_register(name: str, description: str):
    def decorator(func):
        _ai_syscalls[name] =  { "call": func, "disname": name, "description": description }
        return func
    return decorator

@_ai_syscall_register("UTC", "Gets the UTC time")
def _utc(arg:str):
    from datetime import datetime, timezone
    return str(datetime.now(timezone.utc))

@_ai_syscall_register("list-syscalls", "Gets all known syscalls")
def _list_calls(arg: str):
    out = ""
    for call, meta in _ai_syscalls.items():
        out += f'{{"name": "{meta["disname"]}", "description": "{meta["description"]}"}}\n'
    return out

def perform_AI_syscall_requests():
    output = deque()
    for regu in ai_requests:
        if regu not in _ai_syscalls:
            output.append(f"<failed_syscall>\'{regu}\' does not exist and or Not implemented </failed_syscall>")
            continue
        
        output.append(f"<fulfilled_syscall>{_ai_syscalls[regu]["call"]("")}</fulfilled_syscall>")
    ai_requests.clear()
    return list(output)



