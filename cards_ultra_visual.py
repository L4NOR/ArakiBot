import discord
from discord.ext import commands
import json
import random
from datetime import datetime, timedelta
from config import GREEN_COLOR, DARK_BLUE_COLOR
from card_visual_generator import card_visual_gen

# Configuration des cartes (identique)
CARD_TYPES = {
    "Commune": {"color": 0x808080, "emoji": "⚪", "drop_rate": 0.70, "sell_value": 10},
    "Rare": {"color": 0x0099FF, "emoji": "🔵", "drop_rate": 0.20, "sell_value": 50},
    "Épique": {"color": 0x9D00FF, "emoji": "🟣", "drop_rate": 0.07, "sell_value": 150},
    "Légendaire": {"color": 0xFFD700, "emoji": "🟡", "drop_rate": 0.025, "sell_value": 500},
    "Mythique": {"color": 0xFF0000, "emoji": "🔴", "drop_rate": 0.005, "sell_value": 1500}
}

STAT_EMOJIS = {
    "vitesse": "⚡", "defense": "🛡️", "attaque": "⚔️",
    "technique": "🎯", "physique": "💪", "mental": "🧠"
}

# Base de données avec URLs d'images (à personnaliser)
PLAYERS_DB = [
    # DÉFENSEURS
    {
        "name": "Araki", "position": "Défense", "rarity": "Mythique",
        "stats": {"vitesse": 88, "defense": 99, "attaque": 75, "technique": 92, "physique": 90, "mental": 95},
        "description": "Le génie tactique de la défense",
        "image_url": "https://i.imgur.com/example1.png",  # Remplacer par vraie URL
        "special_ability": "Catenaccio Perfect",
        "nationality": "🇯🇵 Japon"
    },
    {
        "name": "Matsumoto", "position": "Défense", "rarity": "Légendaire",
        "stats": {"vitesse": 82, "defense": 91, "attaque": 68, "technique": 85, "physique": 88, "mental": 87},
        "description": "Le mur impénétrable",
        "image_url": "https://i.imgur.com/example2.png",
        "special_ability": "Muraille de Fer",
        "nationality": "🇯🇵 Japon"
    },
    {
        "name": "Tanaka", "position": "Défense", "rarity": "Épique",
        "stats": {"vitesse": 78, "defense": 85, "attaque": 62, "technique": 79, "physique": 84, "mental": 80},
        "description": "Spécialiste du marquage",
        "image_url": None,
        "special_ability": "Marquage Serré",
        "nationality": "🇯🇵 Japon"
    },
    {
        "name": "Yamada", "position": "Défense", "rarity": "Rare",
        "stats": {"vitesse": 72, "defense": 78, "attaque": 55, "technique": 70, "physique": 76, "mental": 72},
        "description": "Défenseur polyvalent",
        "image_url": None,
        "special_ability": "Polyvalence",
        "nationality": "🇯🇵 Japon"
    },
    {
        "name": "Sato", "position": "Défense", "rarity": "Commune",
        "stats": {"vitesse": 65, "defense": 70, "attaque": 48, "technique": 62, "physique": 68, "mental": 65},
        "description": "Jeune espoir défensif",
        "image_url": None,
        "special_ability": "Détermination",
        "nationality": "🇯🇵 Japon"
    },
    
    # MILIEUX
    {
        "name": "Nakamura", "position": "Milieu", "rarity": "Légendaire",
        "stats": {"vitesse": 86, "defense": 80, "attaque": 88, "technique": 93, "physique": 82, "mental": 90},
        "description": "Maestro du milieu de terrain",
        "image_url": "https://i.imgur.com/example3.png",
        "special_ability": "Vision de Jeu",
        "nationality": "🇯🇵 Japon"
    },
    {
        "name": "Ito", "position": "Milieu", "rarity": "Épique",
        "stats": {"vitesse": 80, "defense": 75, "attaque": 82, "technique": 86, "physique": 78, "mental": 83},
        "description": "Récupérateur infatigable",
        "image_url": None,
        "special_ability": "Endurance Infinie",
        "nationality": "🇯🇵 Japon"
    },
    {
        "name": "Watanabe", "position": "Milieu", "rarity": "Rare",
        "stats": {"vitesse": 74, "defense": 70, "attaque": 76, "technique": 80, "physique": 72, "mental": 75},
        "description": "Milieu box-to-box",
        "image_url": None,
        "special_ability": "Course Explosive",
        "nationality": "🇯🇵 Japon"
    },
    
    # ATTAQUANTS
    {
        "name": "Takahashi", "position": "Attaque", "rarity": "Légendaire",
        "stats": {"vitesse": 94, "defense": 58, "attaque": 96, "technique": 90, "physique": 80, "mental": 88},
        "description": "Le finisseur ultime",
        "image_url": "https://i.imgur.com/example4.png",
        "special_ability": "Instinct du Buteur",
        "nationality": "🇯🇵 Japon"
    },
    {
        "name": "Kato", "position": "Attaque", "rarity": "Épique",
        "stats": {"vitesse": 88, "defense": 52, "attaque": 89, "technique": 84, "physique": 76, "mental": 82},
        "description": "Attaquant rapide et technique",
        "image_url": None,
        "special_ability": "Vitesse Éclair",
        "nationality": "🇯🇵 Japon"
    },
    
    # GARDIENS
    {
        "name": "Fujita", "position": "Gardien", "rarity": "Épique",
        "stats": {"vitesse": 70, "defense": 92, "attaque": 45, "technique": 88, "physique": 85, "mental": 91},
        "description": "Gardien aux réflexes exceptionnels",
        "image_url": None,
        "special_ability": "Réflexes Surhumains",
        "nationality": "🇯🇵 Japon"
    },
    
    # TECHNIQUES
    {
        "name": "Catenaccio", "position": "Technique", "rarity": "Mythique",
        "stats": {"vitesse": 75, "defense": 99, "attaque": 65, "technique": 98, "physique": 80, "mental": 97},
        "description": "La tactique défensive ultime",
        "image_url": "https://i.imgur.com/example5.png",
        "special_ability": "Défense Absolue",
        "nationality": "🇮🇹 Italie"
    },
    {
        "name": "Tiki-Taka", "position": "Technique", "rarity": "Légendaire",
        "stats": {"vitesse": 82, "defense": 70, "attaque": 88, "technique": 96, "physique": 75, "mental": 92},
        "description": "Possession et passes courtes",
        "image_url": None,
        "special_ability": "Possession Totale",
        "nationality": "🇪🇸 Espagne"
    },
]

