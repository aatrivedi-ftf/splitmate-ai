import json
import random
import os

def recommend_friends(user_id):
    file_path = os.path.join(os.path.dirname(__file__), "../data/mock_users.json")
    with open(file_path, "r") as f:
        users = json.load(f)

    others = [u for u in users if u["user_id"] != user_id]
    return random.sample(others, 2)  # recommend 2 others
