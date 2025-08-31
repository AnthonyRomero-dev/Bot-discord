# ==================================================================================================
# Copyright (c) 2025 Anthonydev
# Todos los derechos reservados.
# ==================================================================================================

import discord
from discord.commands import SlashCommandGroup, Option
from discord.ext import commands
import logging
import asyncio

# ==================================================================================================
# --- CONFIGURACIÓN PRINCIPAL ---
# ==================================================================================================

CONFIG = {
    "TOKEN": "TU_TOKEN_AQUI",
}

# ==================================================================================================
# --- CONFIGURACIÓN DE LOGGING ---
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
# --- INICIALIZACIÓN DEL BOT ---
# ==================================================================================================

# Define los intents que tu bot necesita.
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Crea la instancia del bot para comandos de barra.
bot = discord.Bot(intents=intents)

# ==================================================================================================
# --- EVENTOS DEL BOT ---
# ==================================================================================================

@bot.event
async def on_ready():
    """Evento que se dispara cuando el bot está listo y conectado."""
    logger.info(f'¡Bot conectado como {bot.user}!')
    logger.info(f'ID del Bot: {bot.user.id}')
    logger.info('------')
    activity = discord.Activity(type=discord.ActivityType.watching, name="el código mejorar")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    logger.info("Estado de actividad configurado como 'Watching el código mejorar'")

# ==================================================================================================
# --- COMANDOS DE BARRA (SLASH COMMANDS) ---
# ==================================================================================================

@bot.slash_command(name='ping', description='Muestra la latencia del bot.')
async def ping(ctx: discord.ApplicationContext):
    """Responde con la latencia del bot para verificar que está activo."""
    latency = round(bot.latency * 1000)
    await ctx.respond(f'Pong! Latencia: {latency}ms')

@bot.slash_command(
    name='clear', 
    description='Borra una cantidad de mensajes en el canal.',
    default_member_permissions=discord.Permissions(manage_messages=True) # Requiere permisos en el usuario
)
async def clear(
    ctx: discord.ApplicationContext, 
    amount: Option(int, "La cantidad de mensajes a borrar", min_value=1, max_value=100)
):
    """Borra una cantidad especificada de mensajes del canal."""
    # Verifica si el bot tiene permisos para borrar mensajes
    if not ctx.app_permissions.manage_messages:
        await ctx.respond("No tengo los permisos para borrar mensajes en este canal.", ephemeral=True)
        return

    await ctx.defer() # Difiere la respuesta para que no se agote el tiempo de espera
    
    # El método purge no puede borrar mensajes de más de 14 días.
    deleted_messages = await ctx.channel.purge(limit=amount)
    
    await ctx.followup.send(f'Se han borrado {len(deleted_messages)} mensajes.', ephemeral=True)

# ==================================================================================================
# --- PUNTO DE ENTRADA PRINCIPAL ---
# ==================================================================================================

def main():
    """Función principal para iniciar el bot."""
    try:
        bot.run(CONFIG["TOKEN"])
    except discord.errors.LoginFailure:
        logger.error("Error de inicio de sesión: El token proporcionado es inválido.")
    except Exception as e:
        logger.error(f"Ha ocurrido un error crítico al iniciar el bot: {e}")

if __name__ == "__main__":
    main()