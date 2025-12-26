# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import json
import random
from datetime import datetime, timedelta
from config import GREEN_COLOR, DARK_BLUE_COLOR

# Import conditionnel du generateur visuel
try:
    from card_visual_generator import card_visual_gen
    VISUAL_MODE_ENABLED = True
    print("Mode visuel active - Generation d'images disponible")
except ImportError:
    VISUAL_MODE_ENABLED = False
    print("Mode visuel desactive - card_visual_generator.py non trouve")
    print("Le bot fonctionnera en mode embed classique")

# Configuration des cartes
CARD_TYPES = {
    "Commune": {"color": 0x808080, "emoji": "⚪", "drop_rate": 0.70, "sell_value": 10},
    "Rare": {"color": 0x0099FF, "emoji": "🔵", "drop_rate": 0.20, "sell_value": 50},
    "Epique": {"color": 0x9D00FF, "emoji": "🟣", "drop_rate": 0.07, "sell_value": 150},
    "Legendaire": {"color": 0xFFD700, "emoji": "🟡", "drop_rate": 0.025, "sell_value": 500},
    "Mythique": {"color": 0xFF0000, "emoji": "🔴", "drop_rate": 0.005, "sell_value": 1500}
}

STAT_EMOJIS = {
    "vitesse": "⚡", "defense": "🛡️", "attaque": "⚔️",
    "technique": "🎯", "physique": "💪", "mental": "🧠"
}

