# bot.py
import os

import discord
from discord.ext.tasks import loop
from discord.ext import commands
from dotenv import load_dotenv
import sqlite3
import configparser
import randombuild as rabu
import time

bot = commands.Bot(command_prefix='!')

verbindung = sqlite3.connect("user.db")


x = 0
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()

client = discord.Client(intents=intents)


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    user = message.author
    user = str(user)

    if '!searchbuild' in message.content and message.channel.id == 902488846699204639:
        mssg = message.content[13:]

        builds = rabu.findinbuilds(mssg)
        if builds:
            i = 0
            for build in builds:
                if i < 10:
                    i += 1
                    print(f"{i} - {build}")
                    await message.channel.send(f'Build: {build}')
                    time.sleep(2)
        else:
            await message.channel.send("Kein Build gefunden")

    if '!randombuild' in message.content and message.channel.id == 902488846699204639:
        build = rabu.printrandom()

        await message.channel.send(f'Dein Build: {build[0]} Link: {build[1]}')

    if '!pob' in message.content and message.channel.id == 902488846699204639:
        await message.channel.send('https://github.com/PathOfBuildingCommunity/PathOfBuilding/releases')

    if '!lootfilter' in message.content and message.channel.id == 902488846699204639:
        await message.channel.send('Theddys Lootfilter: http://e.pc.cd/v1sotalK')

    if '!poe' in message.content and message.channel.id == 902488846699204639:
        user = message.author
        await user.send("Tradeseiten: https://poe.trade/ ODER https://www.pathofexile.com/trade/search/Scourge // Aktuelle Season: https://www.pathofexile.com/scourge // Offizielles PoE-Wiki: https://pathofexile.fandom.com/wiki/Path_of_Exile_Wiki // PoE-Ninja (Preisvergleich, Gegenwert von Items, Leader): https://poe.ninja/ // PoE Builds: https://www.poebuilds.cc/ ODER https://www.poe-vault.com/guides/builds-for-path-of-exile // Custom-PoE-Filter: https://www.filterblade.xyz/")


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Watching You'))

    print(f'{client.user.name} has connected to Discord!')
    


if __name__ == "__main__":
    client.run(TOKEN)
