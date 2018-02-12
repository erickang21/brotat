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
from xml.etree import ElementTree
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


class NSFW:
    '''
    NSFW commands :wink:
    '''
    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ass(self, ctx):
        '''Get random asses from the internet'''
        if not ctx.channel.is_nsfw():
          await ctx.send("**This is not a NSFW channel**")
          return
        """Random butts!"""
        api_base = 'http://api.obutts.ru/butts/'
        number = random.randint(1, 4296)
        url_api = api_base + str(number)
        async with aiohttp.ClientSession() as session:
            async with session.get(url_api) as data:
                data = await data.json()
                data = data[0]
        image_url = 'http://media.obutts.ru/' + data['preview']
        em = discord.Embed(color=passcolor)
        em.set_author(name="Random NSFW Image")
        em.set_image(url=image_url)
        em.set_footer(text=f"Requested by {ctx.message.author.name}")
        await ctx.send(embed=em)

	


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def boobs(self, ctx):
        '''Get random boobs from the internet'''
        if not ctx.channel.is_nsfw():
          await ctx.send("**This is not a NSFW channel**")
          return
        """Random"""
        api_base = 'http://api.oboobs.ru/boobs/'
        number = random.randint(1, 10303)
        url_api = api_base + str(number)
        async with aiohttp.ClientSession() as session:
           async with session.get(url_api) as data:
                data = await data.json()
                data = data[0]
        image_url = 'http://media.oboobs.ru/' + data['preview']
        em = discord.Embed(color=passcolor)
        em.set_author(name="Random image")
        em.set_image(url=image_url)
        em.set_footer(text=f"Requested by {ctx.message.author.name}")
        await ctx.send(embed=em)
	
def setup(bot): 
    bot.add_cog(NSFW(bot)) 
