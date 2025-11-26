import discord
from discord.ext import commands
import json
import random
from datetime import datetime, timedelta
from config import GREEN_COLOR, DARK_BLUE_COLOR

# Configuration des cartes
CARD_TYPES = {
    "Commune": {"color": 0x808080, "emoji": "⚪", "drop_rate": 0.70, "sell_value": 10},
    "Rare": {"color": 0x0099FF, "emoji": "🔵", "drop_rate": 0.20, "sell_value": 50},
    "Épique": {"color": 0x9D00FF, "emoji": "🟣", "drop_rate": 0.07, "sell_value": 150},
    "Légendaire": {"color": 0xFFD700, "emoji": "🟡", "drop_rate": 0.025, "sell_value": 500},
    "Mythique": {"color": 0xFF0000, "emoji": "🔴", "drop_rate": 0.005, "sell_value": 1500}
}

PLAYER_POSITIONS = ["Défense", "Milieu", "Attaque", "Gardien", "Technique"]

# Base de données de joueurs (à enrichir)
PLAYERS_DB = [
    # Défenseurs
    {"name": "Araki", "position": "Défense", "rarity": "Mythique"},
    {"name": "Matsumoto", "position": "Défense", "rarity": "Légendaire"},
    {"name": "Tanaka", "position": "Défense", "rarity": "Épique"},
    {"name": "Yamada", "position": "Défense", "rarity": "Rare"},
    {"name": "Sato", "position": "Défense", "rarity": "Commune"},
    {"name": "Kobayashi", "position": "Défense", "rarity": "Commune"},
    
    # Milieux
    {"name": "Nakamura", "position": "Milieu", "rarity": "Légendaire"},
    {"name": "Ito", "position": "Milieu", "rarity": "Épique"},
    {"name": "Watanabe", "position": "Milieu", "rarity": "Rare"},
    {"name": "Suzuki", "position": "Milieu", "rarity": "Commune"},
    
    # Attaquants
    {"name": "Takahashi", "position": "Attaque", "rarity": "Légendaire"},
    {"name": "Kato", "position": "Attaque", "rarity": "Épique"},
    {"name": "Yoshida", "position": "Attaque", "rarity": "Rare"},
    {"name": "Mori", "position": "Attaque", "rarity": "Commune"},
    
    # Gardiens
    {"name": "Fujita", "position": "Gardien", "rarity": "Épique"},
    {"name": "Ishikawa", "position": "Gardien", "rarity": "Rare"},
    {"name": "Kimura", "position": "Gardien", "rarity": "Commune"},
    
    # Technique
    {"name": "Catenaccio", "position": "Technique", "rarity": "Mythique"},
    {"name": "Tiki-Taka", "position": "Technique", "rarity": "Légendaire"},
    {"name": "Contre-attaque", "position": "Technique", "rarity": "Épique"},
    {"name": "Pressing", "position": "Technique", "rarity": "Rare"},
]

