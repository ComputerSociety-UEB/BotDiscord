import discord
from discord.ext import commands 
import requests
import config #archivo token config.py


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
    print(f"Locked in {bot.user}")

bot.run(config.TOKEN)