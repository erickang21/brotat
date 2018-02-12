import discord
import unicodedata
from discord.ext import commands
import time
import datetime
import requests
import ftfy
import traceback
import sys
import copy
import asyncio
import os
import urllib.parse
from urllib.request import urlopen
import aiohttp
from discord.ext.commands import TextChannelConverter
from ext.paginator import PaginatorSession
from ext import embedtobox
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
from pyfiglet import figlet_format as ascii_format
from collections import Counter
from ext import utils


class Owner:
    '''
    More owner commands
    '''
    def __init__(self, bot):
        self.bot = bot
        

    @commands.cooldown(1, 600, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(pass_context = True)
    async def ctdev(self, ctx, *, pmessage : str = None):
        """Contact the dev"""
        invite = await ctx.channel.create_invite(max_uses = 1, xkcd = True)
        dev = self.bot.get_user(293159670040887297)

        if pmessage == None:
            embed = discord.Embed(description = f"**{ctx.author.name}**, my developers need to know something. Type a feedback!", color = failcolor)
            message = await ctx.send(embed = embed)
            await message.edit(delete_after = 15)

        else:
            try:
                embed = discord.Embed(colour = passcolor)
                embed.set_thumbnail(url = f"{ctx.author.avatar_url}")
                embed.add_field(name = f"Information: ", value = f"Name: **{ctx.author.name}**\nID: **{ctx.author.id}**\nServer: [**{ctx.guild}**]({invite.url})", inline = False)
                embed.add_field(name = f"Feedback/Message: ", value = f"{pmessage}", inline = False)
                await dev.send(embed = embed)
                embed = discord.Embed(description = f"I have sent a message to my developer with your feedback! Thank you for your help!", color = passcolor)
                await ctx.send(embed = embed)
            except discord.Forbidden:
                embed = discord.Embed(color = failcolor)
                embed.add_field(name = "Oops, something went wrong!", value = f"**{ctx.author.name}**, I'm not allowed to do this!", inline = False)
                await ctx.send(embed = embed)    
        


    

    @commands.command(hidden=True, name = 'shutdown')
    async def _shutdown(self, ctx):
       '''Shutdown brotat'''
       if ctx.message.author.id == owner_id:
        reply = await ctx.send(f"<:Brotat:> | **{ctx.author.name}** you sure you wanna shut down **{self.bot.user.name}**?")
        await reply.add_reaction('✅')
        await reply.add_reaction('🔄')
        await reply.add_reaction('🅾')

        def pred(reaction, user):
            return user == ctx.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '🔄' or str(reaction.emoji) == '🅾')

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=pred)
        except asyncio.TimeoutError:
                await reply.delete()
                await ctx.message.delete()
                await ctx.send(f"<:Brotat:> | **{self.bot.user.name}**'s shutdown has ben cancled!")
        else:
            if str(reaction.emoji) == '✅':
                await reply.delete()
                await ctx.send(f"<:Brotat:> | **{self.bot.user.name}** is succesfully shutted down!")
                await ctx.message.delete()
                await self.bot.logout()

            elif str(reaction.emoji) == '🔄':
                await reply.delete()
                await ctx.send(f"<:Brotat:> | **{self.bot.user.name}** is rebooting, one moment please!")
                await ctx.message.delete()
                os.execve(sys.executable, ['python'] + sys.argv, os.environ)

            elif str(reaction.emoji) == '🅾':
                await reply.delete()
                await ctx.message.delete()
                await ctx.send(f"<:Brotat:> | **{self.bot.user.name}**'s shutdown has ben cancled!")

    
    @commands.is_owner()
    @commands.command(hidden=True, name = 'source')
    async def _source(self, ctx, *, command:str):
        source = str(inspect.getsource(self.bot.get_command(command).callback))
        fmt = 'py\n'+source.replace('', '\u200b') + '\n'
        await ctx.send(fmt)

    @commands.is_owner()    
    @commands.command(hidden=True, name = 'source')
    async def _source(self, ctx, *, command:str):
        source = str(inspect.getsource(self.bot.get_command(command).callback))
        fmt = '```py\n'+source.replace('`', '\u200b') + '\n```'
        await ctx.send(fmt)
                
def setup(bot):
    bot.add_cog(Owner(bot))
