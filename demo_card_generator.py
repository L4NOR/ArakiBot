"""
Script de Démonstration - Générateur de Cartes Visuelles
=========================================================
Ce script teste le générateur et crée des exemples de cartes
"""

import asyncio
from card_visual_generator import CardVisualGenerator
from pathlib import Path

# Exemples de données de cartes
DEMO_CARDS = [
    {
        "name": "ARAKI",
        "position": "Défense",
        "rarity": "Mythique",
        "stats": {
            "vitesse": 88,
            "defense": 99,
            "attaque": 75,
            "technique": 92,
            "physique": 90,
            "mental": 95
        },
        "description": "Le génie tactique de la défense",
        "image_url": None,  # Pas d'image pour la démo
        "special_ability": "Catenaccio Perfect",
        "nationality": "🇯🇵 Japon",
        "id": "Araki_Mythique_9999"
    },
    {
        "name": "TAKAHASHI",
        "position": "Attaque",
        "rarity": "Légendaire",
        "stats": {
            "vitesse": 94,
            "defense": 58,
            "attaque": 96,
            "technique": 90,
            "physique": 80,
            "mental": 88
        },
        "description": "Le finisseur ultime",
        "image_url": None,
        "special_ability": "Instinct du Buteur",
        "nationality": "🇯🇵 Japon",
        "id": "Takahashi_Legendaire_8888"
    },
    {
        "name": "NAKAMURA",
        "position": "Milieu",
        "rarity": "Légendaire",
        "stats": {
            "vitesse": 86,
            "defense": 80,
            "attaque": 88,
            "technique": 93,
            "physique": 82,
            "mental": 90
        },
        "description": "Maestro du milieu de terrain",
        "image_url": None,
        "special_ability": "Vision de Jeu",
        "nationality": "🇯🇵 Japon",
        "id": "Nakamura_Legendaire_7777"
    },
    {
        "name": "TANAKA",
        "position": "Défense",
        "rarity": "Épique",
        "stats": {
            "vitesse": 78,
            "defense": 85,
            "attaque": 62,
            "technique": 79,
            "physique": 84,
            "mental": 80
        },
        "description": "Spécialiste du marquage",
        "image_url": None,
        "special_ability": "Marquage Serré",
        "nationality": "🇯🇵 Japon",
        "id": "Tanaka_Epique_6666"
    },
    {
        "name": "WATANABE",
        "position": "Milieu",
        "rarity": "Rare",
        "stats": {
            "vitesse": 74,
            "defense": 70,
            "attaque": 76,
            "technique": 80,
            "physique": 72,
            "mental": 75
        },
        "description": "Milieu box-to-box",
        "image_url": None,
        "special_ability": "Course Explosive",
        "nationality": "🇯🇵 Japon",
        "id": "Watanabe_Rare_5555"
    },
    {
        "name": "SATO",
        "position": "Défense",
        "rarity": "Commune",
        "stats": {
            "vitesse": 65,
            "defense": 70,
            "attaque": 48,
            "technique": 62,
            "physique": 68,
            "mental": 65
        },
        "description": "Jeune espoir défensif",
        "image_url": None,
        "special_ability": "Détermination",
        "nationality": "🇯🇵 Japon",
        "id": "Sato_Commune_4444"
    },
    {
        "name": "CATENACCIO",
        "position": "Technique",
        "rarity": "Mythique",
        "stats": {
            "vitesse": 75,
            "defense": 99,
            "attaque": 65,
            "technique": 98,
            "physique": 80,
            "mental": 97
        },
        "description": "La tactique défensive ultime",
        "image_url": None,
        "special_ability": "Défense Absolue",
        "nationality": "🇮🇹 Italie",
        "id": "Catenaccio_Mythique_3333"
    }
]

async def generate_demo_cards():
    """Génère toutes les cartes de démo"""
    
    print("🎨 GÉNÉRATEUR DE CARTES VISUELLES - DÉMONSTRATION")
    print("=" * 60)
    
    # Créer le dossier de sortie
    output_dir = Path("demo_cards")
    output_dir.mkdir(exist_ok=True)
    
    # Créer le générateur
    generator = CardVisualGenerator()
    
    print(f"\n📁 Les cartes seront sauvegardées dans : {output_dir}/")
    print(f"📊 Génération de {len(DEMO_CARDS)} cartes...\n")
    
    for i, card_data in enumerate(DEMO_CARDS, 1):
        print(f"[{i}/{len(DEMO_CARDS)}] Génération de {card_data['name']} ({card_data['rarity']})...", end=" ")
        
        try:
            # Générer l'image
            card_file = await generator.generate_card_image(card_data)
            
            # Sauvegarder dans le dossier de démo
            filename = f"{card_data['name']}_{card_data['rarity']}.png"
            output_path = output_dir / filename
            
            # Lire les données du fichier Discord et les sauvegarder
            with open(output_path, 'wb') as f:
                card_file.fp.seek(0)
                f.write(card_file.fp.read())
            
            # Calculer la note globale
            overall = sum(card_data['stats'].values()) // len(card_data['stats'])
            
            print(f"✅ Terminé ! (OVR: {overall})")
            
        except Exception as e:
            print(f"❌ Erreur : {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎉 GÉNÉRATION TERMINÉE !")
    print(f"\n📂 Vos cartes sont dans le dossier : {output_dir}/")
    print("\n📸 Vous pouvez maintenant :")
    print("   1. Visualiser les images générées")
    print("   2. Les uploader sur Imgur")
    print("   3. Copier les URLs dans votre code")
    print("\n💡 Conseil : Uploadez-les sur Imgur pour avoir des URLs permanentes")

