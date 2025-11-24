# main.py
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from config import BOT_TOKEN, COMMAND_PREFIX, intents
from commands import setup_commands
from events import setup
# Nouveau import
from cards_commands import setup_cards_commands

async def main():
    # Initialisation du bot
    bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)
    
    # Supprimer la commande help par défaut si existante
    try:
        bot.remove_command('help')
    except Exception:
        pass
    
    # Configuration des commandes et événements
    setup_commands(bot)       # commandes existantes (a!)
    setup_cards_commands(bot) # nouvelles commandes "cartes" (a!)
    await setup(bot)          # ceci configure déjà l'événement on_ready
    
    # Lancer le bot
    async with bot:
        await bot.start(BOT_TOKEN)

# Point d'entrée principal
if __name__ == "__main__":
    asyncio.run(main())
