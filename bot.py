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



bot = commands.Bot(command_prefix=os.environ.get('pr!'),owner_id=293159670040887297)  # Bots prefix



startTime = time.time()

startup_extensions = [

    'cogs.Owner',
    'cogs.Mod',
    'cogs.Errorhandler',
    'cogs.botsorgapi',
    'cogs.poll',
    'cogs.Utility',
    'cogs.help',
    'cogs.cr',
    'cogs.Admin',
    'cogs.Fortnite',
    'cogs.NSFW',
    'cogs.Info',
    'cogs.Math',
    'cogs.botlistapi',
    'cogs.Pokemon',
    'cogs.Meme'
]



bot.remove_command('help')

dbltoken = "os.environ.get('DBLTOKEN')"

directory = 'cogs'

def cleanup_code(content):
    '''Automatically removes code blocks from the code.'''
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    return content.strip('` \n')
     
	
#dont add any more commands above this



@bot.command()
async def uptime(ctx):
        second = time.time() - startTime
        minute, second = divmod(second, 60)
        hour, minute = divmod(minute, 60)
        day, hour = divmod(hour, 24)
        week, day = divmod(day, 7)
        await ctx.send("I've been online for %d weeks, %d days, %d hours, %d minutes, %d seconds" % (week, day, hour, minute, second))




#@bot.event
#async def on_guild_join(guild):
 #   lol = bot.get_channel(399549588341522443)
 #   em = discord.Embed(color=discord.Color(value=passcolor))
 #   em.title = "New server!"
 #   em.description = f"Server: {guild}"
 #   await lol.send(embed=em)
 #   await ctx.send(f".")

@bot.event
async def on_command(ctx):
    lol = bot.get_channel(392104491438309382)
    colour = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
    colour = int(colour, 16)
    embed = discord.Embed(title = "Command Executed!", colour = discord.Colour(value = colour), timestamp = datetime.datetime.utcnow())
    embed.add_field(name = "Server", value = ctx.guild, inline = True)
    embed.add_field(name = "Channel", value = ctx.message.channel.name, inline = True)
    embed.add_field(name = "Author", value = ctx.message.author.name)
    embed.add_field(name = "Content", value = "```{}```".format(ctx.message.clean_content))
    await lol.send(embed = embed)
	
	

	
	
	
@bot.command(aliases=['trump', 'trumpquote'])
async def asktrump(ctx, *, question):
        '''Ask Donald Trump a question! Usage: {p}asktrump <yourquestion>'''
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.whatdoestrumpthink.com/api/v1/quotes/personalized?q={question}') as resp:
                file = await resp.json()
                quote = file['message']
                em = discord.Embed(color=discord.Color(value=passcolor))
                em.title = "What does Trump say?"
                em.description = quote
                em.set_footer(text="Brotat")
                await ctx.send(embed=em)
	

@commands.guild_only()
@bot.command(aliases=['osu'])
async def osustats(ctx, *, osuplayer : str = None):

		if osuplayer == None:
			embed = discord.Embed(description = "**"+ ctx.author.name +"** you need to tell me a username!", color = failcolor)
			await ctx.send(embed = embed)

		else:
			#embed.set_thumbnail(url = ctx.author.avatar_url)
			embed = discord.Embed(color = passcolor)
			embed.set_author(name = f"{osuplayer}'s Stats", url = f"https://osu.ppy.sh/u/{osuplayer}", icon_url = "https://s.ppy.sh/images/head-logo.png")
			embed.set_footer(text = "Brotat")
			embed.set_image(url = f"http://lemmmy.pw/osusig/sig.php?colour=hexff66aa&uname={osuplayer}&pp=1&countryrank&flagshadow&flagstroke&opaqueavatar&avatarrounding=5&onlineindicator=undefined&xpbar&xpbarhex")
			await ctx.send(embed = embed)

	
@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command()
async def mathfact(ctx, number: int):
        '''Get a math fact about a number. Usage: {p}mathfact <number>.'''
        if not number:
            await ctx.send(f'Usage: `{ctx.prefix}mathfact <number>`')
            return
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://numbersapi.com/{number}/math?json') as resp:
                    file = await resp.json()
                    fact = file['text']
                    await ctx.send(f"**Did you know?**\n*{fact}*")
        except:
            await ctx.send("No facts are available for that number.")

@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command()
async def comic(ctx):
        '''Get a comic'''
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://xkcd.com/info.0.json') as resp:
                data = await resp.json()
                currentcomic = data['num']
        rand = random.randint(0, currentcomic)  # max = current comic
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://xkcd.com/{rand}/info.0.json') as resp:
                data = await resp.json()
                em = discord.Embed(color=discord.Color(value=0x00ff00))
                em.title = f"XKCD Number {data['num']}- \"{data['title']}\""
                em.set_footer(text=f"Published on {data['month']}/{data['day']}/{data['year']}")
                em.set_image(url=data['img'])
                await ctx.send(embed=em)


