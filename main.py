import discord
from discord.ext import commands
import config
from sourvey import Sourvey
from trivia import Trivia
from xpSystem import xpSystem 
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='-', intents = intents)

#Prueba de Argumento
@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)


#Prueba de runeo exitoso 
@bot.event
async def on_ready():
    print(f" Locked in as {bot.user}")

async def setup():
    await bot.add_cog(Sourvey(bot))
    await bot.add_cog(Trivia(bot))
    await bot.add_cog(xpSystem(bot))
async def main():
    await setup()
    await bot.start(config.TOKEN)

asyncio.run(main())

bot.run(config.TOKEN)