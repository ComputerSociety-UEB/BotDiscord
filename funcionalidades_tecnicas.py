# funcionalidades_tecnicas.py
import requests
import config
from discord.ext import commands

class FuncionalidadesTecnicas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='github')
    async def github(self, ctx):
        repos = [
            "[Repositorio Base](https://github.com/ComputerSociety-UEB)",
            "[Repositorio Proyecto BotDiscord](https://github.com/ComputerSociety-UEB/BotDiscord.git)"
        ]
        mensaje = "**📦 Repositorios del Semillero:**\n" + "\n".join(repos)
        await ctx.send(mensaje)

    @commands.command(name='miembros')
    async def miembros(self, ctx):
        miembros = ctx.guild.members  # Obtiene todos los miembros del servidor
        mensaje = "**👥 Lista de miembros y sus roles:**\n\n"

        for miembro in miembros:
            roles = [rol.name for rol in miembro.roles if rol.name != "@everyone"]
            roles_str = ', '.join(roles) if roles else 'Sin rol'
            mensaje += f"• {miembro.display_name} → {roles_str}\n"

        # Dividir el mensaje si es muy largo
        if len(mensaje) > 1900:
            partes = [mensaje[i:i + 1900] for i in range(0, len(mensaje), 1900)]
            for parte in partes:
                await ctx.send(parte)
        else:
            await ctx.send(mensaje)

    @commands.command(name='botinfo')
    async def botinfo(self, ctx):
        info = (
            "**🤖 Información del Bot:**\n"
            "• 👨‍🔧 Creador: *Tu Nombre Aquí*\n"
            "• 🧾 Versión: `1.0.0`\n"
            "• ⚙️ Lenguaje: Python 3 + discord.py\n"
            "• 🧠 Propósito: Automatización del semillero y herramientas técnicas\n"
            "• 📅 Fecha de creación: Abril 2025"
        )
        await ctx.send(info)

    @commands.command(name='noticias')
    async def noticias(self, ctx):
        url = f"https://gnews.io/api/v4/search?q=tecnología&lang=es&token={config.GNEWS_API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            articulos = data.get("articles", [])[:3]
            if not articulos:
                await ctx.send("No encontré noticias recientes de tecnología 😕")
                return

            mensaje = "**📰 Noticias de Tecnología:**\n"
            for articulo in articulos:
                mensaje += f"• [{articulo['title']}]({articulo['url']})\n"
            await ctx.send(mensaje)
        else:
            await ctx.send("Hubo un error al obtener las noticias 😓")

    @commands.command(name='memes')
    async def memes(self, ctx):
        url = "https://meme-api.com/gimme/programmingmemes"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            meme_url = data.get("url")
            title = data.get("title", "Meme de programación")
            await ctx.send(f"**{title}**\n{meme_url}")
        else:
            await ctx.send("No se pudo obtener el meme en este momento 😅")

    @commands.command(name='documentacion')
    async def documentacion(self, ctx, *, tema: str):
        url = f"https://api.duckduckgo.com/?q={tema}+documentation&format=json&no_html=1"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            abstract = data.get("Abstract")
            related = data.get("RelatedTopics", [])
            respuesta = f"**📚 Resultado para:** `{tema}`\n"

            if abstract:
                respuesta += f"> {abstract}\n"
            elif related:
                resultado = related[0]
                if "Text" in resultado and "FirstURL" in resultado:
                    respuesta += f"{resultado['Text']}\n🔗 {resultado['FirstURL']}"
                else:
                    respuesta += "No se encontró información clara sobre ese tema 😕"
            else:
                respuesta += "No se encontró información relevante 😓"

            await ctx.send(respuesta)
        else:
            await ctx.send("❌ No se pudo conectar a DuckDuckGo.")

    @commands.command(name='deepseek')
    async def deepseek(self, ctx, *, pregunta: str):
        await ctx.send("🧠 Consultando a DeepSeek...")

        headers = {
            "Authorization": f"Bearer {config.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": pregunta}],
            "temperature": 0.7,
            "max_tokens": 200
        }

        try:
            response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=body)
            if response.status_code == 200:
                data = response.json()
                respuesta = data["choices"][0]["message"]["content"]
                await ctx.send(f"💡 **DeepSeek responde:**\n{respuesta}")
            else:
                await ctx.send("❌ Error al contactar con DeepSeek.")
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")


def setup(bot):
    bot.add_cog(FuncionalidadesTecnicas(bot))
