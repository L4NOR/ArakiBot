# 📚 Exemples d'Utilisation - Système de Cartes Catenaccio

## 🎮 Scénarios d'Utilisation Courants

### Scénario 1 : Nouveau Joueur

**Pierre rejoint le serveur et découvre le système de cartes**

```
Étape 1 : Découvrir le système
Pierre: a!card_help

Bot: [Affiche le guide complet avec toutes les commandes]

Étape 2 : Vérifier son solde initial
Pierre: a!balance

Bot: 💰 Vos Crédits Catenaccio
     500 CC
     
     📊 Statistiques
     Packs ouverts: 0
     Cartes collectées: 0
     Échanges effectués: 0

Étape 3 : Consulter la boutique
Pierre: a!shop

Bot: 🛒 Boutique de Packs
     📦 Pack Basique - 100 CC - 3 cartes
     📦 Pack Argent - 250 CC - 5 cartes
     📦 Pack Or - 500 CC - 7 cartes
     📦 Pack Platine - 1000 CC - 10 cartes

Étape 4 : Ouvrir son premier pack
Pierre: a!open_pack basique

Bot: 📦 Pack Basique ouvert !
     
     ⚪ Défenseur Latéral
     🛡️ Défense | Commune
     
     ⚪ Milieu Défensif
     🛡️ Défense | Commune
     
     🔵 Buteur Clinique
     ⚡ Attaque | Rare
     
     Crédits restants: 400 CC
```

---

### Scénario 2 : Collectionneur Régulier

**Marie joue quotidiennement et optimise ses ressources**

```
Jour 1 - Matin
Marie: a!daily

Bot: 🎁 Récompense Quotidienne
     Vous avez reçu 100 Crédits Catenaccio (CC) !
     Revenez demain pour votre prochaine récompense !

Marie: a!balance

Bot: 💰 Vos Crédits Catenaccio
     850 CC (avait 750 + 100)

Marie: a!open_pack argent

Bot: 📦 Pack Argent ouvert ! [5 cartes affichées]
     Crédits restants: 600 CC

---

Jour 3
Marie: a!balance

Bot: 💰 Vos Crédits Catenaccio
     1050 CC
     
     📊 Statistiques
     Packs ouverts: 7
     Cartes collectées: 38
     Échanges effectués: 2

Marie: a!open_pack or

Bot: 📦 Pack Or ouvert !
     
     ⚪ Meneur de Jeu - Technique | Commune
     ⚪ Ailier Rapide - Vitesse | Commune
     🔵 Capitaine Défensif - Défense | Rare
     🟣 Araki - Défenseur Prodige - Défense | Épique  🎉
     ⚪ Joueur Polyvalent - Physique | Commune
     🔵 Sprinter Ailier - Vitesse | Rare
     ⚪ Attaquant de Pointe - Attaque | Commune
     
     Crédits restants: 550 CC
```

---

### Scénario 3 : Échange Simple entre Joueurs

**Thomas veut échanger avec Sophie**

```
Thomas veut donner sa carte "Gardien Légendaire" à Sophie

Étape 1 : Thomas consulte sa collection
Thomas: a!collection

Bot: 📚 Collection de Thomas
     Total: 42 cartes
     
     🆕 Cartes récentes
     1. 🧤 Gardien Légendaire (Épique)
     2. 🛡️ Défenseur Latéral (Commune)
     3. ⚡ Buteur Clinique (Rare)
     [...]

Étape 2 : Thomas propose l'échange (carte #1)
Thomas: a!trade @Sophie 1

Bot: 💱 Proposition d'Échange
     Thomas vous propose un échange !
     
     📇 Carte proposée
     🧤 Gardien Légendaire
     Défense | Épique
     
     ✅ Pour accepter
     Utilisez a!accept_trade 123456789
     
     ❌ Pour refuser
     Utilisez a!decline_trade 123456789

Étape 3 : Sophie accepte
Sophie: a!accept_trade 123456789

Bot: ✅ Échange Réussi !
     L'échange entre Thomas et Sophie a été complété !
     
     📇 Carte échangée
     🧤 Gardien Légendaire
     Défense | Épique
```

---

### Scénario 4 : Échange avec Crédits

**Lucas veut obtenir une carte rare de Emma et offre des crédits**

```
Lucas veut la carte "Araki - Catenaccio Ultime" de Emma

Étape 1 : Lucas vérifie la collection d'Emma
Lucas: a!collection @Emma

Bot: 📚 Collection de Emma
     Total: 65 cartes
     
     🆕 Cartes récentes
     1. 🛡️ Araki - Catenaccio Ultime (Légendaire)  ⭐
     2. 🎯 Maestro du Milieu (Épique)
     [...]

Étape 2 : Lucas vérifie ses crédits
Lucas: a!balance

Bot: 💰 Vos Crédits Catenaccio
     1500 CC

Étape 3 : Lucas propose carte + crédits
Lucas: a!trade @Emma 5 500

Bot: [Message d'échange envoyé à Emma]
     
     💱 Proposition d'Échange
     Lucas vous propose un échange !
     
     📇 Carte proposée
     🎯 Dribbleur Technique
     Technique | Rare
     
     💰 Crédits offerts
     500 CC
     
     ✅ Pour accepter : a!accept_trade 987654321
     ❌ Pour refuser : a!decline_trade 987654321

Étape 4 : Emma refuse
Emma: a!decline_trade 987654321

Bot: ✅ Vous avez refusé la proposition d'échange.

[Lucas reçoit un message privé]
Bot: ❌ Emma a refusé votre proposition d'échange.

Étape 5 : Lucas fait une meilleure offre
Lucas: a!trade @Emma 5 1000

Emma: a!accept_trade 987654321

Bot: ✅ Échange Réussi !
     
     📇 Carte échangée : Dribbleur Technique
     💰 Crédits transférés : 1000 CC
```

