import discord
from utils.config import *
from discord.ext import commands
from ext import utils

def to_emoji(c):
    base = 0x1f1e6
    return chr(base + c)

class Poll:
    """Poll voting system."""

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def poll(self, ctx, *questions_and_choices: str):
        """Makes a poll quickly.
        Put your question and answers in ""
        """

        if len(questions_and_choices) < 3:
            return await ctx.send('Need at least 1 question with 2 choices.')
        elif len(questions_and_choices) > 21:
            return await ctx.send('You can only have up to 20 choices.')

        perms = ctx.channel.permissions_for(ctx.me)
        if not (perms.read_message_history or perms.add_reactions):
            return await ctx.send('Need Read Message History and Add Reactions permissions.')

        question = questions_and_choices[0]
        choices = [(to_emoji(e), v) for e, v in enumerate(questions_and_choices[1:])]

        try:
            await ctx.message.delete()
        except:
            pass

        body = "\n".join(f"{key}: {c}" for key, c in choices)
        embed = discord.Embed(title = f"**{ctx.author.name}** asks: ", description = f"{question}", color = passcolor)
        embed.add_field(name = "Answers:", value = f"{body}")
        embed.set_thumbnail(url = ctx.author.avatar_url)
        poll = await ctx.send(embed = embed)

        #poll = await ctx.send(f'{ctx.author} asks: {question}\n\n{body}')
        for emoji, _ in choices:
            await poll.add_reaction(emoji)

def setup(bot):
    bot.add_cog(Poll(bot))
