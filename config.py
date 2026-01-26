import os
from dotenv import load_dotenv
import discord

# Charger les variables d'environnement
load_dotenv()

# Configuration du bot
BOT_TOKEN = os.getenv('TOKEN')
PORT = int(os.getenv('PORT', 8080))
COMMAND_PREFIX = 'a!'  # 'a' pour Araki

# ID des rôles et canaux (à remplacer par vos propres IDs)
ROLE_CATENACCIO_ID = 1465027907968831541  # À remplacer
WELCOME_THREAD_ID = 1330182024832614541   # À remplacer
ANNOUNCEMENTS_CHANNEL_ID = 1330182401787170847  # À remplacer
DISCUSSIONS_CATEGORY_ID = 1330182024832614541   # À remplacer

# Configuration des intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Couleurs pour les embeds (thème football/Catenaccio)
GREEN_COLOR = 0x00FF00      # Vert terrain de foot
DARK_BLUE_COLOR = 0x003366  # Bleu foncé tactique

# Réactions pour les annonces
ANNOUNCEMENT_REACTIONS = ["🔥", "👀", "❤️"]

# Paramètres pour les threads de discussion
THREAD_AUTO_ARCHIVE_DURATION = 1440  # 24 heures

# Configuration du timer
TIMER_UPDATE_INTERVAL = 60 * 60  # Mise à jour toutes les heures
TIMER_STATUS_COLORS = {
    'EARLY': 0x00FF00,    # Vert
    'SOON': 0xFFFF00,     # Jaune
    'IMMINENT': 0xFF0000  # Rouge
}