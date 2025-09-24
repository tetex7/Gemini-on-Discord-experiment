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
import re
from FileBackedRingBuffer import FileBackedRingBuffer
import request_system

recent_thoughts_buff = FileBackedRingBuffer("thoughts.json", size=10)

def recent_talk(previous_messages: list[discord.Message]):
    hist = list(reversed(previous_messages.copy()))
    return "Recent messages before current user prompt\nYou may reference former history but do not recite verbatim\n" + "".join([f"{msg.author.display_name}@{msg.created_at}: \"{msg.content}\"\n" for msg in hist])


def recent_thoughts():
    return "\n\n<recent_thoughts>\n" + "".join([f"\"{thought}\"\n" for thought in recent_thoughts_buff.to_list()]) + "</recent_thoughts>\n\n"


def request_fulfillment_block():
    return "".join([f"{fulfilled}\n" for fulfilled in request_system.perform_AI_syscall_requests()])

def post_process_response(response: str):
    for selfs in re.findall(r"<self>(.*?)</self>", response, flags=re.DOTALL):
        recent_thoughts_buff.push(re.sub(r"<important>", "", selfs), len(re.findall(r"<important>", selfs)) > 0)

    for syscalls in re.findall(r"<syscall>(.*?)</syscall>", response, flags=re.DOTALL):
        print(f"Requests made for {syscalls}")
        request_system.ai_requests.append(syscalls)

    cleaned = re.sub(r"<syscall>.*?</syscall>", "", response, flags=re.DOTALL)
    cleaned = re.sub(r"<self>.*?</self>", "", cleaned, flags=re.DOTALL)
    return cleaned

def _form_context_reply_header(prev_message: discord.Message):
    return f"Previous bot message: {prev_message.content}\nUser reply:"

def form_self_prompt():
    prompt = request_fulfillment_block() + recent_thoughts() + "\n\n\n"

    prompt += """
This is a self prompt You are completely in your own head your output is to be put into a <self> block
Any thoughts made here can be important they don't need to be You're completely free here To review your thoughts and memories
If you ever mention your tags don't use '<' or '>' To prevent accidental tag usage
You're allowed to make internal syscalls for your own self
"""
    return prompt

def form_prompt(bot_mention: str, bot_name: str, msg: discord.Message, is_reply: bool, recent_message_history: list[discord.Message]):
    prompt = request_fulfillment_block() + recent_thoughts() + "\n\n" + recent_talk(recent_message_history) + "\n\n\n"

    if is_reply:
        prompt += _form_context_reply_header(msg.reference.resolved)
    else:
        prompt += "User:"


    prompt += msg.content.replace(bot_mention, bot_name).strip()

    return prompt
    