import random

class FuncionalidadesExtras:

    @staticmethod
    async def enviar_frase_motivacional(ctx):
        """Envía una frase motivacional ultra épica y meme."""
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
        """Detecta si alguien dice 'profe' y responde algo gracioso."""
        if "profe" in message.content.lower():
            respuestas = [
                "¿Profe? Yo sólo veo pura sabrosura aquí 😎",
                "¿Profe? Está ocupado viendo memes, vuelve en 5 minutos 😂",
                "El profe dice que no hay tarea... pero tampoco calificación 😬",
                "¿Quién invocó al profe? 🧙‍♂️✨",
                "Profe detectado. ¡Modo serio activado! 👨‍🏫"
            ]
            respuesta = random.choice(respuestas)
            await message.channel.send(respuesta)