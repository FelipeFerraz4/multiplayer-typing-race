import random
import uuid
from repository.game_repository import GameRepository
from repository.room_repository import RoomRepository
from repository.text_game import texts_game
import logging

logger = logging.getLogger(__name__)


class GameService:    
    
    def __init__(self):
        self.repo = GameRepository()
        self.room_repo = RoomRepository()

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
    
    
    def start_game(self, room_id, user_id):
        print(f"[START_GAME] Request received - room_id={room_id} user_id={user_id}")

        text = random.choice(texts_game)
        text_size = len(text)

        print(f"[START_GAME] Selected text size={text_size}")

        # Buscar sala
        room = self.room_repo.get_room_with_users(room_id)

        if not room:
            print(f"[START_GAME] Room not found - room_id={room_id}")
            raise Exception("Room not found")

        print(f"[START_GAME] Room found - state={room['state']} admin={room['id_admin']}")

        if room["id_admin"] != user_id:
            print(f"[START_GAME] Unauthorized start attempt - user={user_id}")
            raise Exception("Only the host can start the game")

        if room["state"] != "WAITING":
            print(f"[START_GAME] Room not ready - state={room['state']}")
            raise Exception("Room is not ready to start")

        if len(room["users"]) < 1:
            print("[START_GAME] No players in room")
            raise Exception("No players in room")

        # Criar game
        game_id = str(uuid.uuid4())
        print(f"[START_GAME] Creating game_id={game_id}")

        game = {
            "id": game_id,
            "room_id": room_id,
            "text": text,
            "text_size": text_size,
            "state": "RUNNING"
        }

        self.repo.create_game(game)
        print("[START_GAME] Game created in repository")

        self.room_repo.update_room_game(room_id, game)
        self.room_repo.update_room_state(room_id, "PLAYING")

        print("[START_GAME] Room updated to PLAYING")

        # Criar progresso inicial
        for user in room["users"]:
            self.repo.create_initial_progress(game_id, user["id"])
            print(f"[START_GAME] Initial progress created for user={user['id']}")

        print(f"[START_GAME] Game successfully started - game_id={game_id}")

        return self.repo.get_game_with_progress(game_id)
    
    
    def update_progress(self, game_id, user_id, typed_characters, errors, elapsed_time):

        # Buscar jogo
        game = self.repo.get_game_with_progress(game_id)

        if not game:
            raise Exception("Game not found")

        if game["state"] != "RUNNING":
            raise Exception("Game is not running")

        text_size = game["text_size"]

        if typed_characters > text_size:
            typed_characters = text_size

        # Calcular porcentagem
        progress_percentage = (typed_characters / text_size) * 100

        # Atualizar progresso no banco
        self.repo.update_user_progress(
            game_id=game_id,
            user_id=user_id,
            progress=progress_percentage,
            progress_index=typed_characters,
            errors=errors,
            elapsed_time=elapsed_time
        )

        # Verificar se terminou
        finished = typed_characters >= text_size

        return {
            "progress": progress_percentage,
            "finished": finished
        }
        
        
    def get_all_progress(self, game_id):
        # 🔹 Verifica se o jogo existe
        game = self.repo.get_game_with_progress(game_id)

        if not game:
            raise Exception("Game not found")

        # Busca todos os progressos
        progress_list = self.repo.get_all_progress(game_id)

        return progress_list    
    
    
    def finish_game(self, game_id):
        # Buscar jogo com progresso
        game = self.repo.get_game_with_progress(game_id)

        if not game:
            raise Exception("Game not found")

        # Atualizar estado do jogo
        self.repo.update_game_state(game_id, "FINISHED")

        progress_list = game["users_progress"]

        # Ordenar ranking
        sorted_progress = sorted(
            progress_list,
            key=lambda p: (-p["progress"], p["elapsed_time"])
        )

        results = []

        for position, progress in enumerate(sorted_progress, start=1):

            user = self.repo.get_user_by_id(progress["user_id"])

            wpm = self._calculate_wpm(progress)

            result = {
                "game_id": game_id,
                "user_id": progress["user_id"],
                "name": user["name"] if user else "",
                "position": position,
                "wpm": wpm,
                "final_time": progress["elapsed_time"]
            }

            # Salvar no banco
            self.repo.save_game_result(result)

            results.append(result)

        return {
            "game_id": game_id,
            "state": "FINISHED",
            "results": results
        }
        
        
    def _calculate_wpm(self, progress):
        typed_chars = progress.get("progress_index", 0)
        elapsed_time = progress.get("elapsed_time", 1)

        words = typed_chars / 5  # média padrão: 5 chars = 1 palavra
        minutes = elapsed_time / 60

        if minutes == 0:
            return 0

        return round(words / minutes, 2)
    
    
    
    def get_result(self, game_id):
        results = self.repo.get_game_results(game_id)

        if not results:
            raise Exception("Results not found")

        return {
            "game_id": game_id,
            "results": results
        }