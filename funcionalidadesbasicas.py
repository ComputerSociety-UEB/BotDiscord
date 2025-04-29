from discord.ext import commands
import discord
import asyncio  # Necesario para el uso de asyncio.sleep()


BAD_WORDS = ["cagada", "mierda", "puta", ":v"]  # Lista de malas palabras

def setup(bot):
    
    @bot.event
    async def on_message(message):
        """Filtra malas palabras y spam en los mensajes."""
        
        # No procesar mensajes del bot mismo
        if message.author == bot.user:
            return

        # Convertir el mensaje a minúsculas para hacer la búsqueda insensible a mayúsculas
        message_content = message.content.lower()

        # Verificar si el mensaje contiene alguna de las malas palabras
        for bad_word in BAD_WORDS:
            if bad_word in message_content:
                # Eliminar el mensaje
                await message.delete()

                # Advertir al usuario
                await message.channel.send(f"❌ {message.author.mention}, ese lenguaje no es permitido.")
                
                # Opcional: Mutea al usuario por 5 minutos si se detecta una mala palabra
                mute_role = discord.utils.get(message.guild.roles, name="muted")
                if mute_role:
                    await message.author.add_roles(mute_role)
                    await message.channel.send(f"✅ {message.author.mention} ha sido muteado por 5 minutos debido al uso de malas palabras.")
                    
                    # Esperar 5 minutos antes de quitar el mute
                    await asyncio.sleep(5 * 60)  # 5 minutos en segundos
                    await message.author.remove_roles(mute_role)
                    await message.channel.send(f"✅ {message.author.mention} ha dejado de estar muteado.")
                break  # Salir del ciclo una vez que se encuentra una palabra prohibida

        # Continuar con el procesamiento de otros comandos
        await bot.process_commands(message)

    @bot.command(name="reglas")
    async def reglas(ctx):
        """Muestra las normas del semillero."""
        normas = (
            "📌 **Normas del Grupo:**\n\n"
            "1. Mantener respeto y profesionalismo en todas las interacciones.\n"
            "2. Compartir únicamente información relevante al proyecto.\n"
            "3. Participar activamente en las discusiones y tareas asignadas.\n\n"
        )
        await ctx.send(normas)

    @bot.command(name="borrar")
    @commands.has_permissions(manage_messages=True)
    async def borrar(ctx, cantidad: int = None):
        """Borra una cantidad de mensajes del canal."""
        if cantidad is None:
            advertencia = await ctx.send("❌ Debes especificar cuántos mensajes deseas borrar. Ejemplo: `-borrar 5`")
            await advertencia.delete(delay=5)
            return

        if cantidad <= 0:
            advertencia = await ctx.send("❌ Debes especificar una cantidad positiva de mensajes a borrar.")
            await advertencia.delete(delay=5)
            return
        
        await ctx.channel.purge(limit=cantidad + 1)
        confirmacion = await ctx.send(f"✅ Se han borrado {cantidad} mensajes.")
        await confirmacion.delete(delay=3)

    @bot.command(name="mutear")
    @commands.has_permissions(manage_roles=True)  # Necesita permisos para gestionar roles
    async def mutear(ctx, member: discord.Member, tiempo: int = 5):
        """Muta a un usuario por un tiempo determinado (en minutos)."""
        
        # Establecer el tiempo predeterminado a 5 minutos si no se especifica
        if tiempo is None:
            tiempo = 5

        # Buscamos el rol de 'muted'
        mute_role = discord.utils.get(ctx.guild.roles, name="muted")
        if mute_role is None:
            # Si no existe, lo creamos
            mute_role = await ctx.guild.create_role(name="muted", permissions=discord.Permissions(send_messages=False))

            # Asegurarnos de que este rol no permita enviar mensajes en todos los canales
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(mute_role, send_messages=False)

        # Verificamos si el usuario ya tiene el rol 'muted'
        if mute_role in member.roles:
            await ctx.send(f"❌ {member.mention} ya está muteado.")
            return

        # Aplicamos el rol 'muted' al usuario
        await member.add_roles(mute_role)
        await ctx.send(f"✅ {member.mention} ha sido muteado por {tiempo} minutos.")

        # Esperamos el tiempo de mutear (convertido a segundos)
        await asyncio.sleep(tiempo * 60)

        # Quitamos el rol 'muted' después del tiempo
        await member.remove_roles(mute_role)
        await ctx.send(f"✅ {member.mention} ha dejado de estar muteado.")

    @bot.command(name="banear")
    @commands.has_permissions(ban_members=True)  # Requiere permiso de banear
    async def banear(ctx, miembro: discord.Member = None, *, motivo="No especificado"):
        """Banea a un miembro del servidor."""
        if miembro is None:
            await ctx.send("❌ Debes mencionar a un usuario para banear. Ejemplo: `-banear @usuario`")
            return

        try:
            await miembro.ban(reason=motivo)
            await ctx.send(f"🔨 {miembro.mention} ha sido baneado. Motivo: {motivo}")
        except Exception as e:
            await ctx.send(f"❌ No se pudo banear al usuario. Error: {e}")

    @bot.command(name="desbanear")
    @commands.has_permissions(ban_members=True)
    async def desbanear(ctx, user_id: int = None):
        """Desbanea a un usuario por su ID."""
        if user_id is None:
            await ctx.send("❌ Debes especificar el ID del usuario a desbanear. Ejemplo: `-desbanear 1234567890`")
            return

        banned_users = [entry async for entry in ctx.guild.bans()]
        user = discord.utils.get(banned_users, user__id=user_id)

        if user is None:
            await ctx.send("❌ No se encontró un usuario baneado con ese ID.")
            return

        try:
            await ctx.guild.unban(user.user)
            await ctx.send(f"✅ El usuario {user.user.mention} ha sido desbaneado correctamente.")
        except Exception as e:
            await ctx.send(f"❌ No se pudo desbanear al usuario. Error: {e}")