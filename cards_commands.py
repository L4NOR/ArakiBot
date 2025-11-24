# cards_commands.py
# Commandes du système de cartes Catenaccio
# Conçu pour être chargé depuis main.py (setup_cards_commands(bot)).

import discord
from discord.ext import commands
import random
import math
import asyncio
from save_manager import (
    get_user, add_credits, get_credits, give_card_to_user, register_card,
    get_user_collection, list_user_cards_pretty, get_all_cards,
    create_trade, get_trade, accept_trade, set_trade_status, remove_card_from_user
)
from config import GREEN_COLOR, COMMAND_PREFIX

# Définition des packs et probabilités (valeurs d'exemple)
PACK_DEFINITIONS = {
    "bronze": {
        "price": 100,
        "count": 3,
        "guarantees": {"common": 3}
    },
    "argent": {
        "price": 250,
        "count": 5,
        "guarantees": {"common": 4, "rare": 1}
    },
    "or": {
        "price": 500,
        "count": 7,
        "guarantees": {"common": 5, "rare": 1, "epic": 1}
    },
    "platine": {
        "price": 1000,
        "count": 10,
        "guarantees": {"common": 6, "rare": 2, "epic": 1, "legendary": 1}
    },
    "evenement": {
        "price": 0,
        "count": 3,
        "guarantees": {}
    }
}

# Rarity probabilities
RARITY_POOL = [
    ("mythique", 0.5),   # 0.5%
    ("legendary", 2),    # 2%
    ("epic", 8),         # 8%
    ("rare", 20),        # 20%
    ("common", 69.5)     # remaining to total 100
]

def weighted_choice(rarity_pool):
    total = sum(weight for (_, weight) in rarity_pool)
    r = random.random() * total
    upto = 0
    for item, weight in rarity_pool:
        if upto + weight >= r:
            return item
        upto += weight
    return rarity_pool[-1][0]

def pick_card_by_rarity(cards_by_rarity, rarity):
    """cards_by_rarity: dict rarity -> list of card_id"""
    pool = cards_by_rarity.get(rarity, [])
    if not pool:
        # fallback to any card
        all_cards = [cid for lst in cards_by_rarity.values() for cid in lst]
        return random.choice(all_cards) if all_cards else None
    return random.choice(pool)

def build_cards_by_rarity(cards_dict):
    by_rarity = {}
    for cid, meta in cards_dict.items():
        r = meta.get("rarity", "common")
        by_rarity.setdefault(r, []).append(cid)
    return by_rarity

