import random
import string
import threading
import json
import os

DB_FILE = "database.json"
db_lock = threading.Lock()

def load_db():
    if not os.path.exists(DB_FILE):
        return {"rooms": {}}
    with open(DB_FILE, "r") as file:
        return json.load(file)

def save_db(data):
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)

def list_rooms():
    db = load_db()
    return db["rooms"], 200

def create_room(name, avatar_id):
    with db_lock:
        db = load_db()
        
        characters = string.ascii_uppercase + string.digits
        room_id = ''.join(random.choices(characters, k=4))
        while room_id in db["rooms"]:
            room_id = ''.join(random.choices(characters, k=4))
            
        user_id = str(random.randint(1, 10000))
        
        new_room = {
            'id': room_id,
            'port': None,
            'admin_id': user_id,
            'state': 'WAITING', 
            'users': [{
                'id': user_id,
                'name': name,
                'is_host': True,
                'avatar_id': avatar_id
            }],
            'game': None
        }
        
        db["rooms"][room_id] = new_room
        save_db(db)
        
        return {'room_id': room_id, 'user_id': user_id, 'message': 'Room created successfully'}, 201

def join_room(room_id, name, avatar_id):
    with db_lock:
        db = load_db()
        
        if room_id not in db["rooms"]:
            return {'error': 'Room not found'}, 404
        
        room = db["rooms"][room_id]
        
        if room["state"] != 'WAITING':
            return {'error': 'The race has already started or the room is closed'}, 400

        if len(room["users"]) >= 5:
            return {'error': 'The room is full. The limit is 5 players.'}, 403
            
        existing_ids = [u["id"] for u in room["users"]]
        
        user_id = str(random.randint(1, 10000))
        while user_id in existing_ids:
            user_id = str(random.randint(1, 10000))
        
        new_user = {
            'id': user_id,
            'name': name,
            'is_host': False,
            'avatar_id': avatar_id
        }
        
        room["users"].append(new_user)
        db["rooms"][room_id] = room
        save_db(db)
        
        return {'user_id': user_id, 'room_info': room}, 200

def start_race(room_id, user_id):
    with db_lock:
        db = load_db()
        
        if room_id not in db["rooms"]:
            return {'error': 'Room not found'}, 404
        
        room = db["rooms"][room_id]
        
        if str(user_id) != str(room["admin_id"]):
            return {'error': 'Only the admin (host) can start the race'}, 403
            
        if room["state"] != 'WAITING':
            return {'error': 'The game is already in progress or finished'}, 400
        
        room["state"] = 'PLAYING'
        
        game_id = f"GAME_{room_id}_{random.randint(100, 999)}"
        text_to_type = "Distributed Systems is an amazing subject"
        
        room["game"] = {
            'id': game_id,
            'room_id': room_id,
            'text': text_to_type,
            'text_size': len(text_to_type),
            'state': 'RUNNING',
            'users_progress': []
        }
        
        for user in room["users"]:
            room["game"]["users_progress"].append({
                'user_id': user['id'],
                'progress': 0.0,
                'progress_index': 0
            })
        
        db["rooms"][room_id] = room
        save_db(db)
        
        return {'status': 'started', 'game': room["game"]}, 200