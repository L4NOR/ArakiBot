import discord
from discord.ext import commands
import json
import random
from datetime import datetime, timedelta
from config import GREEN_COLOR, DARK_BLUE_COLOR

# Définition des cartes avec leurs rarités et stats
CARD_DATABASE = {
    # Cartes Communes (70% drop rate)
    "Commune": {
        "drop_rate": 0.70,
        "cards": [
            {"name": "Défenseur Latéral", "type": "Défense", "rarity": "Commune", "emoji": "🛡️"},
            {"name": "Milieu Défensif", "type": "Défense", "rarity": "Commune", "emoji": "🛡️"},
            {"name": "Arrière Central", "type": "Défense", "rarity": "Commune", "emoji": "🛡️"},
            {"name": "Gardien Remplaçant", "type": "Défense", "rarity": "Commune", "emoji": "🧤"},
            {"name": "Attaquant de Pointe", "type": "Attaque", "rarity": "Commune", "emoji": "⚡"},
            {"name": "Ailier Rapide", "type": "Vitesse", "rarity": "Commune", "emoji": "💨"},
            {"name": "Meneur de Jeu", "type": "Technique", "rarity": "Commune", "emoji": "🎯"},
            {"name": "Joueur Polyvalent", "type": "Physique", "rarity": "Commune", "emoji": "💪"},
        ]
    },
    # Cartes Rares (20% drop rate)
    "Rare": {
        "drop_rate": 0.20,
        "cards": [
            {"name": "Capitaine Défensif", "type": "Défense", "rarity": "Rare", "emoji": "🛡️"},
            {"name": "Libéro Tactique", "type": "Défense", "rarity": "Rare", "emoji": "🛡️"},
            {"name": "Gardien Expérimenté", "type": "Défense", "rarity": "Rare", "emoji": "🧤"},
            {"name": "Buteur Clinique", "type": "Attaque", "rarity": "Rare", "emoji": "⚡"},
            {"name": "Dribbleur Technique", "type": "Technique", "rarity": "Rare", "emoji": "🎯"},
            {"name": "Sprinter Ailier", "type": "Vitesse", "rarity": "Rare", "emoji": "💨"},
        ]
    },
    # Cartes Épiques (8% drop rate)
    "Épique": {
        "drop_rate": 0.08,
        "cards": [
            {"name": "Araki - Défenseur Prodige", "type": "Défense", "rarity": "Épique", "emoji": "🛡️"},
            {"name": "Mur Infranchissable", "type": "Défense", "rarity": "Épique", "emoji": "🛡️"},
            {"name": "Gardien Légendaire", "type": "Défense", "rarity": "Épique", "emoji": "🧤"},
            {"name": "Attaquant d'Élite", "type": "Attaque", "rarity": "Épique", "emoji": "⚡"},
            {"name": "Maestro du Milieu", "type": "Technique", "rarity": "Épique", "emoji": "🎯"},
        ]
    },
    # Cartes Légendaires (2% drop rate)
    "Légendaire": {
        "drop_rate": 0.02,
        "cards": [
            {"name": "Araki - Catenaccio Ultime", "type": "Défense", "rarity": "Légendaire", "emoji": "🛡️"},
            {"name": "Gardien Immortel", "type": "Défense", "rarity": "Légendaire", "emoji": "🧤"},
            {"name": "Stratège Absolu", "type": "Technique", "rarity": "Légendaire", "emoji": "🎯"},
        ]
    },
    # Cartes Mythiques (0.5% drop rate - événements spéciaux)
    "Mythique": {
        "drop_rate": 0.005,
        "cards": [
            {"name": "Araki - Maître du Catenaccio", "type": "Mythique", "rarity": "Mythique", "emoji": "👑"},
        ]
    }
}

# Prix des packs
PACK_PRICES = {
    "basique": {"price": 100, "cards": 3, "name": "Pack Basique"},
    "argent": {"price": 250, "cards": 5, "name": "Pack Argent"},
    "or": {"price": 500, "cards": 7, "name": "Pack Or"},
    "platine": {"price": 1000, "cards": 10, "name": "Pack Platine"},
    "événement": {"price": 0, "cards": 5, "name": "Pack Événement"}
}

