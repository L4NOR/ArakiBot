import json
import os
import random
from discord import Embed

SAVE_FILE = "card_saves.json"


# ---------------------------------------------------------
# ------------ 1. Gestion du fichier de sauvegarde --------
# ---------------------------------------------------------

def load_data():
    if not os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump({"players": {}, "cards": {}}, f, indent=4)
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# ---------------------------------------------------------
# ------------ 2. Base des cartes -------------------------
# ---------------------------------------------------------

RARITY_TABLE = {
    "Commune": 70,
    "Rare": 20,
    "Épique": 8,
    "Légendaire": 2,
    "Mythique": 0.5
}

CARD_STATS = ["Défense", "Vitesse", "Précision", "Physique", "Tactique", "Technique"]


def generate_card():
    rarity = random.choices(list(RARITY_TABLE.keys()), weights=RARITY_TABLE.values())[0]

    card_id = str(random.randint(1000000, 9999999))
    stat_name = random.choice(CARD_STATS)
    stat_value = random.randint(20, 100)

    new_card = {
        "id": card_id,
        "rarity": rarity,
        "stat": stat_name,
        "value": stat_value
    }

    return new_card


# ---------------------------------------------------------
# ------------ 3. Packs -----------------------------------
# ---------------------------------------------------------

PACKS = {
    "bronze": {"price": 100, "cards": 3},
    "argent": {"price": 250, "cards": 5, "min_rarity": "Rare"},
    "or": {"price": 500, "cards": 7, "min_rarity": "Rare"},
    "platine": {"price": 1000, "cards": 10, "min_rarity": "Légendaire"},
}


def open_pack(player_id, pack_name):
    data = load_data()

    if player_id not in data["players"]:
        return False, "Tu n’as pas de compte ! Fais **a!start**"

    if pack_name not in PACKS:
        return False, "Ce pack n'existe pas."

    pack = PACKS[pack_name]
    price = pack["price"]

    if data["players"][player_id]["credits"] < price:
        return False, "Tu n’as pas assez de crédits."

    # Retrait des crédits
    data["players"][player_id]["credits"] -= price

    obtained = []

    for _ in range(pack["cards"]):
        card = generate_card()

        # S'assurer d'une rareté minimum
        if "min_rarity" in pack:
            rar_order = list(RARITY_TABLE.keys())
            while rar_order.index(card["rarity"]) < rar_order.index(pack["min_rarity"]):
                card = generate_card()

        # Sauvegarde
        data["cards"][card["id"]] = card
        data["players"][player_id]["collection"].append(card["id"])
        obtained.append(card)

    save_data(data)

    return True, obtained


# ---------------------------------------------------------
# ------------ 4. Création de compte ----------------------
# ---------------------------------------------------------

def create_account(user_id):
    data = load_data()
    if user_id in data["players"]:
        return False

    data["players"][user_id] = {
        "credits": 200,
        "collection": []
    }
    save_data(data)
    return True


# ---------------------------------------------------------
# ------------ 5. Consultation de collection ---------------
# ---------------------------------------------------------

def get_collection(user_id):
    data = load_data()

    if user_id not in data["players"]:
        return None

    cards = []
    for cid in data["players"][user_id]["collection"]:
        if cid in data["cards"]:
            cards.append(data["cards"][cid])

    return cards


# ---------------------------------------------------------
# ------------ 6. Échanges entre joueurs -------------------
# ---------------------------------------------------------

# Système d'échange simple :
# joueur A propose → joueur B confirme → échange effectué

PENDING_TRADES = {}  # {user_id: {"target": id, "card": id, "price": int}}


def start_trade(author_id, target_id, card_id, price):
    data = load_data()

    # Vérif possession
    if author_id not in data["players"]:
        return False, "Tu n'as pas de compte."

    if card_id not in data["players"][author_id]["collection"]:
        return False, "Tu ne possèdes pas cette carte."

    PENDING_TRADES[target_id] = {
        "author": author_id,
        "card": card_id,
        "price": price
    }

    return True, None


def accept_trade(user_id):
    data = load_data()

    if user_id not in PENDING_TRADES:
        return False, "Aucune offre pour toi."

    trade = PENDING_TRADES[user_id]

    # Vérif crédits acheteur
    if data["players"][user_id]["credits"] < trade["price"]:
        return False, "Tu n’as pas assez de crédits."

    # Effectuer l'échange
    data["players"][user_id]["credits"] -= trade["price"]
    data["players"][trade["author"]]["credits"] += trade["price"]

    # Transfert de carte
    data["players"][trade["author"]]["collection"].remove(trade["card"])
    data["players"][user_id]["collection"].append(trade["card"])

    save_data(data)

    del PENDING_TRADES[user_id]

    return True, None