class CardSystem:
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "card_data.json"
        self.load_data()
        
    def load_data(self):
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {"users": {}, "trades": {}, "daily_claims": {}}
            self.save_data()
    
    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
    
    def get_user_data(self, user_id):
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
        rand = random.random()
        cumulative = 0
        
        for rarity, info in CARD_TYPES.items():
            cumulative += info["drop_rate"]
            if rand <= cumulative:
                available = [p for p in PLAYERS_DB if p["rarity"] == rarity]
                if available:
                    player = random.choice(available)
                    return {
                        "name": player["name"],
                        "position": player["position"],
                        "rarity": rarity,
                        "stats": player["stats"],
                        "description": player["description"],
                        "image_url": player["image_url"],
                        "special_ability": player["special_ability"],
                        "nationality": player["nationality"],
                        "id": f"{player['name']}_{rarity}_{random.randint(1000, 9999)}",
                        "obtained_at": datetime.now().isoformat()
                    }
        
        player = random.choice([p for p in PLAYERS_DB if p["rarity"] == "Commune"])
        return {
            "name": player["name"], "position": player["position"], "rarity": "Commune",
            "stats": player["stats"], "description": player["description"],
            "image_url": player["image_url"], "special_ability": player["special_ability"],
            "nationality": player["nationality"],
            "id": f"{player['name']}_Commune_{random.randint(1000, 9999)}",
            "obtained_at": datetime.now().isoformat()
        }
    
    def get_overall_rating(self, stats):
        return sum(stats.values()) // len(stats) if stats else 0

