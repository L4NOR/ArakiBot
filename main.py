import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from config_catenaccio import BOT_TOKEN, COMMAND_PREFIX, intents
from commands_catenaccio import setup_commands
from events_catenaccio import setup
from utils_catenaccio import app

async def main():
    # Initialisation du bot
    bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)
    
    # Supprimer la commande help par défaut
    bot.remove_command('help')
    
    # Configuration des commandes et événements
    setup_commands(bot)  # Commandes avec préfixe a!
    await setup(bot)
    
    # Événement on_ready pour synchroniser les commandes slash
    @bot.event
    async def on_ready():
        print(f'Bot connecté en tant que {bot.user.name}')
        # Synchroniser les commandes slash avec Discord
        await bot.tree.sync()
        await bot.change_presence(activity=discord.Game(name="Lire Catenaccio ⚽"))
        from utils_catenaccio import start_webserver
        await start_webserver(bot)
    
    # Lancer le bot
    async with bot:
        await bot.start(BOT_TOKEN)

# Point d'entrée principal
if __name__ == "__main__":
    asyncio.run(main())