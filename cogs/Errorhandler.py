import discord
import time
import datetime
from discord.ext.commands import errors
from utils.config import *
from discord.ext import commands
import traceback
import sys

class ErrorHandler:
	def __init__(self, bot):
		self.bot = bot

	async def is_on_cooldown(self, ctx, error):
                        if isinstance(err, errors.CommandOnCooldown):
                               await ctx.send(f"This command is on cooldown... try again in {err.retry_after:.0f} seconds.")

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
