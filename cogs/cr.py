import discord
import sys
import os
from utils.config import *
import io
import clashroyale
from ext import utils
from discord.ext import commands


class cr:
    '''
    Get information about a Clashroyale user
    '''
    def __init__(self, bot):
        self.bot = bot
        self.client = clashroyale.Client("49c21c37d3da47ea89deaa90528322730c4343230e6b4184a707af262d386d74", is_async=True)
        

    @commands.command()
    async def crprofile(self, ctx, crtag:str):
        """Shows CR stats for you! Usage: %profile [tag]"""
        if crtag is None:
            await ctx.send('Please enter your tag. Usage: %profile [tag].') # Bot hosts on Heroku, which means there is no save tag feature (Heroku deletes data every day.)
        else:
            try:
                profile = await self.client.get_player(crtag)
            except (clashroyale.errors.NotResponding, clashroyale.errors.ServerError) as e:
                color = discord.Color(value=failcolor)
                em = discord.Embed(color=color, title='Some idiot is spamming the api please wait')
                em.description = 'Error code **{e.code}**: {e.error}'
                return await ctx.send(embed=em)
            color = discord.Color(value=passcolor)
            em = discord.Embed(color=color, title=f'{profile.name} ({profile.tag})')
            em.add_field(name='Trophies', value=f'{profile.trophies}')
            em.add_field(name='Personal Best', value=f'{profile.stats.max_trophies}')
            em.add_field(name='XP Level', value=f'{profile.stats.level}')
            em.add_field(name='Arena', value=f'{profile.arena.name}')
            em.add_field(name='Wins/Losses/Draws', value=f'{profile.games.wins}/{profile.games.draws}/{profile.games.losses}')
            em.add_field(name='Win Rate', value=f'{(profile.games.wins / (profile.games.wins + profile.games.losses) * 100):.3f}%')
            em.add_field(name='Favorite Card', value=f'{profile.stats.favorite_card.name}')                                                                                                                                                 
            em.set_author(name=f'Users stats')
            em.set_thumbnail(url=f'https://cr-api.github.io/cr-api-assets/arenas/arena{profile.arena.arenaID}.png') # This allows thumbnail to match your arena! Maybe it IS possible after all...
            await ctx.send(embed=em)
            profile = await self.client.get_player(crtag)
            try:
                clan = await profile.get_clan()
            except:
                pass
            color = discord.Color(value=passcolor)
            if profile.clan.role:
                em = discord.Embed(color=color, title='Clan')
                em.description = f'{clan.name} (#{clan.tag})'
                em.add_field(name='Role', value=f'{profile.clan.role}')                                                                                                                                                                      
                em.add_field(name='Clan Score', value=f'{clan.score}')
                em.add_field(name='Members', value=f'{len(clan.members)}/50')
                em.set_thumbnail(url=clan.badge.image)
                await ctx.send(embed=em)
            else:
                em.description = 'No Clan'
                em.set_thumbnail(url='http://i1253.photobucket.com/albums/hh599/bananaboy21/maxresdefault_zpseuid4jln.jpg') # This is the url for the No Clan symbol.
                em.set_footer(text='API: cr-api.com', icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')
                await ctx.send(embed=em)
            profile = await self.client.get_player(crtag)
            color = discord.Color(value=passcolor)
            em = discord.Embed(color=color)
            em.add_field(name='Challenge Max Wins', value=f'{profile.stats.challenge_max_wins}')
            em.add_field(name='Challenge Cards Won', value=f'{profile.stats.challenge_cards_won}')
            em.add_field(name='Tourney Cards Won', value=f'{profile.stats.tournament_cards_won}')
            em.set_author(name='Challenge/Tourney Stats')
            em.set_thumbnail(url='http://vignette4.wikia.nocookie.net/clashroyale/images/a/a7/TournamentIcon.png/revision/latest?cb=20160704151823')
            em.set_footer(text='cr-api.com', icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')
            await ctx.send(embed=em)


    @commands.command()
    async def crclan(self, ctx, clantag:str):
        """Shows info for a clan. Usage: %clan [CLAN TAG]"""
        if clantag is None:
            return await ctx.send('Please enter a valid clan tag. Usage: %clan [clan tag]')
        else:
            try:
                clan = await self.client.get_clan(clantag)
            except (clashroyale.errors.NotResponding, clashroyale.errors.ServerError) as e:
                color = discord.Color(value=failcolor)
                em = discord.Embed(color=color, title='Some idiot is spamming the api please wait.')
                em.description = 'Error code **{e.code}**: {e.error}'
                return await ctx.send(embed=em)
            color = discord.Color(value=passcolor)
            em = discord.Embed(color=color, title=f'{clan.name}')
            em.description = f'{clan.description}'
            em.add_field(name='Clan Trophies', value=f'{clan.score}')
            em.add_field(name='Members', value=f'{clan.memberCount}/50')
            em.add_field(name='Type', value=f'{clan.type}')
            em.add_field(name='Weekly Donations', value=f'{clan.donations}')
            em.add_field(name='Location', value=f'{clan.location.name}')
            if clan.clan_chest.status == 'inactive':
                tier = "Inactive"
            else:
                crowns = 0
                for m in clan.members:
                    crowns += m.clan_chest_crowns
                if crowns < 70:
                    tier = "0/10"
                if crowns > 70 and crowns < 160:
                    tier = "1/10"
                if crowns > 160 and crowns < 270:
                    tier = "2/10"
                if crowns > 270 and crowns < 400:
                    tier = "3/10"
                if crowns > 400 and crowns < 550:
                    tier = "4/10"
                if crowns > 550 and crowns < 720:
                    tier = "5/10"
                if crowns > 720 and crowns < 910:
                    tier = "6/10"
                if crowns > 910 and crowns < 1120:
                    tier = "7/10"
                if crowns > 1120 and crowns < 1350:
                    tier = "8/10"
                if crowns > 1350 and crowns < 1600:
                    tier = "9/10"
                if crowns == 1600:
                    tier = "10/10"
            em.add_field(name='Clan Chest Tier', value=f'{tier}')
            em.add_field(name='Trophy Requirement', value=f'{clan.requiredScore}')
            em.set_author(name=f'#{clan.tag}')
            em.set_thumbnail(url=f'{clan.badge.image}')
            em.set_footer(text='cr-api.com', icon_url='http://cr-api.com/static/img/branding/cr-api-logo.png')
            await ctx.send(embed=em)



        

def setup(bot): 
    bot.add_cog(cr(bot)) 
