import discord
from discord.ext import commands
import config  # archivo con config.TOKEN

from funcionalidadesbasicas import setup
from funcionalidadesextras import FuncionalidadesExtras

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='-', intents=intents)

# Evento de encendido
@bot.event
async def on_ready():
    print(f"Locked in {bot.user}")

# Evento para detectar la palabra "profe"
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await FuncionalidadesExtras.detectar_profe(message)
    await bot.process_commands(message)

# Comando de prueba
@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

# Comando motivacional
@bot.command(name="motivacion")
async def motivacion(ctx):
    await FuncionalidadesExtras.enviar_frase_motivacional(ctx)

# Comando para generar meme de Megamind
@bot.command(name="megamind")
async def megamind(ctx, *, texto: str):
    """Genera un meme con la plantilla de Megamind."""
    await FuncionalidadesExtras.generar_meme_megamind(ctx, texto)

# Comando para generar meme triste (Kermit)
@bot.command(name="sad")
async def sad(ctx, *, texto: str):
    """Genera un meme triste con Kermit."""
    await FuncionalidadesExtras.generar_meme_sad(ctx, texto)

# Comandos básicos
setup(bot)

# Ejecutar bot
bot.run(config.TOKEN)
