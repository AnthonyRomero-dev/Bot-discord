# ==================================================================================================
# Copyright (c) 2025 Anthonydev
# Todos los derechos reservados.
# ==================================================================================================

import discord
from discord.ext import commands
import logging
import asyncio

# ==================================================================================================
# --- CONFIGURACIÓN PRINCIPAL ---
# Aquí se definen las variables clave para el funcionamiento del bot.
# ==================================================================================================

CONFIG = {
    # --- ¡ADVERTENCIA DE SEGURIDAD! ---
    # Reemplaza "TU_TOKEN_AQUI" con el token de tu bot de Discord.
    # ¡NUNCA compartas tu token ni lo subas a repositorios públicos como GitHub!
    # Se recomienda encarecidamente usar variables de entorno para manejar el token en producción.
    "TOKEN": "TU_TOKEN_AQUI",
    "PREFIX": "!"
}

# ==================================================================================================
# --- CONFIGURACIÓN DE LOGGING ---
# Un sistema de logging es superior a usar print() porque permite un control detallado
# sobre qué mensajes se muestran, su nivel de importancia (INFO, WARNING, ERROR) y
# a dónde se envían (consola, archivos, etc.).
# ==================================================================================================

def setup_logging():
    """Configura el logging para la aplicación."""
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    return logger

logger = setup_logging()

# ==================================================================================================
# --- COGS (MÓDULOS DE COMANDOS) ---
# Los Cogs permiten agrupar comandos, eventos y listeners en clases separadas (archivos).
# Esto mantiene el código base organizado, legible y escalable.
# ==================================================================================================

class GeneralCog(commands.Cog):
    """Cog para comandos generales y de utilidad."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Evento que se dispara cuando el bot está listo y conectado."""
        logger.info(f'¡Bot conectado como {self.bot.user}!')
        logger.info(f'ID del Bot: {self.bot.user.id}')
        logger.info('------')
        activity = discord.Activity(type=discord.ActivityType.watching, name="el código mejorar")
        await self.bot.change_presence(status=discord.Status.online, activity=activity)
        logger.info("Estado de actividad configurado como 'Watching el código mejorar'")

    @commands.command(name='ping', help='Muestra la latencia del bot.')
    async def ping(self, ctx: commands.Context):
        """Responde con la latencia del bot para verificar que está activo."""
        latency = round(self.bot.latency * 1000)
        await ctx.send(f'Pong! Latencia: {latency}ms')

    @commands.command(name='clear', help='Borra una cantidad de mensajes. Uso: !clear <cantidad>')
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx: commands.Context, amount: int):
        """Borra una cantidad especificada de mensajes del canal."""
        if amount <= 0:
            await ctx.send("La cantidad debe ser un número positivo.", delete_after=5)
            return
            
        # Se suma 1 para borrar también el comando !clear
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'Se han borrado {len(deleted) - 1} mensajes.', delete_after=5)

    @clear.error
    async def clear_error(self, ctx: commands.Context, error):
        """Manejo de errores específico para el comando clear."""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Por favor, especifica la cantidad de mensajes a borrar. Ejemplo: `!clear 5`')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('No tienes los permisos necesarios para usar este comando.')
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send('No tengo los permisos para borrar mensajes en este canal.')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Por favor, proporciona un número válido. Ejemplo: `!clear 5`')
        else:
            logger.error(f"Error inesperado en el comando clear: {error}")
            await ctx.send('Ha ocurrido un error inesperado al ejecutar el comando.')

# ==================================================================================================
# --- PUNTO DE ENTRADA PRINCIPAL ---
# Usar una función `main` asíncrona y el `if __name__ == "__main__":` es la
# práctica estándar para aplicaciones asíncronas, asegurando que el código
# se ejecute solo cuando el script es el punto de entrada principal.
# ==================================================================================================

async def main():
    """Función principal para configurar e iniciar el bot."""
    # Define los intents que tu bot necesita.
    intents = discord.Intents.default()
    intents.message_content = True  # Necesario para leer el contenido de los mensajes
    intents.members = True          # Opcional: si necesitas eventos de miembros

    # Crea la instancia del bot.
    bot = commands.Bot(command_prefix=CONFIG["PREFIX"], intents=intents)

    # Añade los Cogs al bot.
    await bot.add_cog(GeneralCog(bot))

    # Inicia el bot.
    try:
        await bot.start(CONFIG["TOKEN"])
    except discord.errors.LoginFailure:
        logger.error("Error de inicio de sesión: El token proporcionado es inválido. Asegúrate de haberlo copiado correctamente y que no haya expirado.")
    except Exception as e:
        logger.error(f"Ha ocurrido un error crítico al iniciar el bot: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Apagando el bot.")
