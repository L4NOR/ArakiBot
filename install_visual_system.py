#!/usr/bin/env python3
"""
Script d'Installation Automatique - Système de Cartes Ultra-Visuel
===================================================================
Ce script intègre automatiquement le nouveau système visuel avec 
vos fichiers existants et migre vos données.
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path

class ColoredText:
    """Couleurs pour le terminal"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header():
    """Affiche l'en-tête du script"""
    print("\n" + "="*70)
    print(ColoredText.BOLD + ColoredText.CYAN + 
          "🎴 INSTALLATION - SYSTÈME DE CARTES ULTRA-VISUEL 🎴" + 
          ColoredText.END)
    print(ColoredText.BLUE + "Bot Discord Catenaccio - Par Orlan" + ColoredText.END)
    print("="*70 + "\n")

def print_step(step_num, total_steps, message):
    """Affiche une étape"""
    print(f"{ColoredText.BOLD}[{step_num}/{total_steps}]{ColoredText.END} {message}")

def print_success(message):
    """Affiche un message de succès"""
    print(f"{ColoredText.GREEN}✅ {message}{ColoredText.END}")

def print_warning(message):
    """Affiche un avertissement"""
    print(f"{ColoredText.YELLOW}⚠️  {message}{ColoredText.END}")

def print_error(message):
    """Affiche une erreur"""
    print(f"{ColoredText.RED}❌ {message}{ColoredText.END}")

def print_info(message):
    """Affiche une info"""
    print(f"{ColoredText.CYAN}ℹ️  {message}{ColoredText.END}")

def check_dependencies():
    """Vérifie les dépendances"""
    print_step(1, 7, "Vérification des dépendances...")
    
    missing = []
    
    try:
        import PIL
        print_success("Pillow installé")
    except ImportError:
        missing.append("Pillow")
        print_warning("Pillow manquant")
    
    try:
        import aiohttp
        print_success("aiohttp installé")
    except ImportError:
        missing.append("aiohttp")
        print_warning("aiohttp manquant")
    
    try:
        import discord
        print_success("discord.py installé")
    except ImportError:
        missing.append("discord.py")
        print_error("discord.py manquant (CRITIQUE)")
    
    if missing:
        print_info(f"\nInstallez les dépendances manquantes avec :")
        print(f"pip install {' '.join(missing)}")
        
        response = input("\nVoulez-vous que je les installe automatiquement ? (o/n) : ")
        if response.lower() in ['o', 'oui', 'y', 'yes']:
            import subprocess
            for package in missing:
                print(f"\n📦 Installation de {package}...")
                subprocess.check_call(['pip', 'install', package])
            print_success("Toutes les dépendances ont été installées !")
        else:
            print_error("Installation annulée. Installez les dépendances manuellement.")
            return False
    
    print()
    return True

