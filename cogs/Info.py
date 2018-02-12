import pytz
import discord
import unicodedata
from discord.ext import commands
import time
import datetime
import psutil
import requests
import ftfy
import traceback
import openweathermapy.core as weather
import platform
import copy
import asyncio
import os
import urllib.parse
from urllib.request import urlopen
import aiohttp
import json
import random
from utils.paginator import Pages
import io
import textwrap
import subprocess
import inspect
from urllib.parse import urlencode
from contextlib import redirect_stdout
from utils.config import *
from ext import utils
from pyfiglet import figlet_format as ascii_format


class Info:
    '''Information commands'''

    def __init__(self, bot):
        self.bot = bot




    @commands.command(brief="Display role info.", aliases=["rinfo"])
    @commands.guild_only()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def roleinfo(self, ctx, *, role:discord.Role):
        """Display information about a role.
        
        * role - The role to display information about."""
        
        embed = discord.Embed(title=role.name)
        embed.color = role.color
        embed.description = role.id
        
        embed.add_field(name="Create instant invite", value=role.permissions.create_instant_invite)
        embed.add_field(name="Kick members", value=role.permissions.kick_members)
        embed.add_field(name="Ban members", value=role.permissions.ban_members)
        embed.add_field(name="Administrator", value=role.permissions.administrator)
        embed.add_field(name="Manage channels", value=role.permissions.manage_channels)
        embed.add_field(name="Manage guild", value=role.permissions.manage_guild)
        embed.add_field(name="Add reactions", value=role.permissions.add_reactions)
        embed.add_field(name="Read messages", value=role.permissions.read_messages)
        embed.add_field(name="Send messages", value=role.permissions.send_messages)
        embed.add_field(name="Send TTS messages", value=role.permissions.send_tts_messages)
        embed.add_field(name="Manage messages", value=role.permissions.manage_messages)
        embed.add_field(name="Embed links", value=role.permissions.embed_links)
        embed.add_field(name="Attach files", value=role.permissions.attach_files)
        embed.add_field(name="Read message history", value=role.permissions.read_message_history)
        embed.add_field(name="Mention everyone", value=role.permissions.mention_everyone)
        embed.add_field(name="External emojis", value=role.permissions.external_emojis)
        embed.add_field(name="Connect to voice channel", value=role.permissions.connect)
        embed.add_field(name="Speak in voice channel", value=role.permissions.speak)
        embed.add_field(name="Mute members", value=role.permissions.mute_members)
        embed.add_field(name="Deafen members", value=role.permissions.deafen_members)
        embed.add_field(name="Move members", value=role.permissions.move_members)
        embed.add_field(name="Use voice activation", value=role.permissions.use_voice_activation)
        embed.add_field(name="Change nickname", value=role.permissions.change_nickname)
        embed.add_field(name="Manage nicknames", value=role.permissions.manage_nicknames)
        
        embed2 = discord.Embed()
        embed2.color = role.color
        embed2.add_field(name="Manage roles", value=role.permissions.manage_roles)
        embed2.add_field(name="Manage webhooks", value=role.permissions.manage_webhooks)
        embed2.add_field(name="Manage emojis", value=role.permissions.manage_emojis)
        
        await ctx.send(embed=embed)
        await ctx.send(embed=embed2)


    @commands.command()
    async def datetime(self, ctx, tz=None):
        """Get the current date and time for a time zone or UTC."""
        now = datetime.datetime.now(tz=pytz.UTC)
        all_tz = 'https://pastebin.com/raw/FLh9cyvp'
        if tz:
            try:
                now = now.astimezone(pytz.timezone(tz))
            except:
                em = discord.Embed(color=failcolor)
                em.title = "Invalid timezone"
                em.description = f'Please take a look at the [list]({all_tz}) of timezones.'
                return await ctx.send(embed=em)
        await ctx.send(f'It is currently {now:%A, %B %d, %Y} at {now:%I:%M:%S %p}.')























def setup(bot):
    bot.add_cog(Info(bot))