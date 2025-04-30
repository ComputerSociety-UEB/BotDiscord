import discord
from discord.ext import commands

class Sourvey(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='encuesta')
    async def encuesta(self, ctx, pregunta: str, *opciones):
        if len(opciones) < 2:
            await ctx.send("Debes proporcionar al menos 2 opciones.")
            return

        embed = discord.Embed(title="📊 Encuesta", description=pregunta, color=0x00ff00)
        mensaje = await ctx.send(embed=embed)

        emojis = ['🇦', '🇧', '🇨', '🇩', '🇪']
        for i, opcion in enumerate(opciones[:5]):
            await mensaje.add_reaction(emojis[i])
            embed.add_field(name=f"{emojis[i]} {opcion}", value='\u200b', inline=False)

        await mensaje.edit(embed=embed)
