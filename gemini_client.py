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
        return re.sub(r"<comment>.*?</<comment>", "", f.read(), flags=re.DOTALL).strip()


def generate_response(user: discord.User, bot_user: discord.User, prompt: str):
    response = client.models.generate_content(

        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction=get_sys_prompt()
            .replace("${BOT_NAME}$", bot_user.display_name)
            .replace("${BOT_AT}$", bot_user.mention)
            .replace("${BOT_ID}$", str(bot_user.id))
            .replace("${USER_NAME}$", user.display_name)
            .replace("${USER_ID}$", str(user.id))
        ),
        contents=prompt
    )
    return response.text