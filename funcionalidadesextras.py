import random
import requests

class FuncionalidadesExtras:

    @staticmethod
    async def enviar_frase_motivacional(ctx):
        frases = [
            "¡A darle con todo, papu! No hay excusas, ¡tú eres el crack del día!",
            "Siempre sé tú mismo. Pero si puedes ser Batman, ¡mejor sé Batman, que está más mejor!",
            "Si la vida te da la espalda... ¡Agárrale las nalgas y demuéstrale quién manda, bro!",
            "El amor no sana... Lo que sana es la colita de rana",
            "Hay dos palabras que te abrirán muchas puertas: Tire y Empuje"
        ]
        frase = random.choice(frases)
        await ctx.send(frase)

    @staticmethod
    async def detectar_profe(message):
        if "profe" in message.content.lower():
            respuestas = [
                "¿Profe? Yo sólo veo pura sabrosura aquí 😎",
                "¿Profe? Está ocupado viendo memes, vuelve en 5 minutos 😂",
                "El profe dice que no hay tarea... pero tampoco calificación 😬",
                "¿Quién invocó al profe? 🧙‍♂️✨",
                "Profe detectado. ¡Modo serio activado! 👨‍🏫"
            ]
            await message.channel.send(random.choice(respuestas))

    @staticmethod
    async def generar_meme_megamind(ctx, texto: str):
        """Genera un meme con la plantilla de Megamind."""
        # Manejar el caso de | o sin |
        if "|" in texto:
            texto_superior, texto_inferior = texto.split("|", 1)
            texto_superior = texto_superior.strip()
            texto_inferior = texto_inferior.strip()
        else:
            texto_superior = ""
            texto_inferior = texto.strip()

        url = "https://api.imgflip.com/caption_image"
        params = {
            "template_id": "370867422",  # ID de la plantilla de Megamind
            "username": "Gianfry13", 
            "password": "holasoyyo777",  
            "text0": texto_superior,
            "text1": texto_inferior
        }

        response = requests.post(url, params=params)
        data = response.json()

        if data["success"]:
            await ctx.send(data["data"]["url"])
        else:
            await ctx.send("No se pudo generar el meme 😢")

    @staticmethod
    async def generar_meme_sad(ctx, texto: str):
        """Genera un meme con la plantilla de Kermit at the Window (Sad)."""
        # Manejar el caso de | o sin |
        if "|" in texto:
            texto_superior, texto_inferior = texto.split("|", 1)
            texto_superior = texto_superior.strip()
            texto_inferior = texto_inferior.strip()
        else:
            texto_superior = ""
            texto_inferior = texto.strip()

        if not texto_inferior:  # Si no hay texto inferior, enviar error
            await ctx.send("❌ ¡Necesito un texto para el meme! 😢")
            return

        url = "https://api.imgflip.com/caption_image"
        params = {
            "template_id": "36698509",  # ID de la plantilla de Kermit
            "username": "Gianfry13",  
            "password": "holasoyyo777",
            "text0": texto_superior,  # Usar el texto superior
            "text1": texto_inferior  # Usar el texto inferior
        }

        response = requests.post(url, params=params)
        data = response.json()

        if data["success"]:
            await ctx.send(data["data"]["url"])
        else:
            await ctx.send("No se pudo generar el meme 😢")
