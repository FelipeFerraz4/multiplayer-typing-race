import json
from database.connection import get_connection

class GameRepository:
    def create_game(self, game):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO games (id, room_id, text, text_size, state)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                game["id"],
                game["room_id"],
                game["text"],
                game["text_size"],
                game["state"]
            ))

            conn.commit()

        finally:
            cursor.close()
            conn.close()
            
            
    
    def get_game_with_progress(self, game_id):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # 🔹 Buscar o jogo
            cursor.execute("""
                SELECT id, room_id, text, text_size, state, created_at
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
                "created_at": game_row[5],
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
            
            
            
    def create_initial_progress(self, game_id, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Evita duplicidade (caso já exista)
            cursor.execute("""
                SELECT 1 FROM game_progress
                WHERE game_id = %s AND user_id = %s
            """, (game_id, user_id))

            exists = cursor.fetchone()

            if exists:
                return  # Já existe, não cria de novo

            cursor.execute("""
                INSERT INTO game_progress (
                    game_id,
                    user_id,
                    progress,
                    progress_index
                )
                VALUES (%s, %s, 0, 0)
            """, (game_id, user_id))

            conn.commit()

        finally:
            cursor.close()
            conn.close()
            

    def update_user_progress(
        self,
        game_id,
        user_id,
        progress,
        progress_index,
        errors,
        elapsed_time
    ):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE game_progress
                SET progress = %s,
                    progress_index = %s,
                    errors = %s,
                    elapsed_time = %s
                WHERE game_id = %s
                AND user_id = %s
            """, (
                progress,
                progress_index,
                errors,
                elapsed_time,
                game_id,
                user_id
            ))

            conn.commit()

        finally:
            cursor.close()
            conn.close()
            
            
    def get_all_progress(self, game_id):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT user_id, progress, progress_index, errors, elapsed_time
                FROM game_progress
                WHERE game_id = %s
                ORDER BY progress DESC
            """, (game_id,))

            rows = cursor.fetchall()

            progress_list = []

            for row in rows:
                progress_list.append({
                    "user_id": str(row[0]),
                    "progress": float(row[1]),
                    "progress_index": row[2],
                    "errors": row[3],
                    "elapsed_time": float(row[4])
                })

            return progress_list

        finally:
            cursor.close()
            conn.close()
            
            
    def update_game_state(self, game_id, state):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE games
            SET state = %s
            WHERE id = %s
        """, (state, game_id))

        conn.commit()
        cur.close()
        conn.close()


    def get_user_by_id(self, user_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, name
            FROM users
            WHERE id = %s
        """, (user_id,))

        row = cur.fetchone()

        cur.close()
        conn.close()

        if row:
            return {
                "id": row[0],
                "name": row[1]
            }

        return None
    
    
    
    def save_game_result(self, result):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO game_results
            (game_id, user_id, name, position, wpm, final_time)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            result["game_id"],
            result["user_id"],
            result["name"],
            result["position"],
            result["wpm"],
            result["final_time"]
        ))

        conn.commit()
        cur.close()
        conn.close()
        
        
    def get_game_results(self, game_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT user_id, name, position, wpm, final_time
            FROM game_results
            WHERE game_id = %s
            ORDER BY wpm DESC, final_time ASC
        """, (game_id,))

        rows = cur.fetchall()

        cur.close()
        conn.close()

        results = []

        for row in rows:
            results.append({
                "user_id": row[0],
                "name": row[1],
                "position": row[2],
                "wpm": row[3],
                "final_time": row[4]
            })

        return results