class CardSystem:
    def __init__(self, data_file="card_data.json"):
        self.data_file = data_file
        self.users_data = self.load_data()
    
    def load_data(self):
        """Charge les données depuis le fichier JSON"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_data(self):
        """Sauvegarde les données dans le fichier JSON"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.users_data, f, ensure_ascii=False, indent=4)
    
    def get_user_data(self, user_id):
        """Récupère ou initialise les données d'un utilisateur"""
        user_id_str = str(user_id)
        if user_id_str not in self.users_data:
            self.users_data[user_id_str] = {
                "credits": 500,  # Crédits de départ
                "collection": [],
                "daily_claimed": None,
                "stats": {
                    "packs_opened": 0,
                    "cards_collected": 0,
                    "trades_completed": 0
                }
            }
            self.save_data()
        return self.users_data[user_id_str]
    
    def add_credits(self, user_id, amount):
        """Ajoute des crédits à un utilisateur"""
        user_data = self.get_user_data(user_id)
        user_data["credits"] += amount
        self.save_data()
    
    def remove_credits(self, user_id, amount):
        """Retire des crédits à un utilisateur"""
        user_data = self.get_user_data(user_id)
        if user_data["credits"] >= amount:
            user_data["credits"] -= amount
            self.save_data()
            return True
        return False
    
    def draw_card(self):
        """Tire une carte aléatoire selon les probabilités"""
        rand = random.random()
        cumulative = 0
        
        for rarity, data in CARD_DATABASE.items():
            cumulative += data["drop_rate"]
            if rand <= cumulative:
                card = random.choice(data["cards"]).copy()
                card["id"] = f"{card['name']}_{datetime.now().timestamp()}"
                return card
        
        # Par défaut, retourne une carte commune
        card = random.choice(CARD_DATABASE["Commune"]["cards"]).copy()
        card["id"] = f"{card['name']}_{datetime.now().timestamp()}"
        return card
    
    def add_card_to_collection(self, user_id, card):
        """Ajoute une carte à la collection d'un utilisateur"""
        user_data = self.get_user_data(user_id)
        user_data["collection"].append(card)
        user_data["stats"]["cards_collected"] += 1
        self.save_data()
    
    def open_pack(self, user_id, pack_type):
        """Ouvre un pack de cartes"""
        pack_info = PACK_PRICES.get(pack_type)
        if not pack_info:
            return None, "Type de pack invalide"
        
        user_data = self.get_user_data(user_id)
        
        # Vérifier si l'utilisateur a assez de crédits
        if user_data["credits"] < pack_info["price"]:
            return None, f"Crédits insuffisants. Vous avez {user_data['credits']} CC, il en faut {pack_info['price']} CC."
        
        # Retirer les crédits
        self.remove_credits(user_id, pack_info["price"])
        
        # Tirer les cartes
        cards = []
        for _ in range(pack_info["cards"]):
            card = self.draw_card()
            self.add_card_to_collection(user_id, card)
            cards.append(card)
        
        user_data["stats"]["packs_opened"] += 1
        self.save_data()
        
        return cards, None
    
    def get_collection(self, user_id):
        """Récupère la collection d'un utilisateur"""
        user_data = self.get_user_data(user_id)
        return user_data["collection"]
    
    def claim_daily_reward(self, user_id):
        """Récompense quotidienne"""
        user_data = self.get_user_data(user_id)
        now = datetime.now()
        
        if user_data["daily_claimed"]:
            last_claim = datetime.fromisoformat(user_data["daily_claimed"])
            if (now - last_claim) < timedelta(hours=24):
                time_left = timedelta(hours=24) - (now - last_claim)
                hours = time_left.seconds // 3600
                minutes = (time_left.seconds % 3600) // 60
                return None, f"Vous avez déjà réclamé votre récompense quotidienne. Revenez dans {hours}h {minutes}m."
        
        # Donner la récompense
        reward = 100
        self.add_credits(user_id, reward)
        user_data["daily_claimed"] = now.isoformat()
        self.save_data()
        
        return reward, None