class CardSystem:
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "card_data.json"
        self.load_data()
        
    def load_data(self):
        """Charge les données depuis le fichier JSON"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {
                "users": {},
                "trades": {},
                "daily_claims": {}
            }
            self.save_data()
    
    def save_data(self):
        """Sauvegarde les données dans le fichier JSON"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
    
    def get_user_data(self, user_id):
        """Récupère les données d'un utilisateur"""
        user_id = str(user_id)
        if user_id not in self.data["users"]:
            self.data["users"][user_id] = {
                "credits": 100,
                "collection": [],
                "packs_opened": 0,
                "last_daily": None
            }
            self.save_data()
        return self.data["users"][user_id]
    
    def generate_card(self):
        """Génère une carte aléatoire selon les taux de drop"""
        rand = random.random()
        cumulative = 0
        
        for rarity, info in CARD_TYPES.items():
            cumulative += info["drop_rate"]
            if rand <= cumulative:
                # Filtrer les joueurs de cette rareté
                available = [p for p in PLAYERS_DB if p["rarity"] == rarity]
                if available:
                    player = random.choice(available)
                    return {
                        "name": player["name"],
                        "position": player["position"],
                        "rarity": rarity,
                        "id": f"{player['name']}_{rarity}_{random.randint(1000, 9999)}",
                        "obtained_at": datetime.now().isoformat()
                    }
        
        # Fallback sur Commune
        player = random.choice([p for p in PLAYERS_DB if p["rarity"] == "Commune"])
        return {
            "name": player["name"],
            "position": player["position"],
            "rarity": "Commune",
            "id": f"{player['name']}_Commune_{random.randint(1000, 9999)}",
            "obtained_at": datetime.now().isoformat()
        }
    
    def create_card_embed(self, card):
        """Crée un embed pour afficher une carte"""
        rarity_info = CARD_TYPES[card["rarity"]]
        
        embed = discord.Embed(
            title=f"{rarity_info['emoji']} {card['name']}",
            description=f"**Position:** {card['position']}\n**Rareté:** {card['rarity']}",
            color=rarity_info["color"]
        )
        
        embed.add_field(
            name="💰 Valeur de revente",
            value=f"{rarity_info['sell_value']} crédits",
            inline=True
        )
        
        embed.add_field(
            name="🆔 ID",
            value=f"`{card['id']}`",
            inline=True
        )
        
        embed.set_footer(text=f"Collection Catenaccio • {card['rarity']}")
        
        return embed