# Base de donnees enrichie avec stats
PLAYERS_DB = [
    # DEFENSEURS
    {"name": "Araki", "position": "Defense", "rarity": "Mythique",
     "stats": {"vitesse": 88, "defense": 99, "attaque": 75, "technique": 92, "physique": 90, "mental": 95},
     "description": "Le genie tactique de la defense", "image_url": None,
     "special_ability": "Catenaccio Perfect", "nationality": "Japon"},
    
    {"name": "Matsumoto", "position": "Defense", "rarity": "Legendaire",
     "stats": {"vitesse": 82, "defense": 91, "attaque": 68, "technique": 85, "physique": 88, "mental": 87},
     "description": "Le mur impenetrable", "image_url": None,
     "special_ability": "Muraille de Fer", "nationality": "Japon"},
    
    {"name": "Tanaka", "position": "Defense", "rarity": "Epique",
     "stats": {"vitesse": 78, "defense": 85, "attaque": 62, "technique": 79, "physique": 84, "mental": 80},
     "description": "Specialiste du marquage", "image_url": None,
     "special_ability": "Marquage Serre", "nationality": "Japon"},
    
    {"name": "Yamada", "position": "Defense", "rarity": "Rare",
     "stats": {"vitesse": 72, "defense": 78, "attaque": 55, "technique": 70, "physique": 76, "mental": 72},
     "description": "Defenseur polyvalent", "image_url": None,
     "special_ability": "Polyvalence", "nationality": "Japon"},
    
    {"name": "Sato", "position": "Defense", "rarity": "Commune",
     "stats": {"vitesse": 65, "defense": 70, "attaque": 48, "technique": 62, "physique": 68, "mental": 65},
     "description": "Jeune espoir defensif", "image_url": None,
     "special_ability": "Determination", "nationality": "Japon"},
    
    {"name": "Kobayashi", "position": "Defense", "rarity": "Commune",
     "stats": {"vitesse": 63, "defense": 68, "attaque": 45, "technique": 60, "physique": 66, "mental": 63},
     "description": "Defenseur en formation", "image_url": None,
     "special_ability": "Apprentissage Rapide", "nationality": "Japon"},
    
    # MILIEUX
    {"name": "Nakamura", "position": "Milieu", "rarity": "Legendaire",
     "stats": {"vitesse": 86, "defense": 80, "attaque": 88, "technique": 93, "physique": 82, "mental": 90},
     "description": "Maestro du milieu de terrain", "image_url": None,
     "special_ability": "Vision de Jeu", "nationality": "Japon"},
    
    {"name": "Ito", "position": "Milieu", "rarity": "Epique",
     "stats": {"vitesse": 80, "defense": 75, "attaque": 82, "technique": 86, "physique": 78, "mental": 83},
     "description": "Recuperateur infatigable", "image_url": None,
     "special_ability": "Endurance Infinie", "nationality": "Japon"},
    
    {"name": "Watanabe", "position": "Milieu", "rarity": "Rare",
     "stats": {"vitesse": 74, "defense": 70, "attaque": 76, "technique": 80, "physique": 72, "mental": 75},
     "description": "Milieu box-to-box", "image_url": None,
     "special_ability": "Course Explosive", "nationality": "Japon"},
    
    {"name": "Suzuki", "position": "Milieu", "rarity": "Commune",
     "stats": {"vitesse": 67, "defense": 64, "attaque": 68, "technique": 72, "physique": 66, "mental": 68},
     "description": "Milieu de terrain prometteur", "image_url": None,
     "special_ability": "Passes Precises", "nationality": "Japon"},
    
    # ATTAQUANTS
    {"name": "Takahashi", "position": "Attaque", "rarity": "Legendaire",
     "stats": {"vitesse": 94, "defense": 58, "attaque": 96, "technique": 90, "physique": 80, "mental": 88},
     "description": "Le finisseur ultime", "image_url": None,
     "special_ability": "Instinct du Buteur", "nationality": "Japon"},
    
    {"name": "Kato", "position": "Attaque", "rarity": "Epique",
     "stats": {"vitesse": 88, "defense": 52, "attaque": 89, "technique": 84, "physique": 76, "mental": 82},
     "description": "Attaquant rapide et technique", "image_url": None,
     "special_ability": "Vitesse Eclair", "nationality": "Japon"},
    
    {"name": "Yoshida", "position": "Attaque", "rarity": "Rare",
     "stats": {"vitesse": 80, "defense": 48, "attaque": 82, "technique": 78, "physique": 70, "mental": 74},
     "description": "Attaquant opportuniste", "image_url": None,
     "special_ability": "Opportunisme", "nationality": "Japon"},
    
    {"name": "Mori", "position": "Attaque", "rarity": "Commune",
     "stats": {"vitesse": 72, "defense": 42, "attaque": 74, "technique": 68, "physique": 64, "mental": 66},
     "description": "Jeune attaquant prometteur", "image_url": None,
     "special_ability": "Combativite", "nationality": "Japon"},
    
    # GARDIENS
    {"name": "Fujita", "position": "Gardien", "rarity": "Epique",
     "stats": {"vitesse": 70, "defense": 92, "attaque": 45, "technique": 88, "physique": 85, "mental": 91},
     "description": "Gardien aux reflexes exceptionnels", "image_url": None,
     "special_ability": "Reflexes Surhumains", "nationality": "Japon"},
    
    {"name": "Ishikawa", "position": "Gardien", "rarity": "Rare",
     "stats": {"vitesse": 65, "defense": 85, "attaque": 40, "technique": 80, "physique": 78, "mental": 83},
     "description": "Gardien fiable", "image_url": None,
     "special_ability": "Plongeon Heroique", "nationality": "Japon"},
    
    {"name": "Kimura", "position": "Gardien", "rarity": "Commune",
     "stats": {"vitesse": 60, "defense": 76, "attaque": 35, "technique": 72, "physique": 70, "mental": 74},
     "description": "Gardien en developpement", "image_url": None,
     "special_ability": "Concentration", "nationality": "Japon"},
    
    # TECHNIQUES
    {"name": "Catenaccio", "position": "Technique", "rarity": "Mythique",
     "stats": {"vitesse": 75, "defense": 99, "attaque": 65, "technique": 98, "physique": 80, "mental": 97},
     "description": "La tactique defensive ultime", "image_url": None,
     "special_ability": "Defense Absolue", "nationality": "Italie"},
    
    {"name": "Tiki-Taka", "position": "Technique", "rarity": "Legendaire",
     "stats": {"vitesse": 82, "defense": 70, "attaque": 88, "technique": 96, "physique": 75, "mental": 92},
     "description": "Possession et passes courtes", "image_url": None,
     "special_ability": "Possession Totale", "nationality": "Espagne"},
    
    {"name": "Contre-attaque", "position": "Technique", "rarity": "Epique",
     "stats": {"vitesse": 92, "defense": 75, "attaque": 90, "technique": 85, "physique": 80, "mental": 87},
     "description": "Vitesse et efficacite", "image_url": None,
     "special_ability": "Transition Rapide", "nationality": "Allemagne"},
    
    {"name": "Pressing", "position": "Technique", "rarity": "Rare",
     "stats": {"vitesse": 86, "defense": 78, "attaque": 80, "technique": 82, "physique": 88, "mental": 85},
     "description": "Pression constante", "image_url": None,
     "special_ability": "Pression Intense", "nationality": "Angleterre"},
]

