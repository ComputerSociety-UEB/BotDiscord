from discord.ext import commands

class xpSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.puntos = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        autor = message.author.id
        self.puntos[autor] = self.puntos.get(autor, 0) + 5

    @commands.command(name='xp')
    async def mostrar_xp(self, ctx):
        xp = self.puntos.get(ctx.author.id, 0)
        await ctx.send(f"📈 {ctx.author.name}, tienes {xp} puntos de experiencia.")

    @commands.command(name='lvl')
    async def mostrar_xp(self, ctx):
        xp = self.puntos.get(ctx.author.id, 0)
        await ctx.send(f"📈 {ctx.author.name}, eres nivel {xp//100 }.")