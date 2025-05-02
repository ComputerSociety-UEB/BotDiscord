from discord.ext import commands
import discord
import asyncio

BAD_WORDS = ["cagada", "mierda", "puta", ":v"]

def setup(bot):

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        message_content = message.content.lower()
        for bad_word in BAD_WORDS:
            if bad_word in message_content:
                await message.delete()
                await message.channel.send(f"❌ {message.author.mention}, ese lenguaje no es permitido.")

                mute_role = discord.utils.get(message.guild.roles, name="muted")
                if mute_role:
                    await message.author.add_roles(mute_role)
                    await message.channel.send(f"✅ {message.author.mention} ha sido muteado por 5 minutos.")
                    await asyncio.sleep(5 * 60)
                    await message.author.remove_roles(mute_role)
                    await message.channel.send(f"✅ {message.author.mention} ha dejado de estar muteado.")
                break

        await bot.process_commands(message)

    @bot.event
    async def on_member_join(member):
        # Obtener el canal de bienvenida, si existe
        canal_bienvenida = discord.utils.get(member.guild.text_channels, name="general")
        if canal_bienvenida:
            await canal_bienvenida.send(f"👋 ¡Bienvenido/a al servidor, {member.mention}! Revisa las reglas con `-reglas`.")

        # Asignar rol inicial
        rol_inicial = discord.utils.get(member.guild.roles, name="prueba")
        if rol_inicial:
            await member.add_roles(rol_inicial)
            if canal_bienvenida:
                await canal_bienvenida.send(f"✅ Se ha asignado el rol **{rol_inicial.name}** a {member.mention}.")
        else:
            if canal_bienvenida:
                await canal_bienvenida.send("⚠️ No se encontró el rol 'prueba'. Asegúrate de crearlo en el servidor.")

    @bot.command(name="reglas")
    async def reglas(ctx):
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
        if cantidad is None or cantidad <= 0:
            advertencia = await ctx.send("❌ Debes especificar una cantidad positiva. Ejemplo: `-borrar 5`")
            await advertencia.delete(delay=5)
            return

        await ctx.channel.purge(limit=cantidad + 1)
        confirmacion = await ctx.send(f"✅ Se han borrado {cantidad} mensajes.")
        await confirmacion.delete(delay=3)

    @bot.command(name="mutear")
    @commands.has_permissions(manage_roles=True)
    async def mutear(ctx, member: discord.Member, tiempo: int = 5):
        mute_role = discord.utils.get(ctx.guild.roles, name="muted")
        if mute_role is None:
            mute_role = await ctx.guild.create_role(name="muted", permissions=discord.Permissions(send_messages=False))
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(mute_role, send_messages=False)

        if mute_role in member.roles:
            await ctx.send(f"❌ {member.mention} ya está muteado.")
            return

        await member.add_roles(mute_role)
        await ctx.send(f"✅ {member.mention} ha sido muteado por {tiempo} minutos.")
        await asyncio.sleep(tiempo * 60)
        await member.remove_roles(mute_role)
        await ctx.send(f"✅ {member.mention} ha dejado de estar muteado.")

    @bot.command(name="banear")
    @commands.has_permissions(ban_members=True)
    async def banear(ctx, miembro: discord.Member = None, *, motivo="No especificado"):
        if miembro is None:
            await ctx.send("❌ Debes mencionar a un usuario. Ejemplo: `-banear @usuario`")
            return
        try:
            await miembro.ban(reason=motivo)
            await ctx.send(f"🔨 {miembro.mention} ha sido baneado. Motivo: {motivo}")
        except Exception as e:
            await ctx.send(f"❌ Error al banear: {e}")

    @bot.command(name="desbanear")
    @commands.has_permissions(ban_members=True)
    async def desbanear(ctx, user_id: int = None):
        if user_id is None:
            await ctx.send("❌ Debes indicar el ID. Ejemplo: `-desbanear 1234567890`")
            return

        banned_users = [entry async for entry in ctx.guild.bans()]
        user = discord.utils.get(banned_users, user__id=user_id)

        if user is None:
            await ctx.send("❌ No se encontró un usuario baneado con ese ID.")
            return

        try:
            await ctx.guild.unban(user.user)
            await ctx.send(f"✅ {user.user.mention} ha sido desbaneado.")
        except Exception as e:
            await ctx.send(f"❌ Error al desbanear: {e}")zz