def setup_cards_commands(bot):
    # COMMANDS NAMESPACE: prefix a! (configured in config.py)
    @bot.command(name="balance")
    async def balance(ctx, member: discord.Member = None):
        target = member or ctx.author
        credits = get_credits(str(target.id))
        embed = discord.Embed(
            title=f"💳 Crédits de {target.display_name}",
            description=f"**{credits} CC**",
            color=GREEN_COLOR
        )
        await ctx.send(embed=embed)

    @bot.command(name="daily")
    async def daily(ctx):
        user_id = str(ctx.author.id)
        # simple daily reward - for demo give 50 CC once per run (no cooldown store)
        add_credits(user_id, 50)
        await ctx.send(f"{ctx.author.mention} Tu as reçu **50 CC** (récompense quotidienne).")

    @bot.command(name="shop")
    async def shop(ctx):
        lines = []
        for key, val in PACK_DEFINITIONS.items():
            price = val.get("price", 0)
            lines.append(f"**{key.capitalize()}** — {price} CC — {val['count']} cartes")
        embed = discord.Embed(
            title="🛒 Boutique de Packs",
            description="\n".join(lines),
            color=GREEN_COLOR
        )
        await ctx.send(embed=embed)

    @bot.command(name="open")
    async def open_pack(ctx, pack_name: str):
        user_id = str(ctx.author.id)
        pack = PACK_DEFINITIONS.get(pack_name.lower())
        if not pack:
            await ctx.send("Pack inconnu. Utilise `a!shop` pour voir les packs disponibles.")
            return

        price = pack.get("price", 0)
        if get_credits(user_id) < price:
            await ctx.send("Tu n'as pas assez de CC pour ouvrir ce pack.")
            return

        # charge user
        add_credits(user_id, -price)

        # load card data
        cards = get_all_cards()
        cards_by_rarity = build_cards_by_rarity(cards)

        opened = []
        # handle guaranteed scheme if provided
        guarantees = pack.get("guarantees", {})
        # first fill guarantees
        for rarity, count in guarantees.items():
            for _ in range(count):
                cid = pick_card_by_rarity(cards_by_rarity, rarity)
                if cid:
                    give_card_to_user(user_id, cid, 1)
                    opened.append((cid, rarity))

        # fill the rest randomly to reach pack['count']
        to_open = pack['count'] - len(opened)
        for _ in range(to_open):
            rarity = weighted_choice(RARITY_POOL)
            cid = pick_card_by_rarity(cards_by_rarity, rarity)
            if not cid:
                # fallback random
                all_cards = list(cards.keys())
                if not all_cards:
                    continue
                cid = random.choice(all_cards)
            give_card_to_user(user_id, cid, 1)
            opened.append((cid, rarity))

        # Create embed summary
        embed = discord.Embed(
            title=f"🎁 {ctx.author.display_name} a ouvert un pack {pack_name.capitalize()}",
            description=f"Prix : {price} CC",
            color=GREEN_COLOR
        )
        desc_lines = []
        cards_meta = get_all_cards()
        for cid, rarity in opened:
            meta = cards_meta.get(cid, {})
            title = meta.get("title", cid)
            img = meta.get("image")
            desc_lines.append(f"**{title}** — *{rarity}* (id: `{cid}`)")
        embed.add_field(name="Contenu", value="\n".join(desc_lines) if desc_lines else "Aucune carte disponible.", inline=False)

        await ctx.send(embed=embed)

    @bot.command(name="createcard")
    @commands.has_permissions(administrator=True)
    async def create_card(ctx, card_id: str, rarity: str, title: str, image_url: str = None, *, extras: str = ""):
        # metadata flexible
        meta = {
            "title": title,
            "rarity": rarity.lower(),
            "image": image_url,
            "extras": extras
        }
        register_card(card_id, meta)
        await ctx.send(f"Carte `{card_id}` créée : **{title}** ({rarity})")

    @bot.command(name="collection")
    async def collection(ctx, member: discord.Member = None):
        target = member or ctx.author
        user_id = str(target.id)
        col = list_user_cards_pretty(user_id)
        if not col:
            await ctx.send(f"{target.display_name} n'a pas encore de cartes.")
            return
        embed = discord.Embed(
            title=f"🗂️ Collection de {target.display_name}",
            color=GREEN_COLOR
        )
        for item in col:
            title = item["meta"].get("title", item["card_id"])
            rarity = item["meta"].get("rarity", "common")
            count = item["count"]
            embed.add_field(name=f"{title} ({rarity})", value=f"x{count} — id `{item['card_id']}`", inline=False)
        await ctx.send(embed=embed)

    @bot.command(name="card")
    async def card_info(ctx, card_id: str):
        card = get_all_cards().get(card_id)
        if not card:
            await ctx.send("Carte introuvable.")
            return
        embed = discord.Embed(title=card.get("title", card_id), color=GREEN_COLOR)
        embed.add_field(name="Rareté", value=card.get("rarity", "common"))
        if card.get("extras"):
            embed.add_field(name="Infos", value=card.get("extras"), inline=False)
        if card.get("image"):
            embed.set_image(url=card.get("image"))
        await ctx.send(embed=embed)

    @bot.command(name="give")
    @commands.has_permissions(administrator=True)
    async def give_cmd(ctx, member: discord.Member, amount: int):
        add_credits(str(member.id), int(amount))
        await ctx.send(f"{member.mention} a reçu **{amount} CC**.")

    @bot.command(name="givecard")
    @commands.has_permissions(administrator=True)
    async def givecard_cmd(ctx, member: discord.Member, card_id: str, amount: int = 1):
        give_card_to_user(str(member.id), card_id, int(amount))
        await ctx.send(f"{member.mention} a reçu **x{amount}** de la carte `{card_id}`.")

    # Trade system (simple)
    @bot.command(name="trade")
    async def trade_cmd(ctx, target: discord.Member, offered_card_id: str, offered_amount: int, requested_credits: int):
        from_id = str(ctx.author.id)
        to_id = str(target.id)

        # verify sender has cards
        user_collection = get_user_collection(from_id)
        if user_collection.get(offered_card_id, 0) < offered_amount:
            await ctx.send("Tu n'as pas assez de cette carte pour proposer cet échange.")
            return

        tid = create_trade(from_id, to_id, {offered_card_id: offered_amount}, int(requested_credits))
        await ctx.send(f"Échange créé (ID `{tid}`) : {ctx.author.display_name} propose x{offered_amount} `{offered_card_id}` à {target.display_name} pour {requested_credits} CC. Le destinataire peut accepter avec `a!accepttrade {tid}`")

    @bot.command(name="accepttrade")
    async def accept_trade_cmd(ctx, trade_id: int):
        t = get_trade(trade_id)
        if not t:
            await ctx.send("Échange introuvable.")
            return
        if str(ctx.author.id) != t.get("to"):
            await ctx.send("Tu n'es pas le destinataire de cet échange.")
            return
        # Attempt accept
        ok = accept_trade(trade_id)
        if ok:
            await ctx.send(f"Échange `{trade_id}` accepté — transaction effectuée.")
        else:
            await ctx.send("Impossible d'accepter l'échange : fonds insuffisants ou carte manquante.")

    @bot.command(name="mycards")
    async def mycards(ctx):
        user_id = str(ctx.author.id)
        col = list_user_cards_pretty(user_id)
        if not col:
            await ctx.send("Tu n'as pas encore de cartes.")
            return
        embed = discord.Embed(title=f"Tes cartes — {ctx.author.display_name}", color=GREEN_COLOR)
        for item in col:
            title = item["meta"].get("title", item["card_id"])
            rarity = item["meta"].get("rarity", "common")
            embed.add_field(name=f"{title} — ({rarity})", value=f"x{item['count']} — id `{item['card_id']}`", inline=False)
        await ctx.send(embed=embed)

    # Admin: list trades
    @bot.command(name="listtrades")
    @commands.has_permissions(administrator=True)
    async def list_trades_cmd(ctx):
        from save_manager import load_data
        data = load_data()
        trades = data.get("trades", {})
        if not trades:
            await ctx.send("Aucun échange en attente.")
            return
        embed = discord.Embed(title="Échanges", color=GREEN_COLOR)
        for tid, info in trades.items():
            embed.add_field(name=f"ID {tid}", value=str(info), inline=False)
        await ctx.send(embed=embed)

    # Register setup message (optional)
    @bot.command(name="cardsetup")
    @commands.has_permissions(administrator=True)
    async def cardsetup(ctx):
        """Crée quelques cartes exemple (id, rareté, titre, image) — adapte les urls d'image."""
        # Exemple d'enregistrement de cartes (à personnaliser)
        cards_examples = [
            ("catenaccio_001", {"title": "Araki - Défenseur", "rarity": "common", "image": "https://i.postimg.cc/example1.png", "extras": "Défense solide"}),
            ("catenaccio_002", {"title": "Kobayashi - Tactique", "rarity": "rare", "image": "https://i.postimg.cc/example2.png", "extras": "Vision du jeu"}),
            ("catenaccio_003", {"title": "Capitaine - Légende", "rarity": "legendary", "image": "https://i.postimg.cc/example3.png", "extras": "Leader"}),
            ("catenaccio_mythique", {"title": "L'Inébranlable", "rarity": "mythique", "image": "https://i.postimg.cc/example4.png", "extras": "Évènement spécial"})
        ]
        for cid, meta in cards_examples:
            register_card(cid, meta)
        await ctx.send("Cartes d'exemple enregistrées. Modifie les metas et images comme tu veux.")
