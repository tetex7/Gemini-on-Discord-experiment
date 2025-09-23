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


import os
import json

class FileBackedRingBuffer:
    def __init__(self, filepath, size):
        self.filepath = filepath
        self.size = size
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                json.dump([], f, indent=4)

    def _read_buffer(self):
        with open(self.filepath, "r") as f:
            return json.load(f)

    def _write_buffer(self, buffer):
        with open(self.filepath, "w") as f:
            json.dump(buffer, f, indent=4)

    def push(self, thought, important=False):
        """Push a new thought into the buffer. 
        If important=True, it won't be automatically removed.
        """
        buffer = self._read_buffer()
        # append as a dict
        buffer.append({"text": thought, "important": important})

        # trim only non-important thoughts if buffer is too big
        non_important_count = sum(1 for t in buffer if not t["important"])
        while non_important_count > self.size:
            # remove the oldest non-important thought
            for i, t in enumerate(buffer):
                if not t["important"]:
                    del buffer[i]
                    break
            non_important_count -= 1

        self._write_buffer(buffer)

    def to_list(self):
        """Return a list of just the thought strings, ignoring importance."""
        buffer = self._read_buffer()
        return [t["text"] for t in buffer]

    def delete(self, index):
        """Manually delete a thought by index (in the stored list)."""
        buffer = self._read_buffer()
        if 0 <= index < len(buffer):
            del buffer[index]
            self._write_buffer(buffer)