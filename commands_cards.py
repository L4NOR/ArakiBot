import discord
from discord.ext import commands
from card_system import (
    create_account, open_pack, get_collection,
    start_trade, accept_trade
)


def setup_card_commands(bot):

    # ----------------------
    # a!start
    # ----------------------
    @bot.command(name="start")
    async def start_cmd(ctx):
        created = create_account(str(ctx.author.id))
        if created:
            await ctx.send("🎉 Compte créé ! Tu commences avec **200 crédits**.")
        else:
            await ctx.send("Tu as déjà un compte !")

    # ----------------------
    # a!pack <type>
    # ----------------------
    @bot.command(name="pack")
    async def pack_cmd(ctx, pack_type=None):
        if pack_type is None:
            return await ctx.send("Usage : `a!pack bronze / argent / or / platine`")

        ok, result = open_pack(str(ctx.author.id), pack_type.lower())

        if not ok:
            return await ctx.send(result)

        embed = discord.Embed(
            title="🎁 Pack ouvert",
            description=f"Tu as obtenu {len(result)} cartes !",
            color=0x00FF00
        )

        for c in result:
            embed.add_field(
                name=f"{c['rarity']} 🟦 | ID {c['id']}",
                value=f"**{c['stat']}** : {c['value']}",
                inline=False
            )

        await ctx.send(embed=embed)

    # ----------------------
    # a!collection
    # ----------------------
    @bot.command(name="collection")
    async def collection_cmd(ctx):
        cards = get_collection(str(ctx.author.id))

        if cards is None:
            return await ctx.send("Fais `a!start` d’abord.")

        if len(cards) == 0:
            return await ctx.send("Tu n'as aucune carte 😭")

        embed = discord.Embed(
            title=f"📚 Collection de {ctx.author.name}",
            color=0x00FF00
        )

        for c in cards:
            embed.add_field(
                name=f"{c['rarity']} | ID {c['id']}",
                value=f"{c['stat']} : **{c['value']}**",
                inline=False
            )

        await ctx.send(embed=embed)

    # ----------------------
    # a!trade @user <id_carte> <prix>
    # ----------------------
    @bot.command(name="trade")
    async def trade_cmd(ctx, user: discord.User = None, card_id=None, price: int = None):
        if user is None or card_id is None or price is None:
            return await ctx.send("Usage : `a!trade @user <id_carte> <prix>`")

        ok, msg = start_trade(str(ctx.author.id), str(user.id), card_id, price)

        if not ok:
            return await ctx.send(msg)

        await ctx.send(f"📨 Offre envoyée à {user.mention} ! Il doit faire `a!accept`.")

    # ----------------------
    # a!accept
    # ----------------------
    @bot.command(name="accept")
    async def accept_cmd(ctx):
        ok, msg = accept_trade(str(ctx.author.id))

        if not ok:
            return await ctx.send(msg)

        await ctx.send("🎉 Échange effectué avec succès !")
