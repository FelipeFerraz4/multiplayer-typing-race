import uuid
from models.game_repository import GameRepository

class GameService:
    
    def __init__(self):
        self.repo = GameRepository()

    def create_game(self, room_id, text, text_size):
        game_id = str(uuid.uuid4())

        game = {
            "id": game_id,
            "room_id": room_id,
            "text": text,
            "text_size": text_size,
            "state": "WAITING",
            "users_progress": []
        }

        self.repo.save_game(game)
        return game


    def get_game(self, game_id):
        game = self.repo.get_game_with_progress(game_id)

        if not game:
            raise Exception("Game not found")

        return game