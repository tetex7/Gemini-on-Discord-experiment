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

import google.genai as genai
import os
import discord
import re

# Initialize the Gemini client
client = genai.Client(api_key=os.environ["AI_API_KEY"])

def get_sys_prompt():
    if not os.path.exists("system.prompt"):
        raise Exception("a system prompt file is required")
    with open("system.prompt", "r") as f:
        return re.sub(r"<comment>.*?</comment>", "", f.read(), flags=re.DOTALL).strip()
    

def fill_system_prompt(bot_user: discord.User | None, user: discord.User | None):
    system_instruction = get_sys_prompt()
    
    system_instruction = system_instruction.replace(
        "${BOT_NAME}$", bot_user.display_name if bot_user else "not specified"
    ).replace(
        "${BOT_AT}$", bot_user.mention if bot_user else "not specified"
    ).replace(
        "${BOT_ID}$", str(bot_user.id) if bot_user else "not specified"
    ).replace(
        "${USER_NAME}$", user.display_name if user else "not specified"
    ).replace(
        "${USER_ID}$", str(user.id) if user else "not specified"
    )
    
    return system_instruction


def generate_response(user: discord.User | None, bot_user: discord.User | None, prompt: str):
    response = client.models.generate_content(
        # gemini-2.5-flash-lite Is a little too dumb to work with the system prompt
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction=fill_system_prompt(bot_user, user)
        ),
        contents=prompt
    )
    return response.text