# save_manager.py
# Gestion simple de sauvegarde JSON pour le système de cartes.
# Utilise un seul fichier JSON pour stocker : users, cards, trades, packs (persistant sur disque).

import json
import os
import threading
from typing import Dict, Any

LOCK = threading.Lock()
DATA_PATH = os.getenv("CARDS_DATA_PATH", "/mnt/data/cards_data.json")

DEFAULT_DATA = {
    "users": {},      # user_id -> {"credits": int, "cards": {card_id: count}, "trades": []}
    "cards": {},      # card_id -> {metadata}
    "trades": {},     # trade_id -> {from, to, offered_cards, requested_credits, status}
    "next_trade_id": 1,
    "packs": {}       # pack definitions (optional)
}

def _ensure_file():
    if not os.path.exists(DATA_PATH):
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_DATA, f, ensure_ascii=False, indent=2)

def load_data() -> Dict[str, Any]:
    _ensure_file()
    with LOCK:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

def save_data(data: Dict[str, Any]):
    with LOCK:
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

# Utility helpers

def get_user(user_id: str) -> Dict[str, Any]:
    data = load_data()
    if user_id not in data["users"]:
        data["users"][user_id] = {"credits": 0, "cards": {}}
        save_data(data)
    return data["users"][user_id]

def add_credits(user_id: str, amount: int):
    if amount == 0:
        return
    data = load_data()
    user = data["users"].setdefault(user_id, {"credits": 0, "cards": {}})
    user["credits"] = user.get("credits", 0) + int(amount)
    save_data(data)

def set_credits(user_id: str, amount: int):
    data = load_data()
    user = data["users"].setdefault(user_id, {"credits": 0, "cards": {}})
    user["credits"] = int(amount)
    save_data(data)

def get_credits(user_id: str) -> int:
    data = load_data()
    return int(data["users"].get(user_id, {}).get("credits", 0))

def register_card(card_id: str, metadata: Dict[str, Any]):
    data = load_data()
    data["cards"].setdefault(card_id, metadata)
    save_data(data)

def give_card_to_user(user_id: str, card_id: str, amount: int = 1):
    data = load_data()
    user = data["users"].setdefault(user_id, {"credits": 0, "cards": {}})
    user_cards = user.setdefault("cards", {})
    user_cards[card_id] = user_cards.get(card_id, 0) + int(amount)
    save_data(data)

def remove_card_from_user(user_id: str, card_id: str, amount: int = 1) -> bool:
    data = load_data()
    user = data["users"].get(user_id)
    if not user:
        return False
    user_cards = user.get("cards", {})
    have = user_cards.get(card_id, 0)
    if have < amount:
        return False
    if have == amount:
        user_cards.pop(card_id, None)
    else:
        user_cards[card_id] = have - amount
    save_data(data)
    return True

def get_user_collection(user_id: str) -> Dict[str, int]:
    data = load_data()
    return dict(data["users"].get(user_id, {}).get("cards", {}))

def get_all_cards() -> Dict[str, Any]:
    data = load_data()
    return dict(data.get("cards", {}))

def get_card(card_id: str) -> Dict[str, Any]:
    data = load_data()
    return data.get("cards", {}).get(card_id)

def list_user_cards_pretty(user_id: str) -> Dict[str, Any]:
    data = load_data()
    user = data["users"].get(user_id, {"cards": {}})
    cards = data.get("cards", {})
    result = []
    for cid, count in user.get("cards", {}).items():
        meta = cards.get(cid, {})
        result.append({"card_id": cid, "count": count, "meta": meta})
    return result

# Trade helpers
def create_trade(from_user: str, to_user: str, offered: Dict[str,int], requested_credits: int) -> int:
    data = load_data()
    tid = data.get("next_trade_id", 1)
    data["trades"][str(tid)] = {
        "from": from_user,
        "to": to_user,
        "offered": offered,
        "requested_credits": int(requested_credits),
        "status": "open"
    }
    data["next_trade_id"] = int(tid) + 1
    save_data(data)
    return int(tid)

def get_trade(trade_id: int) -> Dict[str,Any]:
    data = load_data()
    return data.get("trades", {}).get(str(trade_id))

def set_trade_status(trade_id: int, status: str):
    data = load_data()
    trade = data.get("trades", {}).get(str(trade_id))
    if trade:
        trade["status"] = status
        save_data(data)
        return True
    return False

def accept_trade(trade_id: int) -> bool:
    data = load_data()
    trade = data.get("trades", {}).get(str(trade_id))
    if not trade or trade.get("status") != "open":
        return False

    from_u = trade["from"]
    to_u = trade["to"]
    offered = trade["offered"]
    requested_credits = int(trade["requested_credits"])

    # Check to_user has enough credits
    to_user = data["users"].get(to_u, {"credits":0, "cards":{}})
    if to_user.get("credits",0) < requested_credits:
        return False

    # Check from_user has the offered cards
    from_user = data["users"].get(from_u, {"credits":0, "cards":{}})
    for cid, amt in offered.items():
        if from_user.get("cards", {}).get(cid, 0) < amt:
            return False

    # Perform the exchange
    # Remove cards from from_user and add them to to_user
    for cid, amt in offered.items():
        from_user["cards"][cid] = from_user["cards"].get(cid,0) - amt
        if from_user["cards"][cid] <= 0:
            del from_user["cards"][cid]
        to_user["cards"][cid] = to_user["cards"].get(cid,0) + amt

    # Exchange credits (to_user pays requested_credits to from_user)
    to_user["credits"] = to_user.get("credits",0) - requested_credits
    from_user["credits"] = from_user.get("credits",0) + requested_credits

    trade["status"] = "accepted"
    save_data(data)
    return True
