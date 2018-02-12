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
import pynite

class Fortnite:
    '''
    Get information about a Fortnite user
    '''

    def __init__(self, bot):
        self.bot = bot
        self.client = pynite.Client(os.getenv('FNTOKEN'), timeout=5)

    @commands.command()
    @commands.cooldown(1, 6, commands.BucketType.user)
    async def solofortprofile(self, ctx, platform, name):
        '''Fetch a solo profile.'''

        player = await self.client.get_player(platform, name)
        solos = await player.get_solos()
        em = discord.Embed(color=discord.Color(value=passcolor))
        em.title = "Solo stats for user:"
        em.add_field(name="Victory Royales", value=solos.top1.value)
        em.add_field(name='Top 10', value=solos.top10.value)
        em.add_field(name='Top 25', value=solos.top25.value)
        em.add_field(name="Score", value=solos.score.value)
        em.add_field(name="K/D", value=solos.kd.value)
        em.add_field(name="Kills", value=solos.kills.value)
        em.add_field(name="Kills per Minute", value=solos.kpm.value)
        em.add_field(name="Kills per Match", value=solos.kpg.value)
        em.add_field(name="Matches Played", value=solos.matches.value)
        em.add_field(name="Minutes Played", value=solos.minutes_played.display_value)
        em.add_field(name="Average Match Time", value=solos.avg_time_played.display_value)

        em.set_footer(text="Brotat")
        await ctx.send(embed=em)
        
        
    @commands.command()
    @commands.cooldown(1, 6, commands.BucketType.user)
    async def duofortprofile(self, ctx, platform, name):
        '''Fetch a duo profile.'''

        player = await self.client.get_player(platform, name)
        duos = await player.get_duos()
        em = discord.Embed(color=discord.Color(value=passcolor))
        em.title = "Duo stats for user:"
        em.add_field(name="Victory Royales", value=duos.top1.value)
        em.add_field(name='Top 5', value=duos.top5.value)
        em.add_field(name='Top 10', value=duos.top10.value)
        em.add_field(name="Score", value=duos.score.value)
        em.add_field(name="K/D", value=duos.kd.value)
        em.add_field(name="Kills", value=duos.kills.value)
        em.add_field(name="Kills per Minute", value=duos.kpm.value)
        em.add_field(name="Kills per Match", value=duos.kpg.value)
        em.add_field(name="Matches Played", value=duos.matches.value)
        em.add_field(name="Minutes Played", value=duos.minutes_played.display_value)
        em.add_field(name="Average Match Time", value=duos.avg_time_played.display_value)

        em.set_footer(text="Brotat")
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Fortnite(bot))
