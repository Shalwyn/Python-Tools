from twitchio.ext import commands
from twitchio.ext import routines
import twitchio.ext
import randombuild as rabu
import time
import sys
import os
import sqlite3

oauth_token = '0i1779csd0iy4esvpthmemrttjcl3e'
client_id = 'gp762nuuoqcoxypju8c569th9wz7q5'

bot_account = 'shalorabot'
channel_name = 'shalora_'


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=oauth_token,
            client_id=client_id,
            nick=bot_account,
            prefix='!',
            initial_channels=["shalora_", "theddy"]
        )

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...

        print(f'Logged in as | {self.nick}')
        

    #async def event_message(self, message):
        #if 'Poe' in message.content and 'Deutsch' in message.content:
        #    await message.channel.send("Deutsche Sprachkurse bei Babbel")

        #if 'Hc' in message.content or 'HC' in message.content:
        #    await message.channel.send("Wenn du Tier 4 Subst")

        #await self.handle_commands(message)    

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Send a hello back!
       
        await ctx.send(f'Hello {ctx.author.name}!')

    @commands.command()
    async def beginner(self, ctx: commands.Context):
        # Send a hello back!
       
        await ctx.send(f'Meine empfehlung für euch zum start: https://www.pathofexile.com/forum/view-thread/1147951')

    

    @commands.command()
    async def randombuild(self, ctx: commands.Context):

        build = rabu.printrandom()

        name = ctx.message.author.name

        await ctx.send(f'@{name} Dein Build: {build[0]} Link: {build[1]}')

    @commands.command()
    async def pob(self, ctx: commands.Context):
        await ctx.send('https://github.com/PathOfBuildingCommunity/PathOfBuilding/releases')

    @commands.command()
    async def lootfilter(self, ctx: commands.Context):
        await ctx.send('Theddys Lootfilter: https://drive.google.com/file/d/1uYyoqa8kD1wIU-beuKESVfTZ2JR2zTc0/view?usp=sharing')

    @commands.command()
    async def spannend(self, ctx: commands.Context):
       
        await ctx.send(f'https://clips.twitch.tv/ComfortableOpenArtichokeArsonNoSexy-anh5dLsu1Nq9TJjJ')

    @commands.command()
    async def archnemesis(self, ctx: commands.Context):
       
        await ctx.send(f'2 Cheatcheets für euch: https://craniumviolence.github.io | https://docs.google.com/spreadsheets/d/1RExTa_kBynzy2lExu-SohN5eYnqr9KZ_hpyrcxphm3M/edit#gid=0')

    @commands.command()
    async def kill(self, ctx: commands.Context):
        user = ctx.message.author
        if user.is_mod:
            sys.exit()

    @commands.command()
    async def death(self, ctx: commands.Context):
        user = ctx.message.author
        if user.is_mod:
            bundle_dir = os.path.dirname(os.path.abspath(__file__))
            getpath = os.path.join(bundle_dir, 'death.db')
            disk_db = sqlite3.connect(getpath)

            cursor = disk_db.cursor()
            exucute = f'SELECT * FROM death'
            cursor.execute(exucute)
            zeilen = cursor.fetchall()
            
            for zeile in zeilen:
            
                death = zeile[0]
                death += 1
                exucutes = f'update death set count = {death}'
                
                cursor.execute(exucutes)
                disk_db.commit()
                await ctx.send(f'Anzahl der Tode: {death}')

    @commands.command()
    async def poe(self, ctx: commands.Context):

        user = str(ctx.message.author.name)
        messagesend = "/w " + user + " test"
        await ctx.send(messagesend)

        print(messagesend)

        await ctx.message.author.send("Tradeseiten: https://poe.trade/ ODER https://www.pathofexile.com/trade/search/Scourge // Aktuelle Season: https://www.pathofexile.com/scourge // Offizielles PoE-Wiki: https://pathofexile.fandom.com/wiki/Path_of_Exile_Wiki // PoE-Ninja (Preisvergleich, Gegenwert von Items, Leader): https://poe.ninja/ // PoE Builds: https://www.poebuilds.cc/ ODER https://www.poe-vault.com/guides/builds-for-path-of-exile // Custom-PoE-Filter: https://www.filterblade.xyz/")

    
        #user = message.author
        #await user.send("Tradeseiten: https://poe.trade/ ODER https://www.pathofexile.com/trade/search/Scourge // Aktuelle Season: https://www.pathofexile.com/scourge // Offizielles PoE-Wiki: https://pathofexile.fandom.com/wiki/Path_of_Exile_Wiki // PoE-Ninja (Preisvergleich, Gegenwert von Items, Leader): https://poe.ninja/ // PoE Builds: https://www.poebuilds.cc/ ODER https://www.poe-vault.com/guides/builds-for-path-of-exile // Custom-PoE-Filter: https://www.filterblade.xyz/")

    @commands.command()
    async def searchbuild(self, ctx: commands.Context, mssg):
        mssg = ctx.message.content[13:]
        name = ctx.message.author.name
        builds = rabu.findinbuilds(mssg)
        if builds:
            i = 0
            for build in builds:
                if i < 10:
                    
                    i += 1
                    print(f"{i} - {build}")
                    await ctx.send(f'Build: {build}')
                    time.sleep(2)
            
        else:
            await ctx.send("Kein Build gefunden")

    #@routines.routine(minutes=60)
    #async def hello():
        #if bot.connected_channels:
            #ws = bot.get_channel("theddy")

            #print("ping")
            #await ws.send("Ihr könnt euch jetzt eur eigenen Random Poe Build zuweisen lassen ganz einfach mit !randombuild. Builds könnt ihr suchen mit !searchbuild [stichwort] (Jetzt auch mit poevault.com builds)")

            #testen = await bot.fetch_users(["shalora_"])

    #hello.start()


if __name__ == '__main__':
    bot = Bot()
    bot.run()
