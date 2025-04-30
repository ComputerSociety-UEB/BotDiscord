import discord
from discord.ext import commands

class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.preguntas = {
            "pregunta": "respuesta",
            
        }

    @commands.command(name='trivia')
    async def trivia(self, ctx):
        import random
        pregunta, respuesta = random.choice(list(self.preguntas.items()))
        await ctx.send(f"🧠 **Pregunta:** {pregunta}")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for("message", timeout=30.0, check=check)
            if msg.content.lower() == respuesta.lower():
                await ctx.send("✅ ¡Correcto!")
            else:
                await ctx.send(f"❌ Incorrecto. La respuesta era: {respuesta}")
        except:
            await ctx.send("⌛ Se acabó el tiempo.")