@bot.command(name='presence', hidden=True)
@commands.is_owner()
async def _presence(ctx, type=None, *, game=None):
    '''Change the bot's presence'''
    if type is None:
        await ctx.send(f'Usage: `{ctx.prefix}presence [game/stream/watch/listen] [message]`')
    else:
        if type.lower() == 'stream':
            await bot.change_presence(game=discord.Game(name=game, type=1, url='https://www.twitch.tv/batshal'), status='online')
            await ctx.send(f'Set presence to. `Streaming {game}`')
        elif type.lower() == 'game':
            await bot.change_presence(game=discord.Game(name=game))
            await ctx.send(f'Set presence to `Playing {game}`')
        elif type.lower() == 'watch':
            await bot.change_presence(game=discord.Game(name=game, type=3), afk=True)
            await ctx.send(f'Set presence to `Watching {game}`')
        elif type.lower() == 'listen':
            await bot.change_presence(game=discord.Game(name=game, type=2), afk=True)
            await ctx.send(f'Set presence to `Listening to {game}`')
        elif type.lower() == 'clear':
            await bot.change_presence(game=None)
            await ctx.send('Cleared Presence')
        else:
            await ctx.send('Usage: `%presence [game/stream/watch/listen] [message]`')



	
	
@bot.command(hidden=True, name='eval')
@commands.is_owner()
async def _eval(ctx, *, body: str):
    '''Evaluate python code'''
    
    env = {
        'bot': bot,
        'ctx': ctx,
        'channel': ctx.channel,
        'author': ctx.author,
        'guild': ctx.guild,
        'message': ctx.message,
    }

    env.update(globals())

    body = cleanup_code(body)
    stdout = io.StringIO()

    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

    try:
        exec(to_compile, env)
    except Exception as e:
        return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        try:
            await ctx.message.add_reaction('\u2705')
        except:
            pass

        if ret is None:
            if value:
                await ctx.send(f'```py\n{value}\n```')
        else:
            await ctx.send(f'```py\n{value}{ret}\n```')

		
		
@bot.command(aliases=['about'])
async def info(ctx):
		RAM = psutil.virtual_memory()
		used = RAM.used >> 20
		percent = RAM.percent
		CPU  = psutil.cpu_percent()
		embed = discord.Embed(title="Brotat info", color=passcolor, timestamp=ctx.message.created_at)
		embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
		embed.add_field(name="Author", value="AndroidUpdated")
		embed.add_field(name="Servers", value=len(bot.guilds))
		embed.add_field(name="Memory", value=f'{percent}% ({used}MB)')
		embed.add_field(name="CPU", value=f"{CPU}%")
		embed.add_field(name='Operating system', value=platform.system())
		embed.add_field(name="Bot Latency", value=f"{bot.ws.latency * 1000:.3f} ms")
		embed.add_field(name="Invite", value=f"[Click Here](https://discordapp.com/oauth2/authorize?client_id=371320386693890048&scope=bot&permissions=2146958591)")
		embed.add_field(name="Upvote this bot!", value=f"[Click here](https://discordbots.org/bot/{bot.user.id}) :robot:")
		embed.set_footer(text='Powered by discord.py v.1.0.0a')
		await ctx.send(embed=embed)

		
		



@commands.is_owner()
@bot.command(aliases=['ol'])
async def ownerlist(ctx):
        """Shows a list of all servers using paginator"""
        for guild in bot.guilds:
            guilds = [f"**{guild.name}** \nServer Owner: **{guild.owner.name}#{guild.owner.discriminator}**\nServer ID: **{guild.id}**\nTotal Members: **{guild.member_count}**" for guild in bot.guilds]
        try:
            p = Pages(ctx, entries=guilds, per_page=5)
            p.embed.colour = passcolor
            await p.paginate()
        except Exception as e:
            await ctx.send(e)

@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def textmojify(ctx, *, msg):
        """Convert text into emojis"""
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass

        if msg != None:
            out = msg.lower()
            text = out.replace(' ', '    ').replace('10', '\u200B:keycap_ten:')\
                      .replace('ab', '\u200B🆎').replace('cl', '\u200B🆑')\
                      .replace('0', '\u200B:zero:').replace('1', '\u200B:one:')\
                      .replace('2', '\u200B:two:').replace('3', '\u200B:three:')\
                      .replace('4', '\u200B:four:').replace('5', '\u200B:five:')\
                      .replace('6', '\u200B:six:').replace('7', '\u200B:seven:')\
                      .replace('8', '\u200B:eight:').replace('9', '\u200B:nine:')\
                      .replace('!', '\u200B❗').replace('?', '\u200B❓')\
                      .replace('vs', '\u200B🆚').replace('.', '\u200B🔸')\
                      .replace(',', '🔻').replace('a', '\u200B🅰')\
                      .replace('b', '\u200B🅱').replace('c', '\u200B🇨')\
                      .replace('d', '\u200B🇩').replace('e', '\u200B🇪')\
                      .replace('f', '\u200B🇫').replace('g', '\u200B🇬')\
                      .replace('h', '\u200B🇭').replace('i', '\u200B🇮')\
                      .replace('j', '\u200B🇯').replace('k', '\u200B🇰')\
                      .replace('l', '\u200B🇱').replace('m', '\u200B🇲')\
                      .replace('n', '\u200B🇳').replace('ñ', '\u200B🇳')\
                      .replace('o', '\u200B🅾').replace('p', '\u200B🅿')\
                      .replace('q', '\u200B🇶').replace('r', '\u200B🇷')\
                      .replace('s', '\u200B🇸').replace('t', '\u200B🇹')\
                      .replace('u', '\u200B🇺').replace('v', '\u200B🇻')\
                      .replace('w', '\u200B🇼').replace('x', '\u200B🇽')\
                      .replace('y', '\u200B🇾').replace('z', '\u200B🇿')
            try:
                await ctx.send(text)
            except Exception as e:
                await ctx.send(f'```{e}```')
        else:
            await ctx.send('Write something, reee!', delete_after=3.0)


    

