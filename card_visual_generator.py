"""
Card Visual Generator - Génération de cartes visuelles en temps réel
====================================================================
Ce module génère des images de cartes professionnelles et les envoie
directement dans Discord au lieu d'utiliser des embeds.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import io
import aiohttp
import discord
from pathlib import Path

class CardVisualGenerator:
    """Générateur de cartes visuelles professionnelles"""
    
    def __init__(self):
        self.card_width = 700
        self.card_height = 1000
        self.cache_dir = Path("card_cache")
        self.cache_dir.mkdir(exist_ok=True)
        
        # Couleurs par rareté avec gradients
        self.rarity_gradients = {
            "Commune": {
                "primary": (128, 128, 128),
                "secondary": (80, 80, 80),
                "glow": (150, 150, 150)
            },
            "Rare": {
                "primary": (0, 153, 255),
                "secondary": (0, 100, 200),
                "glow": (100, 200, 255)
            },
            "Épique": {
                "primary": (157, 0, 255),
                "secondary": (100, 0, 180),
                "glow": (200, 100, 255)
            },
            "Légendaire": {
                "primary": (255, 215, 0),
                "secondary": (200, 150, 0),
                "glow": (255, 255, 100)
            },
            "Mythique": {
                "primary": (255, 0, 0),
                "secondary": (180, 0, 0),
                "glow": (255, 100, 100)
            }
        }
        
        # Chemins des polices
        self.fonts = self._load_fonts()
    
    def _load_fonts(self):
        """Charge les polices système"""
        try:
            return {
                'title': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60),
                'subtitle': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40),
                'stat_name': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28),
                'stat_value': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36),
                'small': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24),
                'tiny': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
            }
        except:
            # Fallback sur police par défaut
            default = ImageFont.load_default()
            return {
                'title': default,
                'subtitle': default,
                'stat_name': default,
                'stat_value': default,
                'small': default,
                'tiny': default
            }
    
    def _create_radial_gradient(self, size, center_color, edge_color):
        """Crée un gradient radial"""
        width, height = size
        gradient = Image.new('RGB', size)
        draw = ImageDraw.Draw(gradient)
        
        max_distance = ((width/2)**2 + (height/2)**2)**0.5
        
        for y in range(height):
            for x in range(width):
                # Distance du centre
                distance = ((x - width/2)**2 + (y - height/2)**2)**0.5
                ratio = min(distance / max_distance, 1.0)
                
                r = int(center_color[0] * (1-ratio) + edge_color[0] * ratio)
                g = int(center_color[1] * (1-ratio) + edge_color[1] * ratio)
                b = int(center_color[2] * (1-ratio) + edge_color[2] * ratio)
                
                gradient.putpixel((x, y), (r, g, b))
        
        return gradient
    
    def _add_glow_effect(self, image, color, intensity=20):
        """Ajoute un effet de glow lumineux"""
        # Créer un calque de glow
        glow = Image.new('RGBA', image.size, (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        
        # Dessiner le glow
        for i in range(intensity):
            alpha = int(255 * (1 - i/intensity) * 0.3)
            glow_color = (*color, alpha)
            offset = i * 2
            glow_draw.rectangle(
                [(offset, offset), (image.width - offset, image.height - offset)],
                outline=glow_color,
                width=2
            )
        
        # Appliquer le blur
        glow = glow.filter(ImageFilter.GaussianBlur(intensity/2))
        
        # Composer
        result = Image.alpha_composite(image.convert('RGBA'), glow)
        return result
    
    def _draw_stat_bar_advanced(self, draw, x, y, value, stat_name, max_value=100):
        """Dessine une barre de stat avancée avec gradient"""
        bar_width = 500
        bar_height = 35
        
        # Couleur selon la valeur
        if value >= 90:
            bar_color = (76, 175, 80)  # Vert
            bar_glow = (100, 255, 100)
        elif value >= 75:
            bar_color = (255, 193, 7)  # Jaune
            bar_glow = (255, 255, 100)
        elif value >= 60:
            bar_color = (255, 152, 0)  # Orange
            bar_glow = (255, 200, 100)
        else:
            bar_color = (244, 67, 54)  # Rouge
            bar_glow = (255, 150, 150)
        
        # Fond de la barre (sombre)
        draw.rounded_rectangle(
            [(x, y), (x + bar_width, y + bar_height)],
            radius=15,
            fill=(30, 30, 30),
            outline=(80, 80, 80),
            width=2
        )
        
        # Barre de progression
        filled_width = int((value / max_value) * bar_width)
        if filled_width > 0:
            # Créer un mini gradient pour la barre
            for i in range(filled_width):
                ratio = i / filled_width
                r = int(bar_color[0] * (1-ratio*0.3) + bar_glow[0] * ratio*0.3)
                g = int(bar_color[1] * (1-ratio*0.3) + bar_glow[1] * ratio*0.3)
                b = int(bar_color[2] * (1-ratio*0.3) + bar_glow[2] * ratio*0.3)
                
                draw.rectangle(
                    [(x + i, y + 2), (x + i + 1, y + bar_height - 2)],
                    fill=(r, g, b)
                )
            
            # Arrondir les coins
            draw.rounded_rectangle(
                [(x, y), (x + filled_width, y + bar_height)],
                radius=15,
                outline=None
            )
        
        # Valeur de la stat
        value_text = str(value)
        bbox = draw.textbbox((0, 0), value_text, font=self.fonts['stat_value'])
        text_width = bbox[2] - bbox[0]
        
        # Ombre du texte
        draw.text(
            (x + bar_width + 22, y + 2),
            value_text,
            fill=(0, 0, 0),
            font=self.fonts['stat_value']
        )
        # Texte principal
        draw.text(
            (x + bar_width + 20, y),
            value_text,
            fill=(255, 255, 255),
            font=self.fonts['stat_value']
        )
    
    async def _download_image(self, url):
        """Télécharge une image depuis une URL"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.read()
                        return Image.open(io.BytesIO(data))
        except Exception as e:
            print(f"Erreur téléchargement image: {e}")
            return None
    
    async def generate_card_image(self, card_data):
        """
        Génère une image de carte complète
        
        Returns:
            discord.File: Fichier image prêt à être envoyé sur Discord
        """
        rarity = card_data.get('rarity', 'Commune')
        colors = self.rarity_gradients[rarity]
        
        # === CRÉATION DU FOND ===
        # Gradient radial
        card = self._create_radial_gradient(
            (self.card_width, self.card_height),
            colors['secondary'],
            (20, 20, 20)
        )
        
        # Ajouter un effet de glow
        card = self._add_glow_effect(card, colors['glow'], intensity=15)
        
        draw = ImageDraw.Draw(card)
        
        # === BORDURES DÉCORATIVES ===
        # Bordure extérieure avec gradient
        for i in range(10):
            alpha = int(255 * (1 - i/10))
            draw.rectangle(
                [(i, i), (self.card_width - i, self.card_height - i)],
                outline=(*colors['primary'], alpha) if i < 5 else (*colors['glow'], alpha),
                width=2
            )
        
        # Ligne de séparation haute
        draw.rectangle(
            [(0, 0), (self.card_width, 20)],
            fill=colors['primary']
        )
        
        # === NOM DU JOUEUR ===
        name = card_data.get('name', 'Joueur')
        
        # Ombre du nom
        name_bbox = draw.textbbox((0, 0), name, font=self.fonts['title'])
        name_width = name_bbox[2] - name_bbox[0]
        name_x = (self.card_width - name_width) // 2
        
        draw.text(
            (name_x + 3, 43),
            name,
            fill=(0, 0, 0),
            font=self.fonts['title']
        )
        # Nom principal
        draw.text(
            (name_x, 40),
            name,
            fill=(255, 255, 255),
            font=self.fonts['title']
        )
        
        # === POSITION ET RARETÉ ===
        position = card_data.get('position', 'Joueur')
        position_emojis = {
            'Défense': '🛡️',
            'Milieu': '⚙️',
            'Attaque': '⚔️',
            'Gardien': '🧤',
            'Technique': '📋'
        }
        emoji = position_emojis.get(position, '⚽')
        
        subtitle = f"{emoji} {position} • {rarity}"
        subtitle_bbox = draw.textbbox((0, 0), subtitle, font=self.fonts['subtitle'])
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        
        draw.text(
            ((self.card_width - subtitle_width) // 2, 115),
            subtitle,
            fill=colors['glow'],
            font=self.fonts['subtitle']
        )
        
        # === IMAGE DU JOUEUR ===
        player_img_y = 180
        player_img_size = 350
        
        # Télécharger l'image si URL fournie
        player_image = None
        if card_data.get('image_url'):
            player_image = await self._download_image(card_data['image_url'])
        
        if player_image:
            # Redimensionner en gardant le ratio
            player_image.thumbnail((player_img_size, player_img_size), Image.Resampling.LANCZOS)
            
            # Créer un masque circulaire
            mask = Image.new('L', (player_img_size, player_img_size), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0, player_img_size, player_img_size), fill=255)
            
            # Créer un fond blanc pour l'image
            img_bg = Image.new('RGB', (player_img_size, player_img_size), (255, 255, 255))
            img_bg.paste(player_image, (0, 0))
            
            # Position centrée
            img_x = (self.card_width - player_img_size) // 2
            
            # Cercle de glow autour de l'image
            for i in range(8, 0, -1):
                alpha = int(100 * (1 - i/8))
                draw.ellipse(
                    [(img_x - i*3, player_img_y - i*3),
                     (img_x + player_img_size + i*3, player_img_y + player_img_size + i*3)],
                    outline=(*colors['glow'], alpha),
                    width=3
                )
            
            # Coller l'image
            card.paste(img_bg, (img_x, player_img_y), mask)
            
            # Bordure du cercle
            draw.ellipse(
                [(img_x, player_img_y), (img_x + player_img_size, player_img_y + player_img_size)],
                outline=colors['primary'],
                width=6
            )
        else:
            # Placeholder si pas d'image
            img_x = (self.card_width - player_img_size) // 2
            draw.ellipse(
                [(img_x, player_img_y), (img_x + player_img_size, player_img_y + player_img_size)],
                fill=(40, 40, 40),
                outline=colors['primary'],
                width=6
            )
            
            # Icône de position
            icon_bbox = draw.textbbox((0, 0), emoji, font=self.fonts['title'])
            icon_width = icon_bbox[2] - icon_bbox[0]
            draw.text(
                ((self.card_width - icon_width) // 2, player_img_y + 150),
                emoji,
                font=self.fonts['title']
            )
        
        # === NOTE GLOBALE (OVR) ===
        stats = card_data.get('stats', {})
        overall = sum(stats.values()) // len(stats) if stats else 0
        
        ovr_y = player_img_y + player_img_size + 20
        ovr_size = 140
        ovr_x = (self.card_width - ovr_size) // 2
        
        # Cercle de glow pour OVR
        for i in range(10, 0, -1):
            alpha = int(150 * (1 - i/10))
            draw.ellipse(
                [(ovr_x - i*2, ovr_y - i*2),
                 (ovr_x + ovr_size + i*2, ovr_y + ovr_size + i*2)],
                fill=(*colors['glow'], alpha)
            )
        
        # Cercle principal
        draw.ellipse(
            [(ovr_x, ovr_y), (ovr_x + ovr_size, ovr_y + ovr_size)],
            fill=(20, 20, 20),
            outline=colors['primary'],
            width=8
        )
        
        # Note OVR
        ovr_text = str(overall)
        ovr_bbox = draw.textbbox((0, 0), ovr_text, font=self.fonts['title'])
        ovr_width = ovr_bbox[2] - ovr_bbox[0]
        
        # Déterminer la couleur selon la note
        if overall >= 90:
            ovr_color = (76, 175, 80)
        elif overall >= 80:
            ovr_color = (255, 193, 7)
        elif overall >= 70:
            ovr_color = (255, 152, 0)
        else:
            ovr_color = (244, 67, 54)
        
        draw.text(
            ((self.card_width - ovr_width) // 2, ovr_y + 25),
            ovr_text,
            fill=ovr_color,
            font=self.fonts['title']
        )
        
        # Label OVR
        label = "OVR"
        label_bbox = draw.textbbox((0, 0), label, font=self.fonts['small'])
        label_width = label_bbox[2] - label_bbox[0]
        draw.text(
            ((self.card_width - label_width) // 2, ovr_y + 95),
            label,
            fill=(180, 180, 180),
            font=self.fonts['small']
        )
        
        # === STATISTIQUES ===
        stats_y = ovr_y + ovr_size + 30
        
        stat_emojis = {
            'vitesse': '⚡',
            'defense': '🛡️',
            'attaque': '⚔️',
            'technique': '🎯',
            'physique': '💪',
            'mental': '🧠'
        }
        
        y_offset = 0
        for stat_name, stat_value in stats.items():
            emoji = stat_emojis.get(stat_name, '📊')
            label = f"{emoji} {stat_name.upper()}"
            
            # Label de la stat
            draw.text(
                (40, stats_y + y_offset),
                label,
                fill=(220, 220, 220),
                font=self.fonts['stat_name']
            )
            
            # Barre de progression
            self._draw_stat_bar_advanced(
                draw,
                40,
                stats_y + y_offset + 35,
                stat_value,
                stat_name
            )
            
            y_offset += 80
        
        # === CAPACITÉ SPÉCIALE ===
        special = card_data.get('special_ability', '')
        if special:
            # Rectangle de fond avec gradient
            footer_y = self.card_height - 90
            
            draw.rounded_rectangle(
                [(30, footer_y), (self.card_width - 30, footer_y + 55)],
                radius=15,
                fill=(0, 0, 0, 200)
            )
            
            draw.rounded_rectangle(
                [(30, footer_y), (self.card_width - 30, footer_y + 55)],
                radius=15,
                outline=colors['primary'],
                width=3
            )
            
            # Texte de la capacité
            special_text = f"⚡ {special}"
            special_bbox = draw.textbbox((0, 0), special_text, font=self.fonts['small'])
            special_width = special_bbox[2] - special_bbox[0]
            
            draw.text(
                ((self.card_width - special_width) // 2, footer_y + 17),
                special_text,
                fill=colors['glow'],
                font=self.fonts['small']
            )
        
        # === BORDURE INFÉRIEURE ===
        draw.rectangle(
            [(0, self.card_height - 20), (self.card_width, self.card_height)],
            fill=colors['primary']
        )
        
        # === NATIONALITÉ (petit drapeau) ===
        nationality = card_data.get('nationality', '')
        if nationality:
            draw.text(
                (20, self.card_height - 45),
                nationality,
                fill=(255, 255, 255),
                font=self.fonts['tiny']
            )
        
        # === CONVERSION EN FICHIER DISCORD ===
        # Sauvegarder dans un buffer
        buffer = io.BytesIO()
        card.save(buffer, 'PNG', quality=95)
        buffer.seek(0)
        
        # Créer le fichier Discord
        filename = f"{name}_{rarity}.png"
        discord_file = discord.File(buffer, filename=filename)
        
        return discord_file

# Instance globale
card_visual_gen = CardVisualGenerator()
