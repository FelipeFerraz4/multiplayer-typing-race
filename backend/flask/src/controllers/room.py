import random
import string
import threading
import json
import os
from flask_restx import Namespace, Resource
from flask import request

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

ns = Namespace(name='Rooms', path='/room')

@ns.route('/')
class RoomsList(Resource):
    
    def get(self): 
        db = load_db()
        return db["rooms"], 200

@ns.route('/create')
class CreateRoom(Resource):
    def post(self):
        data = request.json
        name = data.get('name')
        avatar_id = data.get('avatar_id')

        with db_lock:
            db = load_db()
            
            caracteres = string.ascii_uppercase + string.digits
            room_id = ''.join(random.choices(caracteres, k=4))
            while room_id in db["rooms"]:
                room_id = ''.join(random.choices(caracteres, k=4))
                
            user_id = str(random.randint(1, 10000))
            
            new_room = {
                'id': room_id,
                'port': None,
                'id_admin': user_id,
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
            
            return {'room_id': room_id, 'user_id': user_id, 'message': 'Sala criada com sucesso'}, 201

@ns.route('/<string:room_id>/enter')
class EnterRoom(Resource):
    def post(self, room_id):
        data = request.json
        name = data.get('name')
        avatar_id = data.get('avatar_id')

        with db_lock:
            db = load_db()
            
            if room_id not in db["rooms"]:
                return {'error': 'Sala não encontrada'}, 404
            
            room = db["rooms"][room_id]
            
            if room["state"] != 'WAITING':
                return {'error': 'A corrida já começou ou a sala está fechada'}, 400

            if len(room["users"]) >= 5:
                return {'error': 'A sala está cheia. O limite é de 5 jogadores.'}, 403
                
            ids_na_sala = [u["id"] for u in room["users"]]
            
            user_id = str(random.randint(1, 10000))
            while user_id in ids_na_sala:
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

@ns.route('/<string:room_id>/start')
class StartRace(Resource):
    def post(self, room_id):
        data = request.json
        user_id = data.get('user_id')

        with db_lock:
            db = load_db()
            
            if room_id not in db["rooms"]:
                return {'error': 'Sala não encontrada'}, 404
            
            room = db["rooms"][room_id]
            
            if str(user_id) != str(room["id_admin"]):
                return {'error': 'Apenas o admin (host) pode iniciar a corrida'}, 403
                
            if room["state"] != 'WAITING':
                return {'error': 'O jogo já está em andamento ou finalizado'}, 400
            
            room["state"] = 'PLAYING'
            
            game_id = f"GAME_{room_id}_{random.randint(100, 999)}"
            text_to_type = "Sistemas Distribuidos e uma disciplina incrivel"
            
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