def backup_files():
    """Sauvegarde les fichiers existants"""
    print_step(2, 7, "Sauvegarde des fichiers existants...")
    
    backup_dir = Path(f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    backup_dir.mkdir(exist_ok=True)
    
    files_to_backup = ['cards.py', 'card_data.json']
    backed_up = []
    
    for file in files_to_backup:
        if os.path.exists(file):
            shutil.copy2(file, backup_dir / file)
            backed_up.append(file)
            print_success(f"{file} sauvegardé")
    
    if backed_up:
        print_info(f"Sauvegarde créée dans : {backup_dir}/")
    else:
        print_warning("Aucun fichier à sauvegarder")
    
    print()
    return backup_dir

def install_visual_generator():
    """Installe le générateur visuel"""
    print_step(3, 7, "Installation du générateur visuel...")
    
    # Vérifier si card_visual_generator.py existe déjà
    if os.path.exists('card_visual_generator.py'):
        print_success("card_visual_generator.py déjà présent")
        print()
        return
    
    # Copier depuis les uploads
    source = '/mnt/user-data/uploads/card_visual_generator.py'
    if os.path.exists(source):
        shutil.copy2(source, 'card_visual_generator.py')
        print_success("card_visual_generator.py installé")
    else:
        print_error("card_visual_generator.py introuvable")
    
    print()

def install_integrated_cards():
    """Installe le nouveau système de cartes"""
    print_step(4, 7, "Installation du nouveau système de cartes...")
    
    # Vérifier si cards_integrated.py existe
    if not os.path.exists('cards_integrated.py'):
        print_error("cards_integrated.py introuvable")
        print_info("Le fichier devrait être dans le même dossier que ce script")
        print()
        return False
    
    # Remplacer cards.py
    response = input("Remplacer cards.py par la nouvelle version ? (o/n) : ")
    if response.lower() in ['o', 'oui', 'y', 'yes']:
        shutil.copy2('cards_integrated.py', 'cards.py')
        print_success("Nouveau système installé → cards.py")
    else:
        print_warning("cards.py non modifié")
    
    print()
    return True

def migrate_card_data():
    """Migre les données"""
    print_step(5, 7, "Migration des données...")
    
    if not os.path.exists('card_data.json'):
        print_warning("card_data.json introuvable")
        data = {"users": {}, "trades": {}, "daily_claims": {}}
        with open('card_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print_success("Nouveau card_data.json créé")
        print()
        return
    
    print_info("La migration se fera automatiquement au premier lancement du bot")
    print()

def update_requirements():
    """Met à jour requirements.txt"""
    print_step(6, 7, "Mise à jour de requirements.txt...")
    
    if not os.path.exists('requirements.txt'):
        print_warning("requirements.txt introuvable")
        print()
        return
    
    with open('requirements.txt', 'r') as f:
        content = f.read()
    
    new_deps = []
    if 'Pillow' not in content and 'pillow' not in content.lower():
        new_deps.append('Pillow')
    if 'aiohttp' not in content:
        new_deps.append('aiohttp')
    
    if new_deps:
        with open('requirements.txt', 'a') as f:
            f.write('\n# Système visuel de cartes\n')
            for dep in new_deps:
                f.write(f'{dep}\n')
        print_success(f"Ajouté : {', '.join(new_deps)}")
    else:
        print_info("requirements.txt déjà à jour")
    
    print()

def create_demo():
    """Installe le script de démo"""
    print_step(7, 7, "Installation du script de démonstration...")
    
    source = '/mnt/user-data/uploads/demo_card_generator.py'
    if os.path.exists(source):
        shutil.copy2(source, 'demo_card_generator.py')
        print_success("demo_card_generator.py installé")
    else:
        print_warning("demo_card_generator.py introuvable (optionnel)")
    
    print()

def display_next_steps():
    """Affiche les prochaines étapes"""
    print("\n" + "="*70)
    print(ColoredText.BOLD + ColoredText.GREEN + 
          "🎉 INSTALLATION TERMINÉE ! 🎉" + 
          ColoredText.END)
    print("="*70 + "\n")
    
    print(ColoredText.BOLD + "📋 PROCHAINES ÉTAPES :\n" + ColoredText.END)
    
    print(f"{ColoredText.CYAN}1️⃣ Lancez votre bot{ColoredText.END}")
    print(f"   → {ColoredText.YELLOW}python main.py{ColoredText.END}\n")
    
    print(f"{ColoredText.CYAN}2️⃣ Testez dans Discord{ColoredText.END}")
    print(f"   → {ColoredText.YELLOW}a!card_help{ColoredText.END}\n")
    
    print(f"{ColoredText.CYAN}3️⃣ Ouvrez un pack{ColoredText.END}")
    print(f"   → {ColoredText.YELLOW}a!open_pack or{ColoredText.END}\n")
    
    print(f"{ColoredText.CYAN}4️⃣ Générez une carte visuelle{ColoredText.END}")
    print(f"   → {ColoredText.YELLOW}a!card_visual <id>{ColoredText.END}\n")
    
    print(f"{ColoredText.CYAN}5️⃣ Affichez votre galerie{ColoredText.END}")
    print(f"   → {ColoredText.YELLOW}a!gallery{ColoredText.END}\n")
    
    print(ColoredText.BOLD + "💡 IMPORTANT :\n" + ColoredText.END)
    print("  • Vos données ont été préservées")
    print("  • La migration se fait automatiquement au lancement")
    print("  • Le mode visuel s'active si card_visual_generator.py est présent")
    print("  • Pour ajouter des images : uploadez sur Imgur et ajoutez les URLs\n")

def main():
    """Fonction principale"""
    print_header()
    
    # Étape 1 : Vérifier les dépendances
    if not check_dependencies():
        return
    
    # Étape 2 : Sauvegarder
    backup_dir = backup_files()
    
    # Étape 3 : Installer le générateur
    install_visual_generator()
    
    # Étape 4 : Installer le nouveau système
    if not install_integrated_cards():
        return
    
    # Étape 5 : Migrer les données
    migrate_card_data()
    
    # Étape 6 : Mettre à jour requirements
    update_requirements()
    
    # Étape 7 : Créer le script de démo
    create_demo()
    
    # Afficher les prochaines étapes
    display_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{ColoredText.YELLOW}Installation annulée par l'utilisateur{ColoredText.END}")
    except Exception as e:
        print(f"\n\n{ColoredText.RED}❌ Erreur : {str(e)}{ColoredText.END}")
