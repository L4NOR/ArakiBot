# 📥 Guide d'Installation - Système de Cartes Catenaccio

## 🎯 Prérequis

Avant de commencer, assurez-vous d'avoir :
- ✅ Python 3.8 ou supérieur installé
- ✅ Discord.py 2.4.0 ou supérieur
- ✅ Votre bot Discord déjà configuré et fonctionnel
- ✅ Les fichiers de base du bot Catenaccio

## 📦 Fichiers Nécessaires

Téléchargez et placez ces fichiers dans votre dossier de bot :

```
votre_bot/
├── main.py (modifié)
├── commands.py (modifié)
├── config.py
├── events.py
├── utils.py
├── card_system.py (NOUVEAU)
├── card_config.py (NOUVEAU - optionnel)
├── card_data.json (créé automatiquement)
├── requirements.txt
└── .env
```

## 🔧 Installation Étape par Étape

### Étape 1 : Ajouter les Nouveaux Fichiers

1. **Créez `card_system.py`**
   - Copiez le contenu complet du fichier `card_system.py` fourni
   - Placez-le à la racine de votre projet

2. **Créez `card_config.py` (optionnel)**
   - Si vous voulez personnaliser facilement le système
   - Sinon, les configurations par défaut seront utilisées

### Étape 2 : Modifier main.py

Ajoutez cette ligne dans vos imports :
```python
from card_system import setup_card_commands
```

Dans la fonction `main()`, ajoutez après `setup_commands(bot)` :
```python
setup_card_commands(bot)  # Système de cartes
```

Votre `main.py` devrait ressembler à ça :
```python
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from config import BOT_TOKEN, COMMAND_PREFIX, intents
from commands import setup_commands
from events import setup
from card_system import setup_card_commands  # NOUVEAU

async def main():
    bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)
    bot.remove_command('help')
    
    setup_commands(bot)
    setup_card_commands(bot)  # NOUVEAU
    await setup(bot)
    
    async with bot:
        await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
```

### Étape 3 : Modifier commands.py (Optionnel)

Pour ajouter la référence au système de cartes dans la commande d'aide :

Dans la commande `a!Araki`, ajoutez ce champ :
```python
embed.add_field(
    name="🎴 Système de Cartes",
    value=(
        "Utilisez `a!card_help` pour découvrir le système de collection de cartes !\n"
        "Collectionnez, échangez et devenez le meilleur collectionneur !"
    ),
    inline=False
)
```

### Étape 4 : Vérifier les Dépendances

Assurez-vous que votre `requirements.txt` contient :
```
discord.py==2.4.0
python-dotenv==1.0.1
aiohttp==3.11.11
```

Installez les dépendances :
```bash
pip install -r requirements.txt
```

### Étape 5 : Premier Lancement

1. **Lancez votre bot** :
```bash
python main.py
```

2. **Vérifiez les logs** :
   - Le bot devrait démarrer sans erreur
   - Le fichier `card_data.json` sera créé automatiquement

3. **Testez les commandes** :
```
a!card_help      # Affiche l'aide du système
a!daily          # Réclamez votre première récompense
a!shop           # Consultez la boutique
a!balance        # Vérifiez votre solde
```

## ✅ Vérification de l'Installation

### Test Rapide

Exécutez ces commandes dans Discord pour vérifier que tout fonctionne :

1. **Test de base** :
```
a!card_help
```
Vous devriez voir un embed avec toutes les commandes disponibles.

2. **Test des crédits** :
```
a!daily
a!balance
```
Vous devriez recevoir 100 CC et voir votre solde.

3. **Test d'achat** :
```
a!shop
a!open_pack basique
```
Vous devriez pouvoir ouvrir un pack et recevoir 3 cartes.

4. **Test de collection** :
```
a!collection
```
Vous devriez voir vos cartes nouvellement obtenues.

### Checklist de Vérification

- [ ] Le bot démarre sans erreur
- [ ] `card_data.json` est créé dans le dossier du bot
- [ ] La commande `a!card_help` fonctionne
- [ ] La commande `a!daily` donne 100 CC
- [ ] La commande `a!open_pack basique` ouvre un pack
- [ ] La commande `a!collection` affiche les cartes
- [ ] Les embeds s'affichent correctement

