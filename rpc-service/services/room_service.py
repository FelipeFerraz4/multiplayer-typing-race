import uuid
from models.room_repository import RoomRepository


def generate_room_code():
    return str(uuid.uuid4()).replace("-", "")[:6].upper()


class RoomService:

    def __init__(self):
        self.repo = RoomRepository()

    def create_room(self, user):
        room_id = str(uuid.uuid4())
        room_code = generate_room_code()

        room = {
            "id": room_id,
            "room_code": room_code,
            "port": None,
            "id_admin": user["id"],
            "state": "WAITING",
            "users": [user],
            "game": None
        }

        self.repo.save_room(room)
        return room

    def list_rooms(self):
        return self.repo.list_rooms()
    
    def join_room(self, room_code, user):
        # Buscar sala pelo código
        room = self.repo.find_by_code(room_code)

        if not room:
            raise Exception("Room not found")

        if room["state"] != "WAITING":
            raise Exception("Room is not accepting players")

        # Adicionar usuário
        self.repo.add_user_to_room(room["id"], user)

        # Retornar sala atualizada
        return self.repo.get_room_with_users(room["id"])