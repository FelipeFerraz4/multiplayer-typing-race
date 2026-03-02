import uuid
from models.room_repository import RoomRepository


class RoomService: # Remova o (rpyc.Service)
    def __init__(self):
        self.repo = RoomRepository()

    def create_room(self, user):
        room_id = str(uuid.uuid4())[:6].upper()
        room = {
            "id": room_id,
            "port": None,
            "id_admin": str(user["id"]),
            "state": "WAITING",
            "users": [user],
            "game": None
        }
        self.repo.save_room(room)
        return room

    def list_rooms(self):
        return self.repo.list_rooms()