def setup_card_commands(bot):
    card_system = CardSystem(bot)
    
    @bot.command(name='card_help')
    async def card_help(ctx):
        embed = discord.Embed(
            title="🎴 Guide du Système de Cartes Catenaccio",
            description=(
                "Bienvenue dans le système de collection de cartes ULTRA VISUELLES !\n"
                "Chaque carte est maintenant une vraie ŒUVRE D'ART générée en temps réel !\n\n"
                "✨ **NOUVEAU** : Cartes visuelles haute qualité avec images, stats et effets !"
            ),
            color=GREEN_COLOR
        )
        
        embed.add_field(
            name="💳 Commandes de Base",
            value=(
                "`a!daily` - Récompense quotidienne (50 CC)\n"
                "`a!balance` - Voir vos crédits et stats\n"
                "`a!shop` - Voir la boutique de packs\n"
                "`a!open_pack <type>` - Ouvrir un pack (plata/argent/or/platine)\n"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🎨 Collection & Visuels",
            value=(
                "`a!card <id>` - **Voir l'IMAGE COMPLÈTE** d'une carte\n"
                "`a!card_visual <id>` - Générer l'image HD de la carte\n"
                "`a!collection` - Liste de vos cartes\n"
                "`a!top_cards` - Vos 10 meilleures cartes\n"
                "`a!gallery` - **NOUVEAU** : Galerie visuelle de vos meilleures cartes\n"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🔄 Échanges & Vente",
            value=(
                "`a!sell <id>` - Vendre une carte\n"
                "`a!trade @user <id> <credits>` - Proposer un échange\n"
                "`a!trade_accept <id>` - Accepter un échange\n"
                "`a!transfer @user <credits>` - Donner des crédits\n"
            ),
            inline=False
        )
        
        rarities_text = ""
        for rarity, info in CARD_TYPES.items():
            rarities_text += f"{info['emoji']} **{rarity}** ({int(info['drop_rate']*100)}%) - {info['sell_value']} CC\n"
        
        embed.add_field(
            name="⭐ Raretés",
            value=rarities_text,
            inline=False
        )
        
        embed.set_footer(text="🎨 Chaque carte a maintenant une IMAGE UNIQUE générée ! ⚽")
        
        await ctx.send(embed=embed)
    
    @bot.command(name='card_visual')
    async def card_visual(ctx, card_id: str):
        """Génère et envoie l'image visuelle complète d'une carte"""
        user_data = card_system.get_user_data(ctx.author.id)
        card = next((c for c in user_data["collection"] if c["id"] == card_id), None)
        
        if not card:
            await ctx.send("❌ Carte non trouvée dans votre collection !")
            return
        
        # Message de chargement
        loading_msg = await ctx.send("🎨 Génération de l'image de la carte en cours...")
        
        try:
            # Générer l'image
            card_image = await card_visual_gen.generate_card_image(card)
            
            # Supprimer le message de chargement
            await loading_msg.delete()
            
            # Envoyer l'image
            rarity_info = CARD_TYPES[card["rarity"]]
            overall = card_system.get_overall_rating(card["stats"])
            
            await ctx.send(
                f"✨ **{rarity_info['emoji']} {card['name']}** (Note: **{overall}**)\n"
                f"*{card['description']}*",
                file=card_image
            )
            
        except Exception as e:
            await loading_msg.edit(content=f"❌ Erreur lors de la génération : {str(e)}")
    
    @bot.command(name='gallery')
    async def gallery(ctx, member: discord.Member = None):
        """Affiche une galerie visuelle des 3 meilleures cartes"""
        target = member or ctx.author
        user_data = card_system.get_user_data(target.id)
        
        if not user_data["collection"]:
            await ctx.send("❌ Collection vide !")
            return
        
        # Trier et prendre le top 3
        sorted_cards = sorted(
            user_data["collection"],
            key=lambda c: card_system.get_overall_rating(c["stats"]),
            reverse=True
        )[:3]
        
        loading_msg = await ctx.send(f"🎨 Génération de la galerie de {target.display_name}...")
        
        try:
            await loading_msg.edit(content=f"🏆 **Galerie de {target.display_name}** - Top 3 Cartes :")
            
            # Générer et envoyer chaque carte
            for i, card in enumerate(sorted_cards, 1):
                card_image = await card_visual_gen.generate_card_image(card)
                rarity_info = CARD_TYPES[card["rarity"]]
                overall = card_system.get_overall_rating(card["stats"])
                
                await ctx.send(
                    f"**#{i}** - {rarity_info['emoji']} **{card['name']}** (OVR: **{overall}**)",
                    file=card_image
                )
                
        except Exception as e:
            await loading_msg.edit(content=f"❌ Erreur : {str(e)}")
    
    @bot.command(name='open_pack')
    async def open_pack(ctx, pack_type: str):
        """Ouvre un pack et affiche les cartes en images"""
        user_data = card_system.get_user_data(ctx.author.id)
        
        packs = {
            "plata": {"cost": 100, "cards": 3, "guaranteed": None},
            "argent": {"cost": 250, "cards": 5, "guaranteed": "Rare"},
            "or": {"cost": 500, "cards": 7, "guaranteed": "Épique"},
            "platine": {"cost": 1000, "cards": 10, "guaranteed": "Légendaire"}
        }
        
        pack_type = pack_type.lower()
        
        if pack_type not in packs:
            await ctx.send("❌ Type invalide ! Utilisez : `plata`, `argent`, `or` ou `platine`")
            return
        
        pack = packs[pack_type]
        
        if user_data["credits"] < pack["cost"]:
            embed = discord.Embed(
                title="❌ Crédits insuffisants",
                description=f"Il vous faut **{pack['cost']} CC**.\nVous avez : **{user_data['credits']} CC**",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return
        
        user_data["credits"] -= pack["cost"]
        user_data["packs_opened"] += 1
        
        cards = []
        for i in range(pack["cards"]):
            if i == 0 and pack["guaranteed"]:
                available = [p for p in PLAYERS_DB if p["rarity"] == pack["guaranteed"] or 
                           (pack["guaranteed"] == "Légendaire" and p["rarity"] == "Mythique")]
                player = random.choice(available)
                card = {
                    "name": player["name"], "position": player["position"], "rarity": player["rarity"],
                    "stats": player["stats"], "description": player["description"],
                    "image_url": player["image_url"], "special_ability": player["special_ability"],
                    "nationality": player["nationality"],
                    "id": f"{player['name']}_{player['rarity']}_{random.randint(1000, 9999)}",
                    "obtained_at": datetime.now().isoformat()
                }
            else:
                card = card_system.generate_card()
            
            cards.append(card)
            user_data["collection"].append(card)
        
        card_system.save_data()
        
        # Message d'ouverture
        embed = discord.Embed(
            title=f"📦 Ouverture du Pack {pack_type.capitalize()} !",
            description=f"Vous avez obtenu **{pack['cards']} cartes** !",
            color=GREEN_COLOR
        )
        embed.add_field(
            name="💰 Nouveau solde",
            value=f"**{user_data['credits']} CC**",
            inline=False
        )
        
        await ctx.send(embed=embed)
        
        # Afficher les meilleures cartes en images (top 3 du pack)
        sorted_pack = sorted(cards, key=lambda c: card_system.get_overall_rating(c["stats"]), reverse=True)[:3]
        
        await ctx.send("✨ **Voici vos meilleures cartes du pack :**")
        
        for card in sorted_pack:
            try:
                card_image = await card_visual_gen.generate_card_image(card)
                rarity_info = CARD_TYPES[card["rarity"]]
                overall = card_system.get_overall_rating(card["stats"])
                
                await ctx.send(
                    f"{rarity_info['emoji']} **{card['name']}** - OVR: **{overall}**\n`ID: {card['id']}`",
                    file=card_image
                )
            except Exception as e:
                print(f"Erreur génération image: {e}")
        
        # Liste des autres cartes
        if len(cards) > 3:
            other_cards = "\n".join([
                f"• {CARD_TYPES[c['rarity']]['emoji']} {c['name']} (OVR {card_system.get_overall_rating(c['stats'])}) - `{c['id']}`"
                for c in sorted_pack[3:]
            ])
            await ctx.send(f"📋 **Autres cartes :**\n{other_cards}")
    
    @bot.command(name='daily')
    async def daily_reward(ctx):
        user_data = card_system.get_user_data(ctx.author.id)
        
        last_daily = user_data.get("last_daily")
        if last_daily:
            last_date = datetime.fromisoformat(last_daily)
            if datetime.now() - last_date < timedelta(hours=24):
                time_left = timedelta(hours=24) - (datetime.now() - last_date)
                hours = int(time_left.seconds / 3600)
                minutes = int((time_left.seconds % 3600) / 60)
                
                embed = discord.Embed(
                    title="⏰ Déjà réclamé !",
                    description=f"Revenez dans **{hours}h {minutes}min**.",
                    color=0xFF0000
                )
                await ctx.send(embed=embed)
                return
        
        reward = 50
        user_data["credits"] += reward
        user_data["last_daily"] = datetime.now().isoformat()
        card_system.save_data()
        
        embed = discord.Embed(
            title="🎁 Récompense quotidienne !",
            description=f"+**{reward} CC**\n\n💰 Solde : **{user_data['credits']} CC**",
            color=GREEN_COLOR
        )
        await ctx.send(embed=embed)
    
    @bot.command(name='balance')
    async def balance(ctx, member: discord.Member = None):
        target = member or ctx.author
        user_data = card_system.get_user_data(target.id)
        
        total_value = sum(CARD_TYPES[card["rarity"]]["sell_value"] for card in user_data["collection"])
        
        embed = discord.Embed(
            title=f"💰 {target.display_name}",
            description=f"**{user_data['credits']} crédits**",
            color=DARK_BLUE_COLOR
        )
        
        embed.add_field(name="📦 Packs ouverts", value=str(user_data["packs_opened"]), inline=True)
        embed.add_field(name="🎴 Cartes", value=str(len(user_data["collection"])), inline=True)
        embed.add_field(name="💎 Valeur totale", value=f"{total_value} CC", inline=True)
        
        await ctx.send(embed=embed)
    
    @bot.command(name='collection')
    async def collection(ctx, member: discord.Member = None):
        target = member or ctx.author
        user_data = card_system.get_user_data(target.id)
        
        if not user_data["collection"]:
            await ctx.send("❌ Collection vide !")
            return
        
        by_rarity = {}
        for card in user_data["collection"]:
            rarity = card["rarity"]
            if rarity not in by_rarity:
                by_rarity[rarity] = []
            by_rarity[rarity].append(card)
        
        embed = discord.Embed(
            title=f"📚 Collection de {target.display_name}",
            description=f"**{len(user_data['collection'])} cartes**",
            color=DARK_BLUE_COLOR
        )
        
        for rarity in ["Mythique", "Légendaire", "Épique", "Rare", "Commune"]:
            if rarity in by_rarity:
                cards_list = by_rarity[rarity]
                rarity_info = CARD_TYPES[rarity]
                
                cards_text = "\n".join([
                    f"• {c['name']} (OVR {card_system.get_overall_rating(c['stats'])}) - `{c['id']}`"
                    for c in cards_list[:5]
                ])
                
                if len(cards_list) > 5:
                    cards_text += f"\n... +{len(cards_list) - 5} autres"
                
                embed.add_field(
                    name=f"{rarity_info['emoji']} {rarity} ({len(cards_list)})",
                    value=cards_text,
                    inline=False
                )
        
        embed.set_footer(text="Utilisez a!card_visual <id> pour voir une carte en image !")
        await ctx.send(embed=embed)
    
    @bot.command(name='sell')
    async def sell_card(ctx, card_id: str):
        user_data = card_system.get_user_data(ctx.author.id)
        card = next((c for c in user_data["collection"] if c["id"] == card_id), None)
        
        if not card:
            await ctx.send("❌ Carte non trouvée !")
            return
        
        user_data["collection"].remove(card)
        sell_value = CARD_TYPES[card["rarity"]]["sell_value"]
        user_data["credits"] += sell_value
        card_system.save_data()
        
        await ctx.send(f"✅ **{card['name']}** vendu pour **{sell_value} CC**\n💰 Solde : **{user_data['credits']} CC**")
