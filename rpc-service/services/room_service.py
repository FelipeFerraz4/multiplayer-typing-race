import uuid
from repository.room_repository import RoomRepository


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
        print("Listing rooms...")
        rooms = self.repo.list_rooms()
        print(rooms)
        return rooms
    
    def join_room(self, room_code, user):
        print("SERVICE: join_room iniciado")
        print("room_code:", room_code)
        print("user:", user)

        room = self.repo.find_by_code(room_code)
        print("ROOM ENCONTRADA:", room)

        if not room:
            print("Room not found")
            raise Exception("Room not found")

        if room["state"] != "WAITING":
            raise Exception("Room not accepting players")

        self.repo.add_user_to_room(room["id"], user)
        
        print("Usuário adicionado à sala. Atualizando informações da sala...")

        updated_room = self.repo.get_room_with_users(room["id"])
        print("ROOM ATUALIZADA:", updated_room)

        return updated_room
    
    def get_room(self, room_id):
        room = self.repo.get_room_with_users(room_id)

        if not room:
            raise Exception("Room not found")

        return room
    
    def leave_room(self, room_id, user_id):
        room = self.repo.get_room_with_users(room_id)

        if not room:
            raise Exception("Room not found")

        user_ids = [u["id"] for u in room["users"]]

        if user_id not in user_ids:
            raise Exception("User is not in this room")

        # Se for admin
        if room["id_admin"] == user_id:
            self.repo.delete_room(room_id)
            return {"message": "Room deleted because admin left"}

        # Remover usuário normal
        self.repo.remove_user_from_room(room_id, user_id)

        return self.repo.get_room_with_users(room_id)
    
    