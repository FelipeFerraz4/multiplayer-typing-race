import random
import uuid
from repository.game_repository import GameRepository
from repository.room_repository import RoomRepository
from repository.text_game import texts_game
import logging
from datetime import datetime, timedelta

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
    
    
    def update_progress(self, game_id, progress_update_request):
        print("\n================ UPDATE_PROGRESS START ================")
        print(f"[STEP 1] game_id recebido: {game_id}")
        print(f"[STEP 1] payload recebido: {progress_update_request}")

        try:
            user_id = progress_update_request["user_id"]
            typed_characters = progress_update_request["typed_characters"]
            errors = progress_update_request["errors"]
            elapsed_time = progress_update_request["elapsed_time"]
        except KeyError as e:
            print(f"[ERROR] Campo faltando no payload: {e}")
            raise

        print(f"[STEP 2] user_id={user_id}")
        print(f"[STEP 2] typed_characters={typed_characters}")
        print(f"[STEP 2] errors={errors}")
        print(f"[STEP 2] elapsed_time={elapsed_time}")

        game = self.repo.get_game_with_progress(game_id)

        print(f"[STEP 3] game buscado no banco: {game}")

        if not game:
            print("[ERROR] Game não encontrado")
            raise Exception("Game not found")

        print(f"[STEP 4] game state atual: {game['state']}")

        # Se já terminou, apenas retorna resultado
        if game["state"] == "FINISHED":
            print("[INFO] Game já está FINALIZADO")

            results = self.repo.get_game_results(game_id)

            if results:
                print("[INFO] Resultados já existem")
                return {
                    "type": "GAME_FINISHED",
                    "data": {
                        "game_id": game_id,
                        "results": results
                    }
                }
            else:
                print("[WARNING] Game está FINISHED mas sem resultados — regenerando")
                result = self.finish_game(game_id)
                
                print(f"[WARNING] Resultados regenerados: {result}")

                return {
                    "type": "GAME_FINISHED",
                    "data": result
                }

        # Se não estiver rodando e não estiver finalizado → erro
        if game["state"] != "RUNNING":
            print("[ERROR] Game não está RUNNING nem FINISHED")
            raise Exception("Game is not running")

        text_size = game["text_size"]
        print(f"[STEP 5] text_size={text_size}")

        if text_size == 0:
            print("[ERROR] text_size é 0 — divisão inválida")
            raise Exception("Invalid text size")

        if typed_characters > text_size:
            print("[STEP 6] typed_characters maior que text_size — ajustando")
            typed_characters = text_size

        progress_percentage = (typed_characters / text_size) * 100
        print(f"[STEP 7] progress_percentage calculado={progress_percentage}")

        print("[STEP 8] Atualizando progresso no banco...")
        self.repo.update_user_progress(
            game_id=game_id,
            user_id=user_id,
            progress=progress_percentage,
            progress_index=typed_characters,
            errors=errors,
            elapsed_time=elapsed_time
        )
        print("[STEP 8] Banco atualizado com sucesso")

        print("[STEP 9] Rebuscando jogo atualizado para verificar término...")
        updated_game = self.repo.get_game_with_progress(game_id)
        print(f"[STEP 9] updated_game: {updated_game}")

        print("[STEP 10] Chamando _should_finish_game...")
        should_finish = self._should_finish_game(updated_game)
        print(f"[STEP 10] should_finish={should_finish}")

        if should_finish:
            print("[STEP 11] Finalizando jogo...")
            result = self.finish_game(game_id)
            print(f"[STEP 11] Resultado final: {result}")
            print("================ UPDATE_PROGRESS END (FINISHED) ================\n")
            return {
                "type": "GAME_FINISHED",
                "data": result
            }

        print("================ UPDATE_PROGRESS END (PROGRESS_UPDATED) ================\n")
        return {
            "type": "PROGRESS_UPDATED",
            "data": {
                "user_id": user_id,
                "progress": progress_percentage,
                "progress_index": typed_characters
            }
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
        print("\n=========== FINISH_GAME START ===========")

        game = self.repo.get_game_with_progress(game_id)

        if not game:
            raise Exception("Game not found")

        # 🔥 Buscar progresso completo (com elapsed_time)
        progress_list = self.repo.get_all_progress(game_id)

        print("Progress list:", progress_list)

        if not progress_list:
            print("⚠ Nenhum progresso encontrado")
            return {
                "game_id": game_id,
                "state": "FINISHED",
                "results": []
            }

        # 🔥 Atualizar estado só depois de confirmar progresso
        self.repo.update_game_state(game_id, "FINISHED")

        # Ordenar ranking corretamente
        sorted_progress = sorted(
            progress_list,
            key=lambda p: (-p["progress"], p["elapsed_time"])
        )

        results = []

        for position, progress in enumerate(sorted_progress, start=1):

            print(f"Processando user {progress['user_id']}")

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

            print("Salvando resultado:", result)

            self.repo.save_game_result(result)

            results.append(result)

        print("=========== FINISH_GAME END ===========\n")

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
        print("Pegando os resultados")

        results = self.repo.get_game_results(game_id)

        print("Resultados: ", results)

        if not results:
            print("Nenhum resultado encontrado ainda")
            return {
                "game_id": game_id,
                "results": [],
                "status": "PROCESSING"
            }

        print("Resultados encontrados")

        return {
            "game_id": game_id,
            "results": results,
            "status": "FINISHED"
        }
            
    def _should_finish_game(self, game):
        progress_list = self.repo.get_all_progress(game["id"])

        # 🔥 1️⃣ Todos terminaram?
        all_finished = all(
            p["progress"] >= 100 for p in progress_list
        )

        # 🔥 2️⃣ Timeout 7 minutos
        created_at = game["created_at"]
        timeout_time = created_at + timedelta(minutes=7)

        timeout_reached = datetime.now() >= timeout_time

        return all_finished or timeout_reached