class CardSystem:
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "card_data.json"
        self.load_data()
        self.migrate_old_cards()
        
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
    
    def migrate_old_cards(self):
        """Migre les anciennes cartes en ajoutant les stats manquantes"""
        migrated_count = 0
        
        for user_id, user_data in self.data.get("users", {}).items():
            for card in user_data.get("collection", []):
                if "stats" not in card:
                    player_template = next((p for p in PLAYERS_DB 
                                          if p["name"] == card["name"] and p["rarity"] == card["rarity"]), None)
                    
                    if player_template:
                        card["stats"] = player_template["stats"]
                        card["description"] = player_template["description"]
                        card["image_url"] = player_template.get("image_url")
                        card["special_ability"] = player_template["special_ability"]
                        card["nationality"] = player_template["nationality"]
                        migrated_count += 1
        
        if migrated_count > 0:
            self.save_data()
            print(f"Migration reussie : {migrated_count} cartes mises a jour avec les stats")
    
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
                        "image_url": player.get("image_url"),
                        "special_ability": player["special_ability"],
                        "nationality": player["nationality"],
                        "id": f"{player['name']}_{rarity}_{random.randint(1000, 9999)}",
                        "obtained_at": datetime.now().isoformat()
                    }
        
        player = random.choice([p for p in PLAYERS_DB if p["rarity"] == "Commune"])
        return {
            "name": player["name"], "position": player["position"], "rarity": "Commune",
            "stats": player["stats"], "description": player["description"],
            "image_url": player.get("image_url"), "special_ability": player["special_ability"],
            "nationality": player["nationality"],
            "id": f"{player['name']}_Commune_{random.randint(1000, 9999)}",
            "obtained_at": datetime.now().isoformat()
        }
    
    def get_overall_rating(self, stats):
        return sum(stats.values()) // len(stats) if stats else 0
    
    def create_card_embed(self, card):
        rarity_info = CARD_TYPES[card["rarity"]]
        stats = card.get("stats", {})
        overall = self.get_overall_rating(stats) if stats else 0
        
        embed = discord.Embed(
            title=f"{rarity_info['emoji']} {card['name']}",
            description=card.get("description", f"**Position:** {card['position']}\n**Rarete:** {card['rarity']}"),
            color=rarity_info["color"]
        )
        
        if stats:
            stats_text = ""
            for stat_name, stat_value in stats.items():
                emoji = STAT_EMOJIS.get(stat_name, "📊")
                stats_text += f"{emoji} **{stat_name.capitalize()}:** {stat_value}\n"
            
            embed.add_field(name="Statistiques", value=stats_text, inline=False)
            embed.add_field(name="Note OVR", value=f"**{overall}**", inline=True)
        
        embed.add_field(name="Valeur", value=f"{rarity_info['sell_value']} CC", inline=True)
        embed.add_field(name="ID", value=f"`{card['id']}`", inline=True)
        
        if VISUAL_MODE_ENABLED:
            embed.set_footer(text=f"Collection Catenaccio - {card['rarity']} - Utilisez a!card_visual {card['id']}")
        else:
            embed.set_footer(text=f"Collection Catenaccio - {card['rarity']}")
        
        return embed

