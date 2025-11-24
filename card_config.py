# Configuration du système de cartes Catenaccio

# Crédits de départ pour les nouveaux joueurs
STARTING_CREDITS = 500

# Récompense quotidienne
DAILY_REWARD = 100

# Durée avant expiration des échanges (en minutes)
TRADE_EXPIRATION_MINUTES = 5

# Prix des packs (modifiable selon vos besoins)
PACK_PRICES = {
    "basique": {
        "price": 100,
        "cards": 3,
        "name": "Pack Basique",
        "description": "Un pack d'entrée de gamme pour commencer votre collection"
    },
    "argent": {
        "price": 250,
        "cards": 5,
        "name": "Pack Argent",
        "description": "Plus de cartes, plus de chances de cartes rares"
    },
    "or": {
        "price": 500,
        "cards": 7,
        "name": "Pack Or",
        "description": "Pour les collectionneurs sérieux"
    },
    "platine": {
        "price": 1000,
        "cards": 10,
        "name": "Pack Platine",
        "description": "Le meilleur rapport qualité/prix pour les experts"
    },
    "événement": {
        "price": 0,
        "cards": 5,
        "name": "Pack Événement",
        "description": "Pack spécial gratuit lors d'événements"
    }
}

# Taux de drop des cartes (total doit faire 1.0 ou 100%)
DROP_RATES = {
    "Commune": 0.70,      # 70%
    "Rare": 0.20,         # 20%
    "Épique": 0.08,       # 8%
    "Légendaire": 0.02,   # 2%
    "Mythique": 0.005     # 0.5%
}

# Base de données des cartes
CARD_DATABASE = {
    "Commune": {
        "drop_rate": DROP_RATES["Commune"],
        "cards": [
            {"name": "Défenseur Latéral", "type": "Défense", "rarity": "Commune", "emoji": "🛡️"},
            {"name": "Milieu Défensif", "type": "Défense", "rarity": "Commune", "emoji": "🛡️"},
            {"name": "Arrière Central", "type": "Défense", "rarity": "Commune", "emoji": "🛡️"},
            {"name": "Gardien Remplaçant", "type": "Défense", "rarity": "Commune", "emoji": "🧤"},
            {"name": "Attaquant de Pointe", "type": "Attaque", "rarity": "Commune", "emoji": "⚡"},
            {"name": "Ailier Rapide", "type": "Vitesse", "rarity": "Commune", "emoji": "💨"},
            {"name": "Meneur de Jeu", "type": "Technique", "rarity": "Commune", "emoji": "🎯"},
            {"name": "Joueur Polyvalent", "type": "Physique", "rarity": "Commune", "emoji": "💪"},
            {"name": "Milieu Récupérateur", "type": "Défense", "rarity": "Commune", "emoji": "🛡️"},
            {"name": "Avant-Centre", "type": "Attaque", "rarity": "Commune", "emoji": "⚡"},
        ]
    },
    "Rare": {
        "drop_rate": DROP_RATES["Rare"],
        "cards": [
            {"name": "Capitaine Défensif", "type": "Défense", "rarity": "Rare", "emoji": "🛡️"},
            {"name": "Libéro Tactique", "type": "Défense", "rarity": "Rare", "emoji": "🛡️"},
            {"name": "Gardien Expérimenté", "type": "Défense", "rarity": "Rare", "emoji": "🧤"},
            {"name": "Buteur Clinique", "type": "Attaque", "rarity": "Rare", "emoji": "⚡"},
            {"name": "Dribbleur Technique", "type": "Technique", "rarity": "Rare", "emoji": "🎯"},
            {"name": "Sprinter Ailier", "type": "Vitesse", "rarity": "Rare", "emoji": "💨"},
            {"name": "Stoppeur Aérien", "type": "Physique", "rarity": "Rare", "emoji": "💪"},
            {"name": "Passeur Décisif", "type": "Technique", "rarity": "Rare", "emoji": "🎯"},
        ]
    },
    "Épique": {
        "drop_rate": DROP_RATES["Épique"],
        "cards": [
            {"name": "Araki - Défenseur Prodige", "type": "Défense", "rarity": "Épique", "emoji": "🛡️"},
            {"name": "Mur Infranchissable", "type": "Défense", "rarity": "Épique", "emoji": "🛡️"},
            {"name": "Gardien Légendaire", "type": "Défense", "rarity": "Épique", "emoji": "🧤"},
            {"name": "Attaquant d'Élite", "type": "Attaque", "rarity": "Épique", "emoji": "⚡"},
            {"name": "Maestro du Milieu", "type": "Technique", "rarity": "Épique", "emoji": "🎯"},
            {"name": "Éclair sur l'Aile", "type": "Vitesse", "rarity": "Épique", "emoji": "💨"},
        ]
    },
    "Légendaire": {
        "drop_rate": DROP_RATES["Légendaire"],
        "cards": [
            {"name": "Araki - Catenaccio Ultime", "type": "Défense", "rarity": "Légendaire", "emoji": "🛡️"},
            {"name": "Gardien Immortel", "type": "Défense", "rarity": "Légendaire", "emoji": "🧤"},
            {"name": "Stratège Absolu", "type": "Technique", "rarity": "Légendaire", "emoji": "🎯"},
            {"name": "Buteur Légendaire", "type": "Attaque", "rarity": "Légendaire", "emoji": "⚡"},
        ]
    },
    "Mythique": {
        "drop_rate": DROP_RATES["Mythique"],
        "cards": [
            {"name": "Araki - Maître du Catenaccio", "type": "Mythique", "rarity": "Mythique", "emoji": "👑"},
            {"name": "Dieu du Football", "type": "Mythique", "rarity": "Mythique", "emoji": "👑"},
        ]
    }
}

