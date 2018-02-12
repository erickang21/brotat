import discord
import random
from discord.ext import commands
import datetime
import pytz
from utils.config import *
import inspect



class Math:
    '''Math commands'''

    def __init__(self, bot):
        self.bot = bot



#main command
    @commands.group(invoke_without_command=True)
    async def math(self, ctx):
        '''A command group for math commands'''
        await ctx.send('Available commands:\n`add <a> <b>`\n`subtract <a> <b>`\n`multiply <a> <b>`\n`divide <a> <b>`\n`remainder <a> <b>`\n`power <a> <b>`\n`factorial <a>`')



#multiply command
    @math.command(aliases=['*', 'x'])
    async def multiply(self, ctx, a: int, b: int):
        '''Multiply two numbers'''
        em = discord.Embed(color=passcolor)
        em.title = "Result"
        em.description = f'❓ Problem: `{a}*{b}`\n✅ Solution: `{a * b}`'
        await ctx.send(embed=em)



#divide command
    @math.command(aliases=['/', '÷'])
    async def divide(self, ctx, a: int, b: int):
        '''Divide a number by a number'''
        try:
            em = discord.Embed(color=passcolor)
            em.title = "Result"
            em.description = f'❓ Problem: `{a}/{b}`\n✅ Solution: `{a / b}`'
            await ctx.send(embed=em)
        except ZeroDivisionError:
            em = discord.Embed(color=failcolor)
            em.title = "Error"
            em.description = "You can't divide by zero"
            await ctx.send(embed=em)



#add command
    @math.command(aliases=['+'])
    async def add(self, ctx, a: int, b: int):
        '''Add a number to a number'''
        em = discord.Embed(color=passcolor)
        em.title = "Result"
        em.description = f'❓ Problem: `{a}+{b}`\n✅ Solution: `{a + b}`'
        await ctx.send(embed=em)



#subtract command
    @math.command(aliases=['-'])
    async def subtract(self, ctx, a: int, b: int):
        '''Substract two numbers'''
        em = discord.Embed(color=passcolor)
        em.title = "Result"
        em.description = f'❓ Problem: `{a}-{b}`\n✅ Solution: `{a - b}`'
        await ctx.send(embed=em)



#remainder command
    @math.command(aliases=['%'])
    async def remainder(self, ctx, a: int, b: int):
        '''Gets a remainder'''
        em = discord.Embed(color=passcolor)
        em.title = "Result"
        em.description = f'❓ Problem: `{a}%{b}`\n✅ Solution: `{a % b}`'
        await ctx.send(embed=em)



#power command
    @math.command(aliases=['^', '**'])
    async def power(self, ctx, a: int, b: int):
        '''Raise A to the power of B'''
        if a > 100 or b > 100:
            return await ctx.send("Numbers are too large.")
        em = discord.Embed(color=discord.Color.green())
        em.title = "Result"
        em.description = f'❓ Problem: `{a}^{b}`\n✅ Solution: `{a ** b}`'
        await ctx.send(embed=em)


#factorial command
    @math.command(aliases=['!'])
    async def factorial(self, ctx, a: int):
        '''Factorial something'''
        if a > 813:
            await ctx.send("That number is too high to fit within the message limit for discord.")
        else:
            em = discord.Embed(color=passcolor)
            em.title = "Result"
            result = 1
            problem = a
            while a > 0:
                result = result * a
                a = a - 1
            em.description = f'❓ Problem: `{problem}!`\n✅ Solution: `{result}`'
            await ctx.send(embed=em)





def setup(bot):
    bot.add_cog(Math(bot))