def setup_card_commands(bot):
    card_system = CardSystem(bot)
    
    @bot.command(name='card_help')
    async def card_help(ctx):
        embed = discord.Embed(
            title="Guide du Systeme de Cartes Catenaccio",
            description=(
                "Bienvenue dans le systeme de collection de cartes !\n"
                f"{'MODE VISUEL ACTIVE - Cartes en images disponibles !' if VISUAL_MODE_ENABLED else 'Mode embed classique'}"
            ),
            color=GREEN_COLOR
        )
        
        embed.add_field(
            name="Commandes de Base",
            value=(
                "`a!daily` - Recompense quotidienne\n"
                "`a!balance` - Voir vos credits\n"
                "`a!shop` - Boutique de packs\n"
                "`a!open_pack <type>` - Ouvrir un pack\n"
            ),
            inline=False
        )
        
        collection_cmds = (
            "`a!collection` - Voir votre collection\n"
            "`a!card <id>` - Details d'une carte\n"
            "`a!sell <id>` - Vendre une carte\n"
        )
        
        if VISUAL_MODE_ENABLED:
            collection_cmds += (
                "`a!card_visual <id>` - Image de la carte\n"
                "`a!gallery` - Galerie top 3\n"
            )
        
        embed.add_field(name="Collection", value=collection_cmds, inline=False)
        
        embed.add_field(
            name="Echanges",
            value=(
                "`a!trade @user <id> <credits>` - Echanger\n"
                "`a!transfer @user <credits>` - Transferer\n"
            ),
            inline=False
        )
        
        rarities_text = ""
        for rarity, info in CARD_TYPES.items():
            rarities_text += f"{info['emoji']} **{rarity}** ({int(info['drop_rate']*100)}%) - {info['sell_value']} CC\n"
        
        embed.add_field(name="Raretes", value=rarities_text, inline=False)
        
        await ctx.send(embed=embed)
    
    if VISUAL_MODE_ENABLED:
        @bot.command(name='card_visual')
        async def card_visual(ctx, card_id: str):
            user_data = card_system.get_user_data(ctx.author.id)
            card = next((c for c in user_data["collection"] if c["id"] == card_id), None)
            
            if not card:
                await ctx.send("Carte non trouvee !")
                return
            
            loading_msg = await ctx.send("Generation de l'image...")
            
            try:
                card_image = await card_visual_gen.generate_card_image(card)
                await loading_msg.delete()
                
                rarity_info = CARD_TYPES[card["rarity"]]
                overall = card_system.get_overall_rating(card.get("stats", {}))
                
                await ctx.send(
                    f"{rarity_info['emoji']} **{card['name']}** (OVR: **{overall}**)",
                    file=card_image
                )
            except Exception as e:
                await loading_msg.edit(content=f"Erreur : {str(e)}")
        
        @bot.command(name='gallery')
        async def gallery(ctx, member: discord.Member = None):
            target = member or ctx.author
            user_data = card_system.get_user_data(target.id)
            
            if not user_data["collection"]:
                await ctx.send("Collection vide !")
                return
            
            sorted_cards = sorted(
                user_data["collection"],
                key=lambda c: card_system.get_overall_rating(c.get("stats", {})),
                reverse=True
            )[:3]
            
            await ctx.send(f"**Galerie de {target.display_name}** - Top 3 :")
            
            for i, card in enumerate(sorted_cards, 1):
                try:
                    card_image = await card_visual_gen.generate_card_image(card)
                    rarity_info = CARD_TYPES[card["rarity"]]
                    overall = card_system.get_overall_rating(card.get("stats", {}))
                    
                    await ctx.send(
                        f"**#{i}** - {rarity_info['emoji']} **{card['name']}** (OVR: **{overall}**)",
                        file=card_image
                    )
                except Exception as e:
                    print(f"Erreur generation image: {e}")
    
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
                
                await ctx.send(f"Revenez dans **{hours}h {minutes}min** !")
                return
        
        reward = 50
        user_data["credits"] += reward
        user_data["last_daily"] = datetime.now().isoformat()
        card_system.save_data()
        
        await ctx.send(f"+**{reward} CC** !\nSolde : **{user_data['credits']} CC**")
    
    @bot.command(name='balance')
    async def balance(ctx, member: discord.Member = None):
        target = member or ctx.author
        user_data = card_system.get_user_data(target.id)
        
        total_value = sum(CARD_TYPES[card["rarity"]]["sell_value"] for card in user_data["collection"])
        
        embed = discord.Embed(
            title=f"{target.display_name}",
            description=f"**{user_data['credits']} credits**",
            color=DARK_BLUE_COLOR
        )
        
        embed.add_field(name="Packs ouverts", value=str(user_data["packs_opened"]), inline=True)
        embed.add_field(name="Cartes", value=str(len(user_data["collection"])), inline=True)
        embed.add_field(name="Valeur totale", value=f"{total_value} CC", inline=True)
        
        await ctx.send(embed=embed)
    
    @bot.command(name='shop')
    async def shop(ctx):
        embed = discord.Embed(
            title="Boutique de Packs",
            description="Achetez des packs pour agrandir votre collection !",
            color=GREEN_COLOR
        )
        
        embed.add_field(name="Pack Plata (100 CC)", value="3 cartes - `a!open_pack plata`", inline=False)
        embed.add_field(name="Pack Argent (250 CC)", value="5 cartes dont 1 rare min - `a!open_pack argent`", inline=False)
        embed.add_field(name="Pack Or (500 CC)", value="7 cartes dont 1 epique min - `a!open_pack or`", inline=False)
        embed.add_field(name="Pack Platine (1000 CC)", value="10 cartes dont 1 legendaire min - `a!open_pack platine`", inline=False)
        
        await ctx.send(embed=embed)
    
    @bot.command(name='open_pack')
    async def open_pack(ctx, pack_type: str):
        user_data = card_system.get_user_data(ctx.author.id)
        
        packs = {
            "plata": {"cost": 100, "cards": 3, "guaranteed": None},
            "argent": {"cost": 250, "cards": 5, "guaranteed": "Rare"},
            "or": {"cost": 500, "cards": 7, "guaranteed": "Epique"},
            "platine": {"cost": 1000, "cards": 10, "guaranteed": "Legendaire"}
        }
        
        pack_type = pack_type.lower()
        
        if pack_type not in packs:
            await ctx.send("Type invalide ! Utilisez : plata, argent, or ou platine")
            return
        
        pack = packs[pack_type]
        
        if user_data["credits"] < pack["cost"]:
            await ctx.send(f"Il vous faut **{pack['cost']} CC**. Vous avez : **{user_data['credits']} CC**")
            return
        
        user_data["credits"] -= pack["cost"]
        user_data["packs_opened"] += 1
        
        cards = []
        for i in range(pack["cards"]):
            if i == 0 and pack["guaranteed"]:
                available = [p for p in PLAYERS_DB if p["rarity"] == pack["guaranteed"] or 
                           (pack["guaranteed"] == "Legendaire" and p["rarity"] == "Mythique")]
                player = random.choice(available)
                card = {
                    "name": player["name"], "position": player["position"], "rarity": player["rarity"],
                    "stats": player["stats"], "description": player["description"],
                    "image_url": player.get("image_url"), "special_ability": player["special_ability"],
                    "nationality": player["nationality"],
                    "id": f"{player['name']}_{player['rarity']}_{random.randint(1000, 9999)}",
                    "obtained_at": datetime.now().isoformat()
                }
            else:
                card = card_system.generate_card()
            
            cards.append(card)
            user_data["collection"].append(card)
        
        card_system.save_data()
        
        embed = discord.Embed(
            title=f"Pack {pack_type.capitalize()} !",
            description=f"**{pack['cards']} cartes** obtenues !",
            color=GREEN_COLOR
        )
        
        for card in cards:
            rarity_info = CARD_TYPES[card["rarity"]]
            overall = card_system.get_overall_rating(card.get("stats", {}))
            embed.add_field(
                name=f"{rarity_info['emoji']} {card['name']}",
                value=f"{card['position']} - OVR {overall}\n`{card['id']}`",
                inline=True
            )
        
        embed.add_field(
            name="Credits restants",
            value=f"**{user_data['credits']} CC**",
            inline=False
        )
        
        await ctx.send(embed=embed)
        
        if VISUAL_MODE_ENABLED and len(cards) >= 3:
            sorted_pack = sorted(cards, key=lambda c: card_system.get_overall_rating(c.get("stats", {})), reverse=True)[:min(3, len(cards))]
            await ctx.send("**Meilleures cartes du pack :**")
            
            for card in sorted_pack:
                try:
                    card_image = await card_visual_gen.generate_card_image(card)
                    rarity_info = CARD_TYPES[card["rarity"]]
                    overall = card_system.get_overall_rating(card.get("stats", {}))
                    
                    await ctx.send(
                        f"{rarity_info['emoji']} **{card['name']}** - OVR: **{overall}**",
                        file=card_image
                    )
                except Exception as e:
                    print(f"Erreur generation image: {e}")
    
    @bot.command(name='collection')
    async def collection(ctx, member: discord.Member = None):
        target = member or ctx.author
        user_data = card_system.get_user_data(target.id)
        
        if not user_data["collection"]:
            await ctx.send("Collection vide !")
            return
        
        by_rarity = {}
        for card in user_data["collection"]:
            rarity = card["rarity"]
            if rarity not in by_rarity:
                by_rarity[rarity] = []
            by_rarity[rarity].append(card)
        
        embed = discord.Embed(
            title=f"Collection de {target.display_name}",
            description=f"**{len(user_data['collection'])} cartes**",
            color=DARK_BLUE_COLOR
        )
        
        for rarity in ["Mythique", "Legendaire", "Epique", "Rare", "Commune"]:
            if rarity in by_rarity:
                cards_list = by_rarity[rarity]
                rarity_info = CARD_TYPES[rarity]
                
                cards_text = "\n".join([
                    f"{c['name']} (OVR {card_system.get_overall_rating(c.get('stats', {}))}) - `{c['id']}`"
                    for c in cards_list[:5]
                ])
                
                if len(cards_list) > 5:
                    cards_text += f"\n... +{len(cards_list) - 5} autres"
                
                embed.add_field(
                    name=f"{rarity_info['emoji']} {rarity} ({len(cards_list)})",
                    value=cards_text,
                    inline=False
                )
        
        footer_text = "Utilisez a!card <id> pour voir les details"
        if VISUAL_MODE_ENABLED:
            footer_text += " ou a!card_visual <id> pour l'image"
        embed.set_footer(text=footer_text)
        
        await ctx.send(embed=embed)
    
    @bot.command(name='card')
    async def card_details(ctx, card_id: str):
        user_data = card_system.get_user_data(ctx.author.id)
        card = next((c for c in user_data["collection"] if c["id"] == card_id), None)
        
        if not card:
            await ctx.send("Carte non trouvee !")
            return
        
        embed = card_system.create_card_embed(card)
        
        obtained_date = datetime.fromisoformat(card["obtained_at"])
        embed.add_field(
            name="Obtenue le",
            value=obtained_date.strftime("%d/%m/%Y a %H:%M"),
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @bot.command(name='sell')
    async def sell_card(ctx, card_id: str):
        user_data = card_system.get_user_data(ctx.author.id)
        card = next((c for c in user_data["collection"] if c["id"] == card_id), None)
        
        if not card:
            await ctx.send("Carte non trouvee !")
            return
        
        user_data["collection"].remove(card)
        sell_value = CARD_TYPES[card["rarity"]]["sell_value"]
        user_data["credits"] += sell_value
        card_system.save_data()
        
        await ctx.send(f"**{card['name']}** vendu pour **{sell_value} CC**\nSolde : **{user_data['credits']} CC**")
    
    @bot.command(name='trade')
    async def trade(ctx, member: discord.Member, card_id: str, credits: int):
        if member.id == ctx.author.id:
            await ctx.send("Vous ne pouvez pas echanger avec vous-meme !")
            return
        
        sender_data = card_system.get_user_data(ctx.author.id)
        receiver_data = card_system.get_user_data(member.id)
        
        card = next((c for c in sender_data["collection"] if c["id"] == card_id), None)
        
        if not card:
            await ctx.send("Carte non trouvee !")
            return
        
        if receiver_data["credits"] < credits:
            await ctx.send(f"{member.display_name} n'a pas assez de credits !")
            return
        
        trade_id = f"{ctx.author.id}_{member.id}_{datetime.now().timestamp()}"
        card_system.data["trades"][trade_id] = {
            "sender_id": str(ctx.author.id),
            "receiver_id": str(member.id),
            "card": card,
            "credits": credits,
            "created_at": datetime.now().isoformat()
        }
        card_system.save_data()
        
        await ctx.send(
            f"**Echange propose** !\n"
            f"{ctx.author.mention} -> {card['name']} ({card['rarity']})\n"
            f"{member.mention} -> {credits} CC\n\n"
            f"{member.mention}, utilisez :\n"
            f"`a!trade_accept {trade_id}` pour accepter\n"
            f"`a!trade_cancel {trade_id}` pour refuser"
        )
    
    @bot.command(name='trade_accept')
    async def trade_accept(ctx, trade_id: str):
        if trade_id not in card_system.data["trades"]:
            await ctx.send("Echange non trouve !")
            return
        
        trade = card_system.data["trades"][trade_id]
        
        if str(ctx.author.id) != trade["receiver_id"]:
            await ctx.send("Cet echange ne vous est pas destine !")
            return
        
        sender_data = card_system.get_user_data(trade["sender_id"])
        receiver_data = card_system.get_user_data(trade["receiver_id"])
        
        card = next((c for c in sender_data["collection"] if c["id"] == trade["card"]["id"]], None)
        
        if not card:
            await ctx.send("La carte n'est plus disponible !")
            del card_system.data["trades"][trade_id]
            card_system.save_data()
            return
        
        if receiver_data["credits"] < trade["credits"]:
            await ctx.send("Vous n'avez plus assez de credits !")
            return
        
        sender_data["collection"].remove(card)
        receiver_data["collection"].append(card)
        receiver_data["credits"] -= trade["credits"]
        sender_data["credits"] += trade["credits"]
        
        del card_system.data["trades"][trade_id]
        card_system.save_data()
        
        await ctx.send(f"Echange reussi !\n**{card['name']}** -> <@{trade['receiver_id']}>\n**{trade['credits']} CC** -> <@{trade['sender_id']}>")
    
    @bot.command(name='trade_cancel')
    async def trade_cancel(ctx, trade_id: str):
        if trade_id not in card_system.data["trades"]:
            await ctx.send("Echange non trouve !")
            return
        
        trade = card_system.data["trades"][trade_id]
        
        if str(ctx.author.id) not in [trade["sender_id"], trade["receiver_id"]]:
            await ctx.send("Vous n'etes pas concerne par cet echange !")
            return
        
        del card_system.data["trades"][trade_id]
        card_system.save_data()
        
        await ctx.send("Echange annule")
    
    @bot.command(name='transfer')
    async def transfer_credits(ctx, member: discord.Member, credits: int):
        if member.id == ctx.author.id:
            await ctx.send("Vous ne pouvez pas vous transferer des credits !")
            return
        
        if credits <= 0:
            await ctx.send("Le montant doit etre positif !")
            return
        
        sender_data = card_system.get_user_data(ctx.author.id)
        receiver_data = card_system.get_user_data(member.id)
        
        if sender_data["credits"] < credits:
            await ctx.send("Vous n'avez pas assez de credits !")
            return
        
        sender_data["credits"] -= credits
        receiver_data["credits"] += credits
        card_system.save_data()
        
        await ctx.send(f"**{credits} CC** transferes de {ctx.author.mention} -> {member.mention}")