# Couleurs pour les embeds par rareté
RARITY_COLORS = {
    "Commune": 0x808080,      # Gris
    "Rare": 0x0080FF,         # Bleu
    "Épique": 0x8000FF,       # Violet
    "Légendaire": 0xFF8000,   # Orange
    "Mythique": 0xFF0000      # Rouge
}

# Icônes pour les rarétés
RARITY_ICONS = {
    "Commune": "⚪",
    "Rare": "🔵",
    "Épique": "🟣",
    "Légendaire": "🟠",
    "Mythique": "🔴"
}

# Messages personnalisables
MESSAGES = {
    "welcome_new_player": "Bienvenue dans le système de collection Catenaccio ! Vous commencez avec {credits} CC.",
    "daily_claimed": "Vous avez déjà réclamé votre récompense quotidienne. Revenez dans {time}.",
    "daily_reward": "Vous avez reçu {reward} Crédits Catenaccio (CC) !",
    "insufficient_credits": "Crédits insuffisants. Vous avez {current} CC, il en faut {required} CC.",
    "pack_opened": "📦 {pack_name} ouvert ! Voici vos nouvelles cartes :",
    "trade_sent": "Votre proposition d'échange a été envoyée à {user} !",
    "trade_accepted": "L'échange a été complété avec succès !",
    "trade_declined": "Vous avez refusé la proposition d'échange.",
    "trade_expired": "Cette proposition d'échange a expiré.",
    "no_trade_found": "Aucune proposition d'échange trouvée de cet utilisateur."
}

# Nom du fichier de sauvegarde
DATA_FILE = "card_data.json"

# Activer/désactiver certaines fonctionnalités
FEATURES = {
    "daily_rewards": True,
    "trading": True,
    "pack_opening": True,
    "admin_commands": True,
    "statistics": True
}

# Limites pour éviter les abus
LIMITS = {
    "max_collection_size": 1000,        # Nombre maximum de cartes par joueur
    "max_credits": 100000,              # Nombre maximum de crédits
    "max_trade_credits": 10000,         # Montant maximum de crédits dans un échange
    "max_pending_trades_per_user": 5    # Nombre maximum d'échanges en attente par joueur
}