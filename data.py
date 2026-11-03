import json
import os
from filelock import FileLock
from datetime import datetime

DATA_FILE = "restaurants.json"
LOCK_FILE = "restaurants.json.lock"

def _get_lock():
    return FileLock(LOCK_FILE, timeout=10)

def _load_data():
    if not os.path.exists(DATA_FILE):
        return {"restaurants": [], "reviews": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_restaurants():
    with _get_lock():
        return _load_data()["restaurants"]

def add_restaurant(name, address=""):
    with _get_lock():
        data = _load_data()
        new_id = max([r["id"] for r in data["restaurants"]], default=0) + 1
        data["restaurants"].append({"id": new_id, "name": name, "address": address})
        _save_data(data)

def delete_restaurant(restaurant_id):
    with _get_lock():
        data = _load_data()
        data["restaurants"] = [r for r in data["restaurants"] if r["id"] != restaurant_id]
        data["reviews"] = [r for r in data["reviews"] if r["restaurant_id"] != restaurant_id]
        _save_data(data)

def add_review(restaurant_id, rating, user_name="Anonymous"):
    with _get_lock():
        data = _load_data()
        data["reviews"].append({
            "restaurant_id": restaurant_id,
            "rating": rating,
            "user": user_name,
            "timestamp": datetime.now().isoformat()
        })
        _save_data(data)

def get_rankings():
    with _get_lock():
        data = _load_data()
    
    rankings = []
    for restaurant in data["restaurants"]:
        reviews = [r for r in data["reviews"] if r["restaurant_id"] == restaurant["id"]]
        avg_rating = sum(r["rating"] for r in reviews) / len(reviews) if reviews else 0
        rankings.append({
            "id": restaurant["id"],
            "name": restaurant["name"],
            "address": restaurant["address"],
            "avg_rating": round(avg_rating, 2),
            "review_count": len(reviews)
        })
    
    return sorted(rankings, key=lambda x: (-x["avg_rating"], -x["review_count"]))