def setup_card_commands(bot):
    card_system = CardSystem(bot)
    
    @bot.command(name='card_help')
    async def card_help(ctx):
        """Affiche l'aide du système de cartes"""
        embed = discord.Embed(
            title="🎴 Guide du Système de Cartes Catenaccio",
            description=(
                "Bienvenue dans le système de collection de cartes !\n"
                "Collectionnez vos joueurs préférés et échangez avec la communauté."
            ),
            color=GREEN_COLOR
        )
        
        # Système de base
        embed.add_field(
            name="💳 Système de base",
            value=(
                "`a!daily` - Récompense quotidienne\n"
                "`a!balance` - Voir vos crédits\n"
                "`a!shop` - Boutique de packs\n"
                "`a!open_pack <type>` - Ouvrir un pack\n"
            ),
            inline=False
        )
        
        # Collection
        embed.add_field(
            name="📚 Collection",
            value=(
                "`a!collection` - Voir votre collection\n"
                "`a!card <id>` - Détails d'une carte\n"
                "`a!sell <id>` - Vendre une carte\n"
            ),
            inline=False
        )
        
        # Échanges
        embed.add_field(
            name="🔄 Échanges",
            value=(
                "`a!trade @user <votre_id> <leurs_credits>` - Échanger une carte\n"
                "`a!transfer @user <credits>` - Transférer des crédits\n"
                "`a!trade_accept` - Accepter un échange\n"
                "`a!trade_cancel` - Annuler un échange\n"
            ),
            inline=False
        )
        
        # Raretés
        rarities_text = ""
        for rarity, info in CARD_TYPES.items():
            rarities_text += f"{info['emoji']} **{rarity}** - {int(info['drop_rate']*100)}% • {info['sell_value']} crédits\n"
        
        embed.add_field(
            name="⭐ Raretés des cartes",
            value=rarities_text,
            inline=False
        )
        
        embed.set_footer(text="Bonne collection ! ⚽🎴")
        
        await ctx.send(embed=embed)
    
    @bot.command(name='daily')
    async def daily_reward(ctx):
        """Récompense quotidienne"""
        user_data = card_system.get_user_data(ctx.author.id)
        
        # Vérifier si déjà réclamé aujourd'hui
        last_daily = user_data.get("last_daily")
        if last_daily:
            last_date = datetime.fromisoformat(last_daily)
            if datetime.now() - last_date < timedelta(hours=24):
                time_left = timedelta(hours=24) - (datetime.now() - last_date)
                hours = int(time_left.seconds / 3600)
                minutes = int((time_left.seconds % 3600) / 60)
                
                embed = discord.Embed(
                    title="⏰ Déjà réclamé !",
                    description=f"Revenez dans **{hours}h {minutes}min** pour votre récompense quotidienne.",
                    color=0xFF0000
                )
                await ctx.send(embed=embed)
                return
        
        # Donner la récompense
        reward = 50
        user_data["credits"] += reward
        user_data["last_daily"] = datetime.now().isoformat()
        card_system.save_data()
        
        embed = discord.Embed(
            title="🎁 Récompense quotidienne !",
            description=f"Vous avez reçu **{reward} crédits** !\n\n💰 Nouveau solde : **{user_data['credits']} crédits**",
            color=GREEN_COLOR
        )
        embed.set_footer(text="Revenez demain pour une nouvelle récompense !")
        
        await ctx.send(embed=embed)
    
    @bot.command(name='balance')
    async def balance(ctx, member: discord.Member = None):
        """Affiche le solde de crédits"""
        target = member or ctx.author
        user_data = card_system.get_user_data(target.id)
        
        embed = discord.Embed(
            title=f"💰 Solde de {target.display_name}",
            description=f"**{user_data['credits']} crédits**",
            color=DARK_BLUE_COLOR
        )
        
        embed.add_field(
            name="📦 Packs ouverts",
            value=str(user_data["packs_opened"]),
            inline=True
        )
        
        embed.add_field(
            name="🎴 Cartes possédées",
            value=str(len(user_data["collection"])),
            inline=True
        )
        
        await ctx.send(embed=embed)
    
    @bot.command(name='shop')
    async def shop(ctx):
        """Affiche la boutique de packs"""
        embed = discord.Embed(
            title="🏪 Boutique de Packs Catenaccio",
            description="Achetez des packs pour agrandir votre collection !",
            color=GREEN_COLOR
        )
        
        embed.add_field(
            name="📦 Pack Plata (100 CC)",
            value="• 3 cartes communes garanties\n• Utilisez `a!open_pack plata`",
            inline=False
        )
        
        embed.add_field(
            name="💎 Pack Argent (250 CC)",
            value="• 5 cartes dont 1 rare minimum\n• Utilisez `a!open_pack argent`",
            inline=False
        )
        
        embed.add_field(
            name="👑 Pack Or (500 CC)",
            value="• 7 cartes dont 1 épique minimum\n• Utilisez `a!open_pack or`",
            inline=False
        )
        
        embed.add_field(
            name="🌟 Pack Platine (1000 CC)",
            value="• 10 cartes dont 1 légendaire minimum\n• Utilisez `a!open_pack platine`",
            inline=False
        )
        
        embed.add_field(
            name="⚡ Pack Événement",
            value="• Disponible lors d'événements spéciaux\n• Contenu variable",
            inline=False
        )
        
        embed.set_footer(text="CC = Crédits Catenaccio")
        
        await ctx.send(embed=embed)
    
    @bot.command(name='open_pack')
    async def open_pack(ctx, pack_type: str):
        """Ouvre un pack de cartes"""
        user_data = card_system.get_user_data(ctx.author.id)
        
        packs = {
            "plata": {"cost": 100, "cards": 3, "guaranteed": None},
            "argent": {"cost": 250, "cards": 5, "guaranteed": "Rare"},
            "or": {"cost": 500, "cards": 7, "guaranteed": "Épique"},
            "platine": {"cost": 1000, "cards": 10, "guaranteed": "Légendaire"}
        }
        
        pack_type = pack_type.lower()
        
        if pack_type not in packs:
            await ctx.send("❌ Type de pack invalide ! Utilisez : plata, argent, or ou platine")
            return
        
        pack = packs[pack_type]
        
        if user_data["credits"] < pack["cost"]:
            embed = discord.Embed(
                title="❌ Crédits insuffisants",
                description=f"Il vous faut **{pack['cost']} crédits** pour ce pack.\nVous avez : **{user_data['credits']} crédits**",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return
        
        # Déduire le coût
        user_data["credits"] -= pack["cost"]
        user_data["packs_opened"] += 1
        
        # Générer les cartes
        cards = []
        for i in range(pack["cards"]):
            if i == 0 and pack["guaranteed"]:
                # Première carte garantie
                available = [p for p in PLAYERS_DB if p["rarity"] == pack["guaranteed"] or 
                           (pack["guaranteed"] == "Légendaire" and p["rarity"] == "Mythique")]
                player = random.choice(available)
                card = {
                    "name": player["name"],
                    "position": player["position"],
                    "rarity": player["rarity"],
                    "id": f"{player['name']}_{player['rarity']}_{random.randint(1000, 9999)}",
                    "obtained_at": datetime.now().isoformat()
                }
            else:
                card = card_system.generate_card()
            
            cards.append(card)
            user_data["collection"].append(card)
        
        card_system.save_data()
        
        # Afficher l'ouverture
        embed = discord.Embed(
            title=f"📦 Ouverture du Pack {pack_type.capitalize()} !",
            description=f"Vous avez ouvert **{pack['cards']} cartes** !\n\n━━━━━━━━━━━━━━━━━━━━",
            color=GREEN_COLOR
        )
        
        for card in cards:
            rarity_info = CARD_TYPES[card["rarity"]]
            embed.add_field(
                name=f"{rarity_info['emoji']} {card['name']}",
                value=f"{card['position']} • {card['rarity']}\n`{card['id']}`",
                inline=True
            )
        
        embed.add_field(
            name="━━━━━━━━━━━━━━━━━━━━",
            value=f"💰 Crédits restants : **{user_data['credits']} CC**",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @bot.command(name='collection')
    async def collection(ctx, member: discord.Member = None):
        """Affiche la collection d'un joueur"""
        target = member or ctx.author
        user_data = card_system.get_user_data(target.id)
        
        if not user_data["collection"]:
            embed = discord.Embed(
                title="📚 Collection vide",
                description="Aucune carte dans la collection. Achetez des packs dans la boutique !",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return
        
        # Grouper par rareté
        by_rarity = {}
        for card in user_data["collection"]:
            rarity = card["rarity"]
            if rarity not in by_rarity:
                by_rarity[rarity] = []
            by_rarity[rarity].append(card)
        
        embed = discord.Embed(
            title=f"📚 Collection de {target.display_name}",
            description=f"**{len(user_data['collection'])} cartes** au total\n━━━━━━━━━━━━━━━━━━━━",
            color=DARK_BLUE_COLOR
        )
        
        # Afficher par rareté (du plus rare au plus commun)
        rarity_order = ["Mythique", "Légendaire", "Épique", "Rare", "Commune"]
        
        for rarity in rarity_order:
            if rarity in by_rarity:
                cards_list = by_rarity[rarity]
                rarity_info = CARD_TYPES[rarity]
                
                # Limiter à 5 cartes par rareté pour l'affichage
                display_cards = cards_list[:5]
                cards_text = "\n".join([f"• {c['name']} ({c['position']})" for c in display_cards])
                
                if len(cards_list) > 5:
                    cards_text += f"\n... et {len(cards_list) - 5} autres"
                
                embed.add_field(
                    name=f"{rarity_info['emoji']} {rarity} ({len(cards_list)})",
                    value=cards_text,
                    inline=False
                )
        
        embed.set_footer(text=f"Utilisez a!card <id> pour voir les détails d'une carte")
        
        await ctx.send(embed=embed)
    
    @bot.command(name='card')
    async def card_details(ctx, card_id: str):
        """Affiche les détails d'une carte"""
        user_data = card_system.get_user_data(ctx.author.id)
        
        card = next((c for c in user_data["collection"] if c["id"] == card_id), None)
        
        if not card:
            await ctx.send("❌ Carte non trouvée dans votre collection !")
            return
        
        embed = card_system.create_card_embed(card)
        
        obtained_date = datetime.fromisoformat(card["obtained_at"])
        embed.add_field(
            name="📅 Obtenue le",
            value=obtained_date.strftime("%d/%m/%Y à %H:%M"),
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @bot.command(name='sell')
    async def sell_card(ctx, card_id: str):
        """Vend une carte"""
        user_data = card_system.get_user_data(ctx.author.id)
        
        card = next((c for c in user_data["collection"] if c["id"] == card_id), None)
        
        if not card:
            await ctx.send("❌ Carte non trouvée dans votre collection !")
            return
        
        # Retirer la carte et donner les crédits
        user_data["collection"].remove(card)
        sell_value = CARD_TYPES[card["rarity"]]["sell_value"]
        user_data["credits"] += sell_value
        card_system.save_data()
        
        embed = discord.Embed(
            title="✅ Carte vendue !",
            description=f"Vous avez vendu **{card['name']}** ({card['rarity']}) pour **{sell_value} crédits**.",
            color=GREEN_COLOR
        )
        
        embed.add_field(
            name="💰 Nouveau solde",
            value=f"{user_data['credits']} crédits",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @bot.command(name='trade')
    async def trade(ctx, member: discord.Member, card_id: str, credits: int):
        """Propose un échange de carte contre des crédits"""
        if member.id == ctx.author.id:
            await ctx.send("❌ Vous ne pouvez pas échanger avec vous-même !")
            return
        
        if credits < 0:
            await ctx.send("❌ Le montant doit être positif !")
            return
        
        sender_data = card_system.get_user_data(ctx.author.id)
        receiver_data = card_system.get_user_data(member.id)
        
        # Vérifier que la carte existe
        card = next((c for c in sender_data["collection"] if c["id"] == card_id), None)
        
        if not card:
            await ctx.send("❌ Carte non trouvée dans votre collection !")
            return
        
        # Vérifier que le receveur a assez de crédits
        if receiver_data["credits"] < credits:
            await ctx.send(f"❌ {member.display_name} n'a pas assez de crédits ! (possède {receiver_data['credits']} CC)")
            return
        
        # Créer la proposition d'échange
        trade_id = f"{ctx.author.id}_{member.id}_{datetime.now().timestamp()}"
        card_system.data["trades"][trade_id] = {
            "sender_id": str(ctx.author.id),
            "receiver_id": str(member.id),
            "card": card,
            "credits": credits,
            "created_at": datetime.now().isoformat()
        }
        card_system.save_data()
        
        embed = discord.Embed(
            title="🔄 Proposition d'échange",
            description=f"{ctx.author.mention} propose un échange à {member.mention} !",
            color=DARK_BLUE_COLOR
        )
        
        card_embed = card_system.create_card_embed(card)
        
        embed.add_field(
            name="📤 Envoi",
            value=f"**Carte :** {card['name']} ({card['rarity']})",
            inline=True
        )
        
        embed.add_field(
            name="📥 Réception",
            value=f"**Crédits :** {credits} CC",
            inline=True
        )
        
        embed.add_field(
            name="━━━━━━━━━━━━━━━━━━━━",
            value=(
                f"{member.mention}, utilisez :\n"
                f"• `a!trade_accept {trade_id}` pour accepter\n"
                f"• `a!trade_cancel {trade_id}` pour refuser"
            ),
            inline=False
        )
        
        embed.set_footer(text=f"ID de l'échange : {trade_id}")
        
        await ctx.send(embed=embed)
    
    @bot.command(name='trade_accept')
    async def trade_accept(ctx, trade_id: str):
        """Accepte un échange"""
        if trade_id not in card_system.data["trades"]:
            await ctx.send("❌ Échange non trouvé ou expiré !")
            return
        
        trade = card_system.data["trades"][trade_id]
        
        if str(ctx.author.id) != trade["receiver_id"]:
            await ctx.send("❌ Cet échange ne vous est pas destiné !")
            return
        
        # Effectuer l'échange
        sender_data = card_system.get_user_data(trade["sender_id"])
        receiver_data = card_system.get_user_data(trade["receiver_id"])
        
        # Vérifier à nouveau les conditions
        card = next((c for c in sender_data["collection"] if c["id"] == trade["card"]["id"]), None)
        
        if not card:
            await ctx.send("❌ La carte n'est plus disponible !")
            del card_system.data["trades"][trade_id]
            card_system.save_data()
            return
        
        if receiver_data["credits"] < trade["credits"]:
            await ctx.send(f"❌ Vous n'avez plus assez de crédits !")
            return
        
        # Transférer
        sender_data["collection"].remove(card)
        receiver_data["collection"].append(card)
        receiver_data["credits"] -= trade["credits"]
        sender_data["credits"] += trade["credits"]
        
        # Supprimer l'échange
        del card_system.data["trades"][trade_id]
        card_system.save_data()
        
        embed = discord.Embed(
            title="✅ Échange réussi !",
            description=f"L'échange entre <@{trade['sender_id']}> et <@{trade['receiver_id']}> a été effectué !",
            color=GREEN_COLOR
        )
        
        embed.add_field(
            name="📤 Transfert",
            value=f"**{card['name']}** → <@{trade['receiver_id']}>\n**{trade['credits']} CC** → <@{trade['sender_id']}>",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @bot.command(name='trade_cancel')
    async def trade_cancel(ctx, trade_id: str):
        """Annule un échange"""
        if trade_id not in card_system.data["trades"]:
            await ctx.send("❌ Échange non trouvé ou expiré !")
            return
        
        trade = card_system.data["trades"][trade_id]
        
        if str(ctx.author.id) not in [trade["sender_id"], trade["receiver_id"]]:
            await ctx.send("❌ Vous n'êtes pas concerné par cet échange !")
            return
        
        del card_system.data["trades"][trade_id]
        card_system.save_data()
        
        embed = discord.Embed(
            title="❌ Échange annulé",
            description="L'échange a été annulé.",
            color=0xFF0000
        )
        
        await ctx.send(embed=embed)
    
    @bot.command(name='transfer')
    async def transfer_credits(ctx, member: discord.Member, credits: int):
        """Transfère des crédits à un autre joueur"""
        if member.id == ctx.author.id:
            await ctx.send("❌ Vous ne pouvez pas vous transférer des crédits !")
            return
        
        if credits <= 0:
            await ctx.send("❌ Le montant doit être positif !")
            return
        
        sender_data = card_system.get_user_data(ctx.author.id)
        receiver_data = card_system.get_user_data(member.id)
        
        if sender_data["credits"] < credits:
            await ctx.send(f"❌ Vous n'avez pas assez de crédits ! (possède {sender_data['credits']} CC)")
            return
        
        # Effectuer le transfert
        sender_data["credits"] -= credits
        receiver_data["credits"] += credits
        card_system.save_data()
        
        embed = discord.Embed(
            title="💸 Transfert effectué !",
            description=f"{ctx.author.mention} a transféré **{credits} crédits** à {member.mention}",
            color=GREEN_COLOR
        )
        
        embed.add_field(
            name="💰 Votre nouveau solde",
            value=f"{sender_data['credits']} CC",
            inline=True
        )
        
        embed.add_field(
            name="💰 Solde du destinataire",
            value=f"{receiver_data['credits']} CC",
            inline=True
        )
        
        await ctx.send(embed=embed)