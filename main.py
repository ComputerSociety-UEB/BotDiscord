import discord
from discord.ext import commands
import config  # archivo token config.py

# Nuevas importaciones
from funcionalidadesbasicas import setup
from funcionalidadesextras import FuncionalidadesExtras

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='-', intents=intents)

# Prueba de Argumento
@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

# Prueba de runeo exitoso
@bot.event
async def on_ready():
    print(f"Locked in {bot.user}")

# Registrar los comandos de funcionalidadesbasicas.py
setup(bot)

# Comando para enviar frases motivacionales
@bot.command(name="motivacion")
async def motivacion(ctx):
    await FuncionalidadesExtras.enviar_frase_motivacional(ctx)

# MUY IMPORTANTE: on_message personalizado
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Primero detectar si dicen "profe"
    await FuncionalidadesExtras.detectar_profe(message)

    # Después procesar comandos como -motivacion, -test, etc.
    await bot.process_commands(message)

bot.run(config.TOKEN)