def setup_card_commands(bot):
    card_system = CardSystem()
    
    # Dictionnaire pour stocker les propositions d'échange en attente
    pending_trades = {}
    
    @bot.command(name='daily')
    async def daily_reward(ctx):
        """Récompense quotidienne"""
        reward, error = card_system.claim_daily_reward(ctx.author.id)
        
        if error:
            await ctx.send(f"❌ {error}")
            return
        
        embed = discord.Embed(
            title="🎁 Récompense Quotidienne",
            description=f"Vous avez reçu **{reward} Crédits Catenaccio (CC)** !",
            color=GREEN_COLOR
        )
        embed.set_footer(text="Revenez demain pour votre prochaine récompense !")
        await ctx.send(embed=embed)
    
    @bot.command(name='balance')
    async def check_balance(ctx):
        """Affiche le solde de crédits"""
        user_data = card_system.get_user_data(ctx.author.id)
        
        embed = discord.Embed(
            title="💰 Vos Crédits Catenaccio",
            description=f"**{user_data['credits']} CC**",
            color=GREEN_COLOR
        )
        embed.add_field(
            name="📊 Statistiques",
            value=(
                f"Packs ouverts: {user_data['stats']['packs_opened']}\n"
                f"Cartes collectées: {user_data['stats']['cards_collected']}\n"
                f"Échanges effectués: {user_data['stats']['trades_completed']}"
            ),
            inline=False
        )
        await ctx.send(embed=embed)
    
    @bot.command(name='shop')
    async def shop(ctx):
        """Affiche la boutique de packs"""
        embed = discord.Embed(
            title="🛒 Boutique de Packs",
            description="Utilisez `a!open_pack <type>` pour ouvrir un pack",
            color=DARK_BLUE_COLOR
        )
        
        for pack_id, pack_info in PACK_PRICES.items():
            if pack_id != "événement":
                embed.add_field(
                    name=f"📦 {pack_info['name']}",
                    value=f"Prix: **{pack_info['price']} CC**\n{pack_info['cards']} cartes",
                    inline=True
                )
        
        await ctx.send(embed=embed)
    
    @bot.command(name='open_pack')
    async def open_pack(ctx, pack_type: str = "basique"):
        """Ouvre un pack de cartes"""
        pack_type = pack_type.lower()
        
        cards, error = card_system.open_pack(ctx.author.id, pack_type)
        
        if error:
            await ctx.send(f"❌ {error}")
            return
        
        # Créer l'embed avec les cartes obtenues
        pack_info = PACK_PRICES[pack_type]
        embed = discord.Embed(
            title=f"📦 {pack_info['name']} ouvert !",
            description="Voici vos nouvelles cartes :",
            color=DARK_BLUE_COLOR
        )
        
        # Grouper les cartes par rareté pour l'affichage
        rarity_colors = {
            "Commune": "⚪",
            "Rare": "🔵",
            "Épique": "🟣",
            "Légendaire": "🟠",
            "Mythique": "🔴"
        }
        
        for card in cards:
            rarity_icon = rarity_colors.get(card['rarity'], "⚪")
            embed.add_field(
                name=f"{rarity_icon} {card['name']}",
                value=f"{card['emoji']} {card['type']} | {card['rarity']}",
                inline=False
            )
        
        user_data = card_system.get_user_data(ctx.author.id)
        embed.set_footer(text=f"Crédits restants: {user_data['credits']} CC")
        
        await ctx.send(embed=embed)
    
    @bot.command(name='collection')
    async def view_collection(ctx, user: discord.User = None):
        """Affiche la collection de cartes"""
        target_user = user or ctx.author
        collection = card_system.get_collection(target_user.id)
        
        if not collection:
            await ctx.send(f"{'Vous n\'avez' if target_user == ctx.author else f'{target_user.name} n\'a'} aucune carte dans {'votre' if target_user == ctx.author else 'sa'} collection.")
            return
        
        # Compter les cartes par rareté
        rarity_count = {}
        for card in collection:
            rarity = card['rarity']
            rarity_count[rarity] = rarity_count.get(rarity, 0) + 1
        
        embed = discord.Embed(
            title=f"📚 Collection de {target_user.name}",
            description=f"Total: **{len(collection)} cartes**",
            color=GREEN_COLOR
        )
        
        # Afficher le résumé par rareté
        for rarity in ["Mythique", "Légendaire", "Épique", "Rare", "Commune"]:
            if rarity in rarity_count:
                embed.add_field(
                    name=f"{rarity}",
                    value=f"{rarity_count[rarity]} cartes",
                    inline=True
                )
        
        # Afficher les 10 dernières cartes obtenues
        recent_cards = collection[-10:]
        if recent_cards:
            cards_text = "\n".join([f"{card['emoji']} {card['name']} ({card['rarity']})" for card in reversed(recent_cards)])
            embed.add_field(
                name="🆕 Cartes récentes",
                value=cards_text,
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @bot.command(name='trade')
    async def trade_offer(ctx, target_user: discord.User, card_index: int, credits: int = 0):
        """Propose un échange à un autre joueur"""
        if target_user.id == ctx.author.id:
            await ctx.send("❌ Vous ne pouvez pas échanger avec vous-même !")
            return
        
        if target_user.bot:
            await ctx.send("❌ Vous ne pouvez pas échanger avec un bot !")
            return
        
        # Vérifier que l'utilisateur a la carte
        collection = card_system.get_collection(ctx.author.id)
        
        if card_index < 1 or card_index > len(collection):
            await ctx.send(f"❌ Index de carte invalide. Vous avez {len(collection)} cartes.")
            return
        
        card = collection[card_index - 1]
        
        # Vérifier les crédits
        if credits > 0:
            user_data = card_system.get_user_data(ctx.author.id)
            if user_data['credits'] < credits:
                await ctx.send(f"❌ Vous n'avez pas assez de crédits. Vous avez {user_data['credits']} CC.")
                return
        
        # Créer la proposition d'échange
        trade_id = f"{ctx.author.id}_{target_user.id}_{datetime.now().timestamp()}"
        pending_trades[trade_id] = {
            "from_user": ctx.author.id,
            "to_user": target_user.id,
            "card": card,
            "card_index": card_index - 1,
            "credits": credits,
            "timestamp": datetime.now()
        }
        
        # Créer l'embed de proposition
        embed = discord.Embed(
            title="💱 Proposition d'Échange",
            description=f"{ctx.author.mention} vous propose un échange !",
            color=DARK_BLUE_COLOR
        )
        
        embed.add_field(
            name="📇 Carte proposée",
            value=f"{card['emoji']} **{card['name']}**\n{card['type']} | {card['rarity']}",
            inline=False
        )
        
        if credits > 0:
            embed.add_field(
                name="💰 Crédits offerts",
                value=f"**{credits} CC**",
                inline=False
            )
        
        embed.add_field(
            name="✅ Pour accepter",
            value=f"Utilisez `a!accept_trade {ctx.author.id}`",
            inline=False
        )
        
        embed.add_field(
            name="❌ Pour refuser",
            value=f"Utilisez `a!decline_trade {ctx.author.id}`",
            inline=False
        )
        
        embed.set_footer(text="Cette offre expire dans 5 minutes")
        
        await ctx.send(f"{target_user.mention}", embed=embed)
        await ctx.send(f"✅ Votre proposition d'échange a été envoyée à {target_user.name} !")
    
    @bot.command(name='accept_trade')
    async def accept_trade(ctx, from_user_id: int):
        """Accepte une proposition d'échange"""
        # Trouver l'échange en attente
        trade = None
        trade_id_to_remove = None
        
        for tid, t in pending_trades.items():
            if t["from_user"] == from_user_id and t["to_user"] == ctx.author.id:
                trade = t
                trade_id_to_remove = tid
                break
        
        if not trade:
            await ctx.send("❌ Aucune proposition d'échange trouvée de cet utilisateur.")
            return
        
        # Vérifier que l'échange n'a pas expiré (5 minutes)
        if (datetime.now() - trade["timestamp"]) > timedelta(minutes=5):
            del pending_trades[trade_id_to_remove]
            await ctx.send("❌ Cette proposition d'échange a expiré.")
            return
        
        # Effectuer l'échange
        from_user_data = card_system.get_user_data(trade["from_user"])
        to_user_data = card_system.get_user_data(ctx.author.id)
        
        # Vérifier que l'utilisateur qui offre a toujours la carte et les crédits
        if trade["card_index"] >= len(from_user_data["collection"]):
            del pending_trades[trade_id_to_remove]
            await ctx.send("❌ La carte proposée n'est plus disponible.")
            return
        
        if from_user_data["credits"] < trade["credits"]:
            del pending_trades[trade_id_to_remove]
            await ctx.send("❌ L'utilisateur n'a plus assez de crédits pour cet échange.")
            return
        
        # Transférer la carte
        card = from_user_data["collection"].pop(trade["card_index"])
        to_user_data["collection"].append(card)
        
        # Transférer les crédits
        if trade["credits"] > 0:
            from_user_data["credits"] -= trade["credits"]
            to_user_data["credits"] += trade["credits"]
        
        # Mettre à jour les statistiques
        from_user_data["stats"]["trades_completed"] += 1
        to_user_data["stats"]["trades_completed"] += 1
        
        card_system.save_data()
        
        # Supprimer l'échange de la liste
        del pending_trades[trade_id_to_remove]
        
        # Notification
        embed = discord.Embed(
            title="✅ Échange Réussi !",
            description=f"L'échange entre <@{trade['from_user']}> et {ctx.author.mention} a été complété !",
            color=GREEN_COLOR
        )
        
        embed.add_field(
            name="📇 Carte échangée",
            value=f"{card['emoji']} **{card['name']}**\n{card['type']} | {card['rarity']}",
            inline=False
        )
        
        if trade["credits"] > 0:
            embed.add_field(
                name="💰 Crédits transférés",
                value=f"**{trade['credits']} CC**",
                inline=False
            )
        
        await ctx.send(embed=embed)
        
        # Notifier l'autre utilisateur
        try:
            from_user = await bot.fetch_user(trade["from_user"])
            await from_user.send(f"✅ Votre échange avec **{ctx.author.name}** a été accepté !")
        except:
            pass
    
    @bot.command(name='decline_trade')
    async def decline_trade(ctx, from_user_id: int):
        """Refuse une proposition d'échange"""
        # Trouver et supprimer l'échange
        trade_found = False
        trade_id_to_remove = None
        
        for tid, t in pending_trades.items():
            if t["from_user"] == from_user_id and t["to_user"] == ctx.author.id:
                trade_found = True
                trade_id_to_remove = tid
                break
        
        if not trade_found:
            await ctx.send("❌ Aucune proposition d'échange trouvée de cet utilisateur.")
            return
        
        del pending_trades[trade_id_to_remove]
        await ctx.send("✅ Vous avez refusé la proposition d'échange.")
        
        # Notifier l'autre utilisateur
        try:
            from_user = await bot.fetch_user(from_user_id)
            await from_user.send(f"❌ **{ctx.author.name}** a refusé votre proposition d'échange.")
        except:
            pass
    
    @bot.command(name='give_credits')
    @commands.has_permissions(administrator=True)
    async def give_credits(ctx, user: discord.User, amount: int):
        """[ADMIN] Donne des crédits à un utilisateur"""
        card_system.add_credits(user.id, amount)
        await ctx.send(f"✅ {amount} CC ont été donnés à {user.mention}.")
    
    @bot.command(name='reset_collection')
    @commands.has_permissions(administrator=True)
    async def reset_collection(ctx, user: discord.User):
        """[ADMIN] Réinitialise la collection d'un utilisateur"""
        user_id_str = str(user.id)
        if user_id_str in card_system.users_data:
            del card_system.users_data[user_id_str]
            card_system.save_data()
            await ctx.send(f"✅ La collection de {user.mention} a été réinitialisée.")
        else:
            await ctx.send(f"❌ {user.mention} n'a pas de collection.")
    
    @bot.command(name='card_help')
    async def card_help(ctx):
        """Affiche l'aide du système de cartes"""
        embed = discord.Embed(
            title="🎴 Guide du Système de Cartes Catenaccio",
            description="Collectionnez des cartes de joueurs et échangez-les avec vos amis !",
            color=GREEN_COLOR
        )
        
        embed.add_field(
            name="💰 Commandes de Base",
            value=(
                "`a!daily` - Récompense quotidienne\n"
                "`a!balance` - Voir vos crédits\n"
                "`a!shop` - Voir la boutique de packs"
            ),
            inline=False
        )
        
        embed.add_field(
            name="📦 Ouvrir des Packs",
            value=(
                "`a!open_pack <type>` - Ouvrir un pack\n"
                "Types: basique, argent, or, platine"
            ),
            inline=False
        )
        
        embed.add_field(
            name="📚 Collection",
            value=(
                "`a!collection` - Voir votre collection\n"
                "`a!collection @utilisateur` - Voir la collection d'un autre joueur"
            ),
            inline=False
        )
        
        embed.add_field(
            name="💱 Échanges",
            value=(
                "`a!trade @utilisateur <numéro_carte> [crédits]` - Proposer un échange\n"
                "`a!accept_trade <id_utilisateur>` - Accepter un échange\n"
                "`a!decline_trade <id_utilisateur>` - Refuser un échange"
            ),
            inline=False
        )
        
        embed.set_footer(text="Bonne collection ! ⚽🎴")
        
        await ctx.send(embed=embed)