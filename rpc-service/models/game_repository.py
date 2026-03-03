import json
from database.connection import get_connection

class GameRepository:
    def save_game(self, game):
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                INSERT INTO games (id, room_id, state, progress)
                VALUES (%s, %s, %s, %s)
            """, (
                game["id"],
                game["room_id"],
                game["state"],
                json.dumps(game["progress"])
            ))

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cur.close()
            conn.close()
            
            
    
    def get_game_with_progress(self, game_id):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # 🔹 Buscar o jogo
            cursor.execute("""
                SELECT id, room_id, text, text_size, state
                FROM games
                WHERE id = %s
            """, (game_id,))

            game_row = cursor.fetchone()

            if not game_row:
                return None

            game = {
                "id": str(game_row[0]),
                "room_id": str(game_row[1]),
                "text": game_row[2],
                "text_size": game_row[3],
                "state": game_row[4],
                "users_progress": []
            }

            # 🔹 Buscar progressos vinculados
            cursor.execute("""
                SELECT user_id, progress, progress_index
                FROM game_progress
                WHERE game_id = %s
            """, (game_id,))

            progress_rows = cursor.fetchall()

            for row in progress_rows:
                game["users_progress"].append({
                    "user_id": str(row[0]),
                    "progress": float(row[1]),
                    "progress_index": row[2]
                })

            return game

        finally:
            cursor.close()
            conn.close()