def show_card_info():
    """Affiche les informations sur les cartes générées"""
    
    print("\n📋 CARTES GÉNÉRÉES :\n")
    
    rarities = {}
    for card in DEMO_CARDS:
        rarity = card['rarity']
        if rarity not in rarities:
            rarities[rarity] = []
        rarities[rarity].append(card)
    
    # Emojis par rareté
    rarity_emojis = {
        "Mythique": "🔴",
        "Légendaire": "🟡",
        "Épique": "🟣",
        "Rare": "🔵",
        "Commune": "⚪"
    }
    
    for rarity in ["Mythique", "Légendaire", "Épique", "Rare", "Commune"]:
        if rarity in rarities:
            cards = rarities[rarity]
            emoji = rarity_emojis.get(rarity, "⚽")
            print(f"{emoji} {rarity} ({len(cards)}) :")
            
            for card in cards:
                overall = sum(card['stats'].values()) // len(card['stats'])
                print(f"   • {card['name']} (OVR {overall}) - {card['position']}")
            
            print()

def show_next_steps():
    """Affiche les prochaines étapes"""
    
    print("\n🚀 PROCHAINES ÉTAPES :\n")
    
    steps = [
        "1️⃣  Ouvrir le dossier demo_cards/ et visualiser vos cartes",
        "2️⃣  Uploader les images sur Imgur.com (gratuit)",
        "3️⃣  Copier les URLs directes (clic droit > copier le lien de l'image)",
        "4️⃣  Remplacer les 'image_url' dans cards_ultra_visual.py",
        "5️⃣  Installer le nouveau système : mv cards_ultra_visual.py cards.py",
        "6️⃣  Redémarrer votre bot : python main.py",
        "7️⃣  Tester avec : a!card_visual <id>",
        "8️⃣  Profiter de vos cartes ULTRA-VISUELLES ! 🎉"
    ]
    
    for step in steps:
        print(f"   {step}")
    
    print("\n💡 ASTUCE : Pour ajouter vos propres images de joueurs :")
    print("   - Cherchez des images de personnages de manga/anime")
    print("   - Utilisez des générateurs d'IA (Midjourney, DALL-E)")
    print("   - Créez vos propres illustrations")

def show_customization_tips():
    """Affiche des conseils de personnalisation"""
    
    print("\n🎨 PERSONNALISATION :\n")
    
    tips = [
        "🌈 Changer les couleurs → card_visual_generator.py > self.rarity_gradients",
        "📏 Modifier la taille → card_visual_generator.py > self.card_width/height",
        "✨ Ajuster le glow → generate_card_image() > intensity parameter",
        "🖼️  Changer le style → Modifier les draw functions",
        "⚡ Ajouter des effets → Utiliser ImageFilter de PIL"
    ]
    
    for tip in tips:
        print(f"   {tip}")

if __name__ == "__main__":
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print("║     🎴 DÉMO - GÉNÉRATEUR DE CARTES VISUELLES 🎴          ║")
    print("║                                                           ║")
    print("║           Bot Discord Catenaccio - Par Orlan             ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    
    # Afficher les infos
    show_card_info()
    
    # Question pour lancer la génération
    response = input("\n❓ Voulez-vous générer les cartes de démo ? (o/n) : ").lower()
    
    if response == 'o' or response == 'oui' or response == 'y' or response == 'yes':
        # Lancer la génération
        asyncio.run(generate_demo_cards())
        
        # Afficher les prochaines étapes
        show_next_steps()
        show_customization_tips()
        
        print("\n✨ Merci d'avoir utilisé le générateur de cartes !")
        print("⚽ Bon développement avec votre bot Catenaccio ! 🎴\n")
    else:
        print("\n❌ Génération annulée.")
        print("💡 Lancez ce script à nouveau quand vous serez prêt !\n")