@bot.command(pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def echo(ctx, *, echo: str):
        '''Speaks for you'''
        if echo.__contains__("@everyone") or echo.__contains__("@here"):
            try:
                await ctx.message.delete()
            except: pass
            await ctx.send(f"{ctx.author.mention}, Really ? You think you're smart enough to fool me ? :smirk:")
            return
        else:
            try:
                await ctx.message.delete()
            except:
                pass
            await ctx.send(echo)



		

  
		
    
@bot.event
async def on_guild_remove(g):
    await bot.change_presence(game=discord.Game(name=f"{len(bot.guilds)} servers! | %help", type=3), afk=True)

@bot.event
async def on_guild_join(g):
    success = False
    i = 0
    while not success:
        try:
            await g.channels[i].send(f"Hello! Thanks for inviting me to your server. My prefix is '%'. If you have a suggestion please use the command '%ctdev'! You can also upvote me here https://discordbots.org/bot/371320386693890048. Thank you")
        except (discord.Forbidden, AttributeError):
            i += 1
        except IndexError:
            # if the server has no channels, doesn't let the bot talk, or all vc/categories
            pass
        else:
            success = True
    await bot.change_presence(game=discord.Game(name=f"{len(bot.guilds)} servers! | %help", type=3), afk=True)
    

@bot.command(pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def cat(ctx):
    '''Get a random cat pic'''
    r = requests.get('https://random.cat/meow')
    cat = str(r.json()['file'])
    embed = discord.Embed(title = "Purr.", description = "Here is your cat.", color = 0x00ff44)
   # embed.set_thumbnail(url = cat)
    embed.set_author(name = "Random cat")
    embed.set_image(url = cat)
    embed.set_footer(text = "| Brotat |")
    await ctx.send(embed = embed)

    
    
        
@bot.command()
async def ping(ctx):
    '''Pong! Get the bot's response time'''
    em = discord.Embed(color=discord.Color(value=0x00ff00))
    em.title = "Pong!"
    em.description = f'{bot.ws.latency * 1000:.4f} ms'
    await ctx.send(embed=em)
    

@bot.event
async def on_ready():
        """Shows bot's status"""
        print("----------------")
        print("Logged in as:")
        print("Name : {}".format(bot.user.name))
        print("ID : {}".format(bot.user.id))
        print("Py Lib Version: %s"%discord.__version__)
        print("made by AndroidUpdated")
        print("----------------")
	#server = len(bot.guilds)
        #users = sum(1 for _ in bot.get_all_members()
        #while 1==1:
            #await bot.change_presence(game=discord.Game(name='with {} servers'.format(server)))
            #await asyncio.sleep(20)
            #await bot.change_presence(game=discord.Game(name='with {} users'.format(users)))
            #await asyncio.sleep(20)                         
            #await bot.change_presence(game=discord.Game(name='PREFIX = %'))
            #await asyncio.sleep(20)
            #await bot.change_presence(game=discord.Game(name='Version 6.5'))
            #await asyncio.sleep(20)
            #await bot.change_presence(game=discord.Game(name='%help | %invite'))
            #await asyncio.sleep(25)
	
@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name=f"{len(bot.guilds)} servers! | %help", type=3), afk=True)	

	
     
    
@bot.command()
async def invite(ctx):
        embed = discord.Embed(description="Links", color=passcolor)
        embed.set_thumbnail(url=bot_icon)
        embed.add_field(name="__Bot Invite__",
                        value="Click [here](https://discordapp.com/oauth2/authorize?client_id=371320386693890048&scope=bot&permissions=2146958591) to invite the bot and join https://discord.gg/fxFcH4p")
        await ctx.send(embed=embed)
        
        

        

	
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
            print('Loaded extension: {}'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

if not os.environ.get('TOKEN'):
    print("no token found!")
bot.run(os.environ.get('TOKEN').strip('"'))
