# 🎴 Système de Collection de Cartes Catenaccio

## 📋 Vue d'ensemble

Le système de cartes permet aux membres du serveur Discord de collecter des cartes de joueurs virtuelles inspirées du manga Catenaccio, de les échanger avec d'autres joueurs, et de constituer leur collection ultime.

## 💰 Système de Crédits

### Crédits Catenaccio (CC)
- Monnaie virtuelle utilisée pour acheter des packs de cartes
- Chaque nouveau joueur commence avec **500 CC**
- Récompense quotidienne de **100 CC** disponible toutes les 24h

### Obtenir des Crédits
- `a!daily` - Récompense quotidienne (100 CC)
- Échanges avec d'autres joueurs
- Récompenses d'événements (à venir)

## 📦 Types de Packs

| Pack | Prix | Nombre de cartes |
|------|------|------------------|
| 💼 Pack Basique | 100 CC | 3 cartes |
| 💎 Pack Argent | 250 CC | 5 cartes |
| 🥇 Pack Or | 500 CC | 7 cartes |
| 👑 Pack Platine | 1000 CC | 10 cartes |

## 🎴 Rarités des Cartes

### Taux de Drop
- ⚪ **Commune** - 70% de chance
- 🔵 **Rare** - 20% de chance
- 🟣 **Épique** - 8% de chance
- 🟠 **Légendaire** - 2% de chance
- 🔴 **Mythique** - 0.5% de chance (ultra rare !)

### Types de Cartes
- 🛡️ **Défense** - Spécialistes du Catenaccio
- 🧤 **Gardien** - Derniers remparts
- ⚡ **Attaque** - Buteurs redoutables
- 💨 **Vitesse** - Ailiers rapides
- 🎯 **Technique** - Maestros du ballon
- 💪 **Physique** - Forces de la nature
- 👑 **Mythique** - Légendes absolues

## 🎮 Commandes Disponibles

### Commandes de Base
```
a!daily                    - Réclamez votre récompense quotidienne (100 CC)
a!balance                  - Affichez votre solde et statistiques
a!shop                     - Consultez la boutique de packs
a!card_help                - Affiche ce guide complet
```

### Gestion de Collection
```
a!open_pack <type>         - Ouvrez un pack (basique/argent/or/platine)
a!collection               - Affichez votre collection
a!collection @utilisateur  - Consultez la collection d'un autre joueur
```

### Système d'Échange
```
a!trade @utilisateur <n°carte> [crédits]  - Proposez un échange
a!accept_trade <id_user>                  - Acceptez une proposition
a!decline_trade <id_user>                 - Refusez une proposition
```

### Commandes Admin
```
a!give_credits @user <montant>   - Donnez des crédits à un utilisateur
a!reset_collection @user         - Réinitialisez la collection d'un joueur
```

## 💱 Système d'Échange

### Comment Échanger
1. **Proposer un échange** : Utilisez `a!trade @utilisateur <numéro> [crédits]`
   - Indiquez le numéro de la carte dans votre collection
   - Optionnel : ajoutez des crédits à votre offre
   
2. **Accepter/Refuser** : Le destinataire utilise :
   - `a!accept_trade <votre_id>` pour accepter
   - `a!decline_trade <votre_id>` pour refuser

3. **Expiration** : Les offres expirent après 5 minutes

### Exemples d'Échange
```bash
# Échanger la carte #5 avec un joueur
a!trade @JohnDoe 5

# Échanger la carte #3 + 200 CC
a!trade @JaneDoe 3 200

# Accepter l'échange de l'utilisateur avec l'ID 123456789
a!accept_trade 123456789
```

## 📊 Statistiques Suivies

Pour chaque joueur :
- 📦 Nombre de packs ouverts
- 🎴 Nombre total de cartes collectées
- 💱 Nombre d'échanges complétés
- 💰 Crédits Catenaccio actuels

## 🗄️ Stockage des Données

### Fichier : `card_data.json`
Toutes les collections et données des joueurs sont sauvegardées automatiquement dans ce fichier JSON.

### Structure des Données
```json
{
  "user_id": {
    "credits": 500,
    "collection": [
      {
        "id": "unique_id",
        "name": "Nom de la carte",
        "type": "Type",
        "rarity": "Rareté",
        "emoji": "🎴"
      }
    ],
    "daily_claimed": "timestamp",
    "stats": {
      "packs_opened": 0,
      "cards_collected": 0,
      "trades_completed": 0
    }
  }
}
```

## 🎯 Stratégies de Collection

### Pour Débutants
1. Réclamez votre récompense quotidienne chaque jour
2. Commencez avec des packs basiques pour construire votre collection
3. Échangez vos doublons avec d'autres joueurs

### Pour Collectionneurs Avancés
1. Économisez pour les packs Platine (meilleur ratio)
2. Identifiez les cartes rares recherchées par la communauté
3. Utilisez les échanges stratégiques pour compléter votre collection

## ⚙️ Installation

### Fichiers Requis
- `card_system.py` - Système principal de cartes
- `card_data.json` - Fichier de sauvegarde (créé automatiquement)

### Intégration dans main.py
```python
from card_system import setup_card_commands

# Dans la fonction main()
setup_card_commands(bot)
```

## 🔒 Sécurité et Règles

- ✅ Les échanges nécessitent l'accord des deux parties
- ✅ Les données sont sauvegardées automatiquement après chaque action
- ✅ Les offres d'échange expirent après 5 minutes
- ✅ Les administrateurs peuvent gérer les collections en cas de problème
- ❌ Impossible d'échanger avec soi-même ou des bots
- ❌ Les échanges ne peuvent pas être annulés une fois acceptés

## 🐛 Dépannage

### Problèmes Courants

**"Crédits insuffisants"**
- Attendez votre récompense quotidienne
- Échangez des cartes contre des crédits

**"Aucune proposition d'échange trouvée"**
- Vérifiez l'ID de l'utilisateur
- L'offre a peut-être expiré (5 min)

**"Index de carte invalide"**
- Utilisez `a!collection` pour voir vos cartes
- Les index commencent à 1

## 🎉 Événements Futurs

Fonctionnalités prévues :
- 🎁 Packs événementiels gratuits
- 🏆 Classements de collectionneurs
- ⭐ Cartes exclusives saisonnières
- 🎲 Mini-jeux pour gagner des crédits
- 📈 Marché d'échange automatique

## 📞 Support

Pour toute question ou problème :
- Contactez les administrateurs du serveur
- Utilisez `a!card_help` pour revoir les commandes
- Consultez ce README pour les détails

---

**Bonne collection ! ⚽🎴**