## 🐛 Résolution de Problèmes

### Erreur : "Module card_system not found"
**Solution** : Vérifiez que `card_system.py` est bien dans le même dossier que `main.py`

### Erreur : "Permission denied" sur card_data.json
**Solution** : Vérifiez les permissions d'écriture dans le dossier du bot
```bash
chmod 755 votre_dossier_bot/
```

### Les commandes ne fonctionnent pas
**Solution** : 
1. Vérifiez que le préfixe est bien `a!` dans `config.py`
2. Assurez-vous que le bot a les intents nécessaires :
```python
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
```

### Le fichier JSON n'est pas créé
**Solution** :
1. Créez-le manuellement avec le contenu :
```json
{}
```
2. Vérifiez les permissions d'écriture du dossier

### Les embeds ne s'affichent pas correctement
**Solution** : Vérifiez que votre bot a la permission "Embed Links" sur le serveur Discord

## 🎨 Personnalisation

### Modifier les Prix des Packs

Dans `card_system.py`, trouvez `PACK_PRICES` et modifiez :
```python
PACK_PRICES = {
    "basique": {"price": 100, "cards": 3, "name": "Pack Basique"},
    # Modifiez les valeurs selon vos besoins
}
```

### Ajouter de Nouvelles Cartes

Dans `CARD_DATABASE`, ajoutez vos cartes :
```python
"Commune": {
    "drop_rate": 0.70,
    "cards": [
        {"name": "Votre Carte", "type": "Type", "rarity": "Commune", "emoji": "🎴"},
        # Ajoutez autant de cartes que vous voulez
    ]
}
```

### Modifier les Taux de Drop

Ajustez les pourcentages dans `CARD_DATABASE` :
```python
"Commune": {"drop_rate": 0.70},    # 70%
"Rare": {"drop_rate": 0.20},       # 20%
"Épique": {"drop_rate": 0.08},     # 8%
"Légendaire": {"drop_rate": 0.02}, # 2%
"Mythique": {"drop_rate": 0.005}   # 0.5%
```
⚠️ **Important** : Le total doit faire 1.0 (100%)

## 🔄 Mise à Jour

Pour mettre à jour le système :

1. **Sauvegardez** votre `card_data.json` actuel
2. Remplacez `card_system.py` par la nouvelle version
3. Relancez le bot
4. Vos données seront préservées

## 💾 Sauvegarde des Données

### Sauvegarde Automatique
Les données sont sauvegardées automatiquement après chaque action.

### Sauvegarde Manuelle
Copiez régulièrement `card_data.json` :
```bash
cp card_data.json card_data_backup_$(date +%Y%m%d).json
```

### Restauration
Pour restaurer une sauvegarde :
```bash
cp card_data_backup_20241124.json card_data.json
```

## 📊 Monitoring

### Vérifier l'État du Système

Créez un script de monitoring :
```python
import json

with open('card_data.json', 'r') as f:
    data = json.load(f)
    
print(f"Nombre de joueurs : {len(data)}")
print(f"Total de cartes : {sum(len(user['collection']) for user in data.values())}")
```

## 🚀 Optimisation

### Pour les Grands Serveurs

Si vous avez plus de 1000 utilisateurs :

1. **Utilisez une base de données** : Envisagez SQLite ou PostgreSQL
2. **Ajoutez un cache** : Pour réduire les lectures/écritures
3. **Limitez les collections** : Définissez une taille max par joueur

## 📞 Support

Si vous rencontrez des problèmes :

1. Vérifiez les logs du bot
2. Consultez le README_CARD_SYSTEM.md
3. Vérifiez que toutes les dépendances sont installées
4. Assurez-vous que les permissions Discord sont correctes

## ✨ Fonctionnalités Futures

Le système est conçu pour être extensible. Futures améliorations :
- [ ] Base de données SQL pour meilleures performances
- [ ] Interface web pour gérer les collections
- [ ] API REST pour applications tierces
- [ ] Système de quêtes et achievements
- [ ] Marché automatique d'échange

---

**Installation terminée ! Bon jeu ! 🎴⚽**