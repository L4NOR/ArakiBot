import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from config import BOT_TOKEN, COMMAND_PREFIX, intents
from commands import setup_commands
from events import setup
from card_system import setup_card_commands

async def main():
    # Initialisation du bot
    bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)
    
    # Supprimer la commande help par défaut
    bot.remove_command('help')
    
    # Configuration des commandes et événements
    setup_commands(bot)  # Commandes avec préfixe a!
    setup_card_commands(bot)  # Système de cartes
    await setup(bot)  # Ceci configure déjà l'événement on_ready
    
    # Lancer le bot
    async with bot:
        await bot.start(BOT_TOKEN)

# Point d'entrée principal
if __name__ == "__main__":
    asyncio.run(main())