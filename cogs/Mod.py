import discord
from discord.ext import commands
from urllib.parse import urlparse
import datetime
import asyncio
import random
from ext import utils
import pip
import os
import io
import json
from utils.config import *


class Mod:
    '''
    Mod commands
    '''

    def __init__(self, bot):
        self.bot = bot


        
        # TODO: Add reason with ban
    @commands.has_permissions(ban_members=True)    
    @commands.command(aliases=['hban'], pass_context=True)     
    async def hackban(self, ctx, user_id: int):
        """Bans a user outside of the server."""
        author = ctx.message.author
        guild = author.guild

        user = guild.get_member(user_id)
        if user is not None:
            return await ctx.invoke(self.ban, user=user)

        try:
            await self.bot.http.ban(user_id, guild.id, 0)
            await ctx.message.edit(content=self.bot.bot_prefix + 'Banned user: %s' % user_id)
        except discord.NotFound:
            await ctx.message.edit(content=self.bot.bot_prefix + 'Could not find user. '
                               'Invalid user ID was provided.')
        except discord.errors.Forbidden:
            await ctx.message.edit(content=self.bot.bot_prefix + 'Could not ban user. Not enough permissions.')    
        
        
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, length: int, *, reason: str='No reason given.'):
        """Temporarily bans a member for a specified amount of time."""

        if length > 10000:
            return await ctx.send('Length of ban is too long.')

        guild = ctx.guild
        author = ctx.author

        try:
            invitation = await ctx.channel.create_invite(max_uses = 1, xkcd = True)
        except discord.HTTPException:
            return  # we couldn't create an invite, so don't ban.

        user_embed = discord.Embed()
        user_embed.color = 0xd60606
        user_embed.title = 'You have been banned!'
        user_embed.description = f'{author.name} has banned you.\n\nInvite: {invitation.url}\n' \
                                 f'After your ban time is up, click this link to rejoin the server.'
        user_embed.add_field(name='Reason', value=reason)
        user_embed.add_field(name='Length', value=f'{length} seconds')

        public_embed = discord.Embed()
        public_embed.color = 0xd60606
        public_embed.title = f'{member.name} has been banned!'
        public_embed.description = f'This member was banned by {author.name}.'
        public_embed.add_field(name='Reason', value=reason)
        public_embed.add_field(name='Length', value=f'{length} seconds')

        try:
            await ctx.send(embed=public_embed)
        except discord.HTTPException:
            pass  # couldn't send the public embed
        try:
            await member.send(embed=user_embed)
        except discord.HTTPException:
            return  # couldn't send the private message, so don't ban

        try:
            await member.ban(reason=reason, delete_message_days=0)
        except discord.HTTPException:
            return  # we couldn't ban them

        await asyncio.sleep(length)

        try:
            await member.unban(reason='Softban time expired.')
        except discord.HTTPException:
            pass  # we couldn't unban them



        


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason='No reason.'):
        '''Kick a member from the guild'''
        try:
            await ctx.guild.kick(user, reason=reason)
            await ctx.send(f"Kicked {user.name} from the server.")
        except discord.Forbidden:
            await ctx.send("I could not kick the user. Make sure I have the kick members permission.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason='No reason.'):
        '''Ban a member from the guild'''
        try:
            await ctx.guild.ban(user, reason=reason)
            await ctx.send(f"Banned {user.name} from the server.")
        except discord.Forbidden:
            await ctx.send("I could not ban the user. Make sure I have the ban members permission.")


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def mute(self, ctx, user: discord.Member):
        '''Mute a member in the channel'''
        try:
            await ctx.channel.set_permissions(user, send_messages=False)
            await ctx.channel.send(f"{user.mention} has been muted from this channel")
        except discord.Forbidden:
            await ctx.send("I could not unmute the user. Make sure I have the manage channels permission.")


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unmute(self, ctx, user: discord.Member):
        '''Unmute a member from the channel'''
        try:
            await ctx.channel.set_permissions(user, send_messages=True)
            await ctx.channel.send(f"{user.mention} has been unmuted from this channel.")
        except discord.Forbidden:
            await ctx.send("I could not unmute the user. Make sure I have the manage channels permission.")


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, user: discord.Member, *, reason: str):
        '''Warn a member via DMs'''
        warning = f"You have been warned in **{ctx.message.guild}** by **{ctx.message.author}** for {reason}"
        if not reason:
            warning = f"You have been warned in **{ctx.message.guild}** by **{ctx.message.author}**"
        await user.send(warning)
        await ctx.send(f"**{user}** has been **warned**")


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, messages: int):
        '''Delete messages'''
        if messages > 99:
            messages = 99

        try:
            await ctx.channel.purge(limit=messages + 1)
        except Exception as e:
            await ctx.send("I cannot delete the messages. Make sure I have the manage messages permission.")
        else:
            await ctx.send(f'{messages} messages deleted.', delete_after=3)



    @commands.command()
    async def addrole(self, ctx, member: discord.Member, *, rolename: str):
        '''Add a role to someone else.'''
        role = discord.utils.find(lambda m: rolename.lower() in m.name.lower(), ctx.message.guild.roles)
        if not role:
            return await ctx.send('That role does not exist.')
        try:
            await member.add_roles(role)
            await ctx.send(f'Added: `{role.name}`')
        except:
            await ctx.send("I don't have the perms to add that role.")


    @commands.command()
    async def removerole(self, ctx, member: discord.Member, *, rolename: str):
        '''Remove a role from someone else.'''
        role = discord.utils.find(lambda m: rolename.lower() in m.name.lower(), ctx.message.guild.roles)
        if not role:
            return await ctx.send('That role does not exist.')
        try:
            await member.remove_roles(role)
            await ctx.send(f'Removed: `{role.name}`')
        except:
            await ctx.send("I don't have the perms to add that role.")


# Setup bot
def setup(bot):
    bot.add_cog(Mod(bot))
