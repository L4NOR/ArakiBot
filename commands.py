import discord
from discord.ext import commands
from config import GREEN_COLOR, DARK_BLUE_COLOR, ROLE_CATENACCIO_ID, ANNOUNCEMENTS_CHANNEL_ID, ANNOUNCEMENT_REACTIONS
from config import DISCUSSIONS_CATEGORY_ID, THREAD_AUTO_ARCHIVE_DURATION

# ID du canal de test
TEST_CHANNEL_ID = 1330221808753840159

def setup_commands(bot):
    # Commande Araki (aide)
    @bot.command(name='Araki')
    async def help_command(ctx):
        embed = discord.Embed(
            title="⚽ Guide du Bot Catenaccio ⚽",
            description=(
                "Bienvenue sur le terrain de Catenaccio ! \n"
                "🤖 Votre assistant de communauté dédié aux fans du manga de football"
            ),
            color=GREEN_COLOR
        )

        # Section informative avec plus de détails
        embed.add_field(
            name="🌟 Fonctionnalités du Bot",
            value=(
                "• 👋 Gestion des messages de bienvenue dans l'univers de Catenaccio\n"
                "• 📣 Notifications de nouveaux chapitres\n"
                "• 🏷️ Suivi automatique des rôles\n"
                "• 🔔 Alertes communautaires"
            ),
            inline=False
        )

        # Nouveaux détails interactifs
        embed.add_field(
            name="🎉 Interaction Communautaire",
            value=(
                "• Réactions automatiques aux annonces\n"
                "• Mentions de rôles personnalisées"
            ),
            inline=False
        )

        embed.set_footer(
            text="Un problème ? Contactez les administrateurs | Powered by Catenaccio Bot ⚽🛡️",
        )

        await ctx.send(embed=embed)

    # Commande pour annoncer un nouveau chapitre
    @bot.command(name='newchapter_catenaccio')
    @commands.has_permissions(administrator=True)
    async def announce_new_chapter(ctx, *args):
        if ctx.channel.id != ANNOUNCEMENTS_CHANNEL_ID:
            await ctx.send("Cette commande ne peut être utilisée que dans le canal d'annonces approprié.")
            return
        
        # Vérifier qu'il y a au moins 2 arguments (au moins un numéro de chapitre et un lien)
        if len(args) < 2:
            await ctx.send("Syntaxe incorrecte. Utilisez `!newchapter_catenaccio <numéros_chapitres> <lien> [description]`")
            return
        
        # Trouver où se termine la liste des chapitres et où commence le lien
        chapter_numbers = []
        link_index = 0
        
        for i, arg in enumerate(args):
            # Si l'argument ressemble à un URL (commence par http), c'est notre lien
            if arg.startswith("http"):
                link_index = i
                break
            # Sinon, c'est un numéro de chapitre
            chapter_numbers.append(arg)
        
        # Si aucun lien n'a été trouvé
        if link_index == 0:
            await ctx.send("Lien manquant. Utilisez `!newchapter_catenaccio <numéros_chapitres> <lien> [description]`")
            return
        
        chapter_link = args[link_index]
        
        # Récupérer la description si elle existe (tout ce qui vient après le lien)
        description = None
        if link_index + 1 < len(args):
            description = " ".join(args[link_index + 1:])
        
        # Formater les numéros de chapitres pour l'affichage
        chapters_display = ", ".join(chapter_numbers)
        
        role_id = ROLE_CATENACCIO_ID
        role = ctx.guild.get_role(role_id)
        
        if not role:
            await ctx.send("Le rôle spécifié n'a pas été trouvé.")
            return

        # Créer l'embed avec un design amélioré
        embed = discord.Embed(
            title="⚽ NOUVEAU(X) CHAPITRE(S) DE CATENACCIO ⚽",
            description=(
                "De nouveaux chapitres viennent d'arriver ! Préparez-vous à suivre les exploits "
                "d'Araki et son équipe dans leur quête pour devenir les meilleurs défenseurs du football !\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━"
            ),
            color=DARK_BLUE_COLOR
        )
        
        # Informations sur le chapitre
        embed.add_field(
            name="📖 Chapitre(s)",
            value=f"**#{chapters_display}**",
            inline=True
        )
        
        embed.add_field(
            name="⏰ Disponible",
            value="**MAINTENANT !**",
            inline=True
        )
        
        # Lien de lecture
        embed.add_field(
            name="📚 Lien de lecture",
            value=f"[Cliquez ici pour lire le(s) chapitre(s) !]({chapter_link})",
            inline=False
        )
        
        # Séparateur
        embed.add_field(
            name="━━━━━━━━━━━━━━━━━━━━━━",
            value="",
            inline=False
        )
        
        # Description si fournie
        if description:
            embed.add_field(
                name="🔍 Aperçu",
                value=f"{description}",
                inline=False
            )
        
        # Note de bas de page
        embed.set_footer(
            text=(
                "N'oubliez pas de partager vos analyses tactiques et réactions sur twitter et discord ! "
                "Bonne lecture à tous ! 🎉"
            )
        )
        
        # Petit rappel en haut du message
        reminder_text = (
            f"{role.mention}\n"
            "───────────────────────\n"
            "**De nouveaux chapitres viennent d'être publiés !**\n"
            "Retrouvez tous les détails ci-dessous ⬇️"
        )

        # Envoyer l'annonce
        announcement = await ctx.send(reminder_text, embed=embed)
        
        # Ajouter plusieurs réactions
        for reaction in ANNOUNCEMENT_REACTIONS:
            await announcement.add_reaction(reaction)
        
        # Supprimer la commande originale
        await ctx.message.delete()

    # Commande TEST pour annoncer un nouveau chapitre
    @bot.command(name='test_newchapter_catenaccio')
    @commands.has_permissions(administrator=True)
    async def test_announce_new_chapter(ctx, *args):
        if ctx.channel.id != TEST_CHANNEL_ID:
            await ctx.send("Cette commande ne peut être utilisée que dans le canal de test.")
            return
        
        # Vérifier qu'il y a au moins 2 arguments (au moins un numéro de chapitre et un lien)
        if len(args) < 2:
            await ctx.send("Syntaxe incorrecte. Utilisez `!test_newchapter_catenaccio <numéros_chapitres> <lien> [description]`")
            return
        
        # Trouver où se termine la liste des chapitres et où commence le lien
        chapter_numbers = []
        link_index = 0
        
        for i, arg in enumerate(args):
            # Si l'argument ressemble à un URL (commence par http), c'est notre lien
            if arg.startswith("http"):
                link_index = i
                break
            # Sinon, c'est un numéro de chapitre
            chapter_numbers.append(arg)
        
        # Si aucun lien n'a été trouvé
        if link_index == 0:
            await ctx.send("Lien manquant. Utilisez `!test_newchapter_catenaccio <numéros_chapitres> <lien> [description]`")
            return
        
        chapter_link = args[link_index]
        
        # Récupérer la description si elle existe (tout ce qui vient après le lien)
        description = None
        if link_index + 1 < len(args):
            description = " ".join(args[link_index + 1:])
        
        # Formater les numéros de chapitres pour l'affichage
        chapters_display = ", ".join(chapter_numbers)
        
        role_id = ROLE_CATENACCIO_ID
        role = ctx.guild.get_role(role_id)
        
        if not role:
            await ctx.send("Le rôle spécifié n'a pas été trouvé.")
            return

        # Créer l'embed avec un design amélioré
        embed = discord.Embed(
            title="⚽ [TEST] NOUVEAU(X) CHAPITRE(S) DE CATENACCIO ⚽",
            description=(
                "**⚠️ CECI EST UN TEST ⚠️**\n\n"
                "De nouveaux chapitres viennent d'arriver ! Préparez-vous à suivre les exploits "
                "d'Araki et son équipe dans leur quête pour devenir les meilleurs défenseurs du football !\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━"
            ),
            color=DARK_BLUE_COLOR
        )
        
        # Informations sur le chapitre
        embed.add_field(
            name="📖 Chapitre(s)",
            value=f"**#{chapters_display}**",
            inline=True
        )
        
        embed.add_field(
            name="⏰ Disponible",
            value="**MAINTENANT !**",
            inline=True
        )
        
        # Lien de lecture
        embed.add_field(
            name="📚 Lien de lecture",
            value=f"[Cliquez ici pour lire le(s) chapitre(s) !]({chapter_link})",
            inline=False
        )
        
        # Séparateur
        embed.add_field(
            name="━━━━━━━━━━━━━━━━━━━━━━",
            value="",
            inline=False
        )
        
        # Description si fournie
        if description:
            embed.add_field(
                name="🔍 Aperçu",
                value=f"{description}",
                inline=False
            )
        
        # Note de bas de page
        embed.set_footer(
            text=(
                "N'oubliez pas de partager vos analyses tactiques et réactions sur twitter et discord ! "
                "Bonne lecture à tous ! 🎉"
            )
        )
        
        # Petit rappel en haut du message
        reminder_text = (
            f"{role.mention}\n"
            "───────────────────────\n"
            "**[TEST] De nouveaux chapitres viennent d'être publiés !**\n"
            "Retrouvez tous les détails ci-dessous ⬇️"
        )

        # Envoyer l'annonce
        announcement = await ctx.send(reminder_text, embed=embed)
        
        # Ajouter plusieurs réactions
        for reaction in ANNOUNCEMENT_REACTIONS:
            await announcement.add_reaction(reaction)
        
        # Supprimer la commande originale
        await ctx.message.delete()

    # Gestion des erreurs pour la commande newchapter_catenaccio
    @announce_new_chapter.error
    async def announce_new_chapter_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Il manque des arguments. Usage: !newchapter_catenaccio <numéros_chapitres> <lien> [description]")
        else:
            await ctx.send(f"Une erreur s'est produite: {str(error)}")

    # Gestion des erreurs pour la commande test
    @test_announce_new_chapter.error
    async def test_announce_new_chapter_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Il manque des arguments. Usage: !test_newchapter_catenaccio <numéros_chapitres> <lien> [description]")
        else:
            await ctx.send(f"Une erreur s'est produite: {str(error)}")

    # Commande pour donner une récapitulation du dernier chapitre
    @bot.command(name='recap')
    async def recap_command(ctx):
        # Informations sur le dernier chapitre (à mettre à jour)
        last_chapter_number = "XX"  # Numéro du chapitre
        last_chapter_title = "Titre du chapitre"  # Titre du chapitre
        last_chapter_summary = (
            "Araki et son équipe continuent leur progression dans le monde du football défensif. "
            "Ce chapitre met en lumière les stratégies tactiques et la détermination de l'équipe "
            "face à un adversaire redoutable."
        )  # Résumé du chapitre
        chapter_link = "https://votre-lien-vers-le-chapitre.com"  # Lien vers le chapitre

        # Création de l'embed
        embed = discord.Embed(
            title=f"📖 Récapitulatif du Chapitre #{last_chapter_number}",
            description=f"**{last_chapter_title}**",
            color=GREEN_COLOR
        )

        # Ajouter le résumé
        embed.add_field(
            name="Résumé",
            value=last_chapter_summary,
            inline=False
        )

        # Ajouter le lien vers le chapitre
        embed.add_field(
            name="📚 Lien vers le chapitre",
            value=f"[Cliquez ici pour lire le chapitre]({chapter_link})",
            inline=False
        )

        # Ajouter une note de bas de page
        embed.set_footer(
            text="Restez connectés pour le prochain match !",
        )

        # Envoyer l'embed
        await ctx.send(embed=embed)