---

### Scénario 5 : Administrateur Gérant le Système

**Admin donne des récompenses événementielles**

```
Événement Spécial : Nouveau chapitre sorti !

Admin: a!give_credits @Marie 500

Bot: ✅ 500 CC ont été donnés à Marie.

---

Cas problème : Un joueur a perdu sa collection par erreur

Joueur: J'ai accidentellement supprimé mes données !

Admin: a!reset_collection @Joueur

Bot: ✅ La collection de Joueur a été réinitialisée.

Admin: a!give_credits @Joueur 2000

Bot: ✅ 2000 CC ont été donnés à Joueur.
     (Pour compenser la perte)
```

---

### Scénario 6 : Joueur Expérimenté avec Stratégie

**Karim optimise ses ressources pour obtenir des cartes légendaires**

```
Jour 1-7 : Accumulation
Karim: a!daily (chaque jour)
Karim: [Évite d'ouvrir des packs basiques]

Bot: +100 CC par jour = 700 CC en une semaine

Jour 8 : 
Karim: a!balance

Bot: 💰 Vos Crédits Catenaccio
     2200 CC (solde initial + 7 jours + quelques échanges)

Karim: a!open_pack platine

Bot: 📦 Pack Platine ouvert !
     [10 cartes dont probablement 1-2 épiques ou mieux]

Karim: a!open_pack platine

Bot: 📦 Pack Platine ouvert !
     
     ⚪ x5 Cartes Communes
     🔵 x3 Cartes Rares
     🟣 x1 Maestro du Milieu (Épique)
     🟠 x1 Araki - Catenaccio Ultime (Légendaire) 🎉🎉🎉
     
     Crédits restants: 200 CC

Karim: Excellent ! J'ai ma légendaire !
```

---

### Scénario 7 : Gestion d'Échanges Multiples

**Sarah gère plusieurs propositions d'échange**

```
Sarah reçoit 3 propositions d'échange

Message 1:
Bot: Pierre vous propose un échange
     Carte: Buteur Clinique (Rare) + 100 CC
     a!accept_trade 111111111

Message 2:
Bot: Marc vous propose un échange
     Carte: Gardien Expérimenté (Rare)
     a!accept_trade 222222222

Message 3:
Bot: Julie vous propose un échange
     Carte: Sprinter Ailier (Rare) + 200 CC
     a!accept_trade 333333333

Sarah analyse:
Sarah: a!collection
[Vérifie quelles cartes elle a déjà]

Sarah: a!accept_trade 333333333
Bot: ✅ Échange complété avec Julie !

Sarah: a!decline_trade 111111111
Bot: ✅ Vous avez refusé la proposition de Pierre.

[2ème échange expire après 5 min]
Sarah: a!accept_trade 222222222
Bot: ❌ Cette proposition d'échange a expiré.
```

---

### Scénario 8 : Collection Complète d'une Rareté

**Antoine vise à collectionner toutes les cartes Épiques**

```
Antoine: a!collection

Bot: 📚 Collection de Antoine
     Total: 89 cartes
     
     Épique: 4 cartes
     
     🆕 Cartes récentes
     🟣 Araki - Défenseur Prodige (Épique)
     🟣 Mur Infranchissable (Épique)
     🟣 Attaquant d'Élite (Épique)
     🟣 Maestro du Milieu (Épique)

Antoine vérifie la liste complète des cartes Épiques:
- ✅ Araki - Défenseur Prodige
- ✅ Mur Infranchissable
- ❌ Gardien Légendaire
- ✅ Attaquant d'Élite
- ✅ Maestro du Milieu
- ❌ Éclair sur l'Aile

Antoine recherche la carte manquante:
Antoine: @Communauté Quelqu'un a "Gardien Légendaire" (Épique) à échanger ?

Marc: Oui moi ! Qu'est-ce que tu proposes ?

Antoine: a!trade @Marc 12 300
[Carte Rare + 300 CC]

Marc: a!accept_trade 444444444

Bot: ✅ Échange complété !

Antoine: Génial ! Plus qu'une carte Épique à trouver !
```

---

## 💡 Conseils et Astuces

### Pour Débutants
1. Réclamez votre récompense quotidienne TOUS les jours
2. Commencez par des packs basiques pour construire votre collection
3. Ne dépensez pas tous vos crédits d'un coup

### Pour Intermédiaires
1. Économisez pour les packs Platine (meilleur ratio prix/cartes)
2. Échangez vos doublons contre des crédits
3. Suivez les collections des autres pour identifier les opportunités d'échange

### Pour Experts
1. Planifiez vos achats sur plusieurs jours
2. Créez un réseau d'échange avec d'autres collectionneurs
3. Attendez les événements spéciaux pour maximiser vos gains

---

**Ces exemples illustrent toutes les fonctionnalités du système ! Bon jeu ! 🎴⚽**