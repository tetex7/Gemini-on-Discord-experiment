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

import discord
from discord.ext import commands
import gemini_client
import intelligence
import os
import sys
import re
import time
import random
import threading

intelligence.recent_thoughts_buff.push("Your mind is a little clear and fresh because you just came back online")
"""
def run_self_prompt_periodically():
    while True:
        # Wait a random interval between 5 and 20 seconds
        interval = random.uniform(5, 20)
        time.sleep(interval)

        # Run your function
        self_response = gemini_client.generate_response(None, None, intelligence.form_self_prompt())
        print(f"raw self output: \"\"\"\n{self_response}\n\"\"\"")
        intelligence.post_process_response(self_response)

# Start the background thread
thread = threading.Thread(target=run_self_prompt_periodically, daemon=True)
thread.start()
"""

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user or message.author.bot:
        return
    print(f"new message \"\"\"\n{message.content}\n\"\"\"")

    is_mention = (bot.user in message.mentions) or (str(bot.user.id) in message.content)

    # Check if it's a reply to one of the bot's messages
    is_reply = (
        message.reference is not None
        and message.reference.resolved is not None
        and message.reference.resolved.author == bot.user
    )

    # Check if the message mentions the bot
    if is_mention or is_reply:
        print("New message accepted")


        # Fetch the last 3 messages (including this one)
        history = [msg async for msg in message.channel.history(limit=4)]
        
        full_prompt = intelligence.form_prompt(
            bot.user.mention, 
            bot.user.display_name, 
            message, 
            is_reply, 
            history
        )

        print(f"outbound prompt: \"\"\"\n{full_prompt}\n\"\"\"")


        # Generate a response from Gemini
        response = gemini_client.generate_response(
            message.author,
            bot.user,
            full_prompt
        )

        print(f"raw output: \"\"\"\n{response}\n\"\"\"")


        processed_response = intelligence.post_process_response(response)

        await message.reply(processed_response)
        if "${EXIT NOW}$" in processed_response:
            intelligence.recent_thoughts_buff.push("You just shut yourself down Now you're just coming on back online")
            sys.exit(1)

bot.run(os.environ["DISCORD_API_KEY"])