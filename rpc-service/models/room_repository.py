import json
from database.connection import get_connection

class RoomRepository:

    def save_room(self, room):
        conn = get_connection()
        cur = conn.cursor()

        try:
            admin = room["users"][0]

            # Inserir usuário
            cur.execute("""
                INSERT INTO users (id, name, is_host, avatar_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                admin["id"],
                admin["name"],
                admin["is_host"],
                admin["avatar_id"]
            ))

            # Inserir sala com room_code
            cur.execute("""
                INSERT INTO rooms (id, room_code, port, state, id_admin, game)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                room["id"],
                room["room_code"],
                room["port"],
                room["state"],
                room["id_admin"],
                None
            ))

            # Relacionamento
            cur.execute("""
                INSERT INTO room_users (room_id, user_id)
                VALUES (%s, %s)
            """, (
                room["id"],
                admin["id"]
            ))

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cur.close()
            conn.close()
            
    def get_room_by_code(self, room_code):
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT id FROM rooms WHERE room_code = %s
            """, (room_code,))
            result = cur.fetchone()
            return result[0] if result else None
        except Exception as e:
            raise e
        finally:
            cur.close()
            conn.close()    
            

    def find_by_code(self, room_code):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, room_code, port, state, id_admin, game
            FROM rooms
            WHERE room_code = %s
        """, (room_code,))

        row = cur.fetchone()

        cur.close()
        conn.close()

        if not row:
            return None

        return {
            "id": row[0],
            "room_code": row[1],
            "port": row[2],
            "state": row[3],
            "id_admin": row[4],
            "game": row[5]
        }
        
    
    def add_user_to_room(self, room_id, user):
        conn = get_connection()
        cur = conn.cursor()

        try:
            # Inserir usuário
            cur.execute("""
                INSERT INTO users (id, name, is_host, avatar_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                user["id"],
                user["name"],
                False,  # quem entra nunca é host
                user["avatar_id"]
            ))

            # Relacionar usuário à sala
            cur.execute("""
                INSERT INTO room_users (room_id, user_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (
                room_id,
                user["id"]
            ))

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cur.close()
            conn.close()

    def get_room_with_users(self, room_id):
        conn = get_connection()
        cur = conn.cursor()

        # Buscar sala
        cur.execute("""
            SELECT id, room_code, port, state, id_admin, game
            FROM rooms
            WHERE id = %s
        """, (room_id,))
        room_row = cur.fetchone()
        
        if not room_row:
            cur.close()
            conn.close()
            return None

        # Buscar usuários da sala
        cur.execute("""
            SELECT u.id, u.name, u.is_host, u.avatar_id
            FROM users u
            JOIN room_users ru ON ru.user_id = u.id
            WHERE ru.room_id = %s
        """, (room_id,))
        users_rows = cur.fetchall()

        cur.close()
        conn.close()

        users = []
        for u in users_rows:
            users.append({
                "id": u[0],
                "name": u[1],
                "is_host": u[2],
                "avatar_id": u[3]
            })

        return {
            "id": room_row[0],
            "room_code": room_row[1],
            "port": room_row[2],
            "state": room_row[3],
            "id_admin": room_row[4],
            "game": room_row[5],
            "users": users
        }
        
        
    def list_rooms(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, room_code, port, state, id_admin, game
            FROM rooms
            ORDER BY created_at DESC
        """)

        rooms_rows = cur.fetchall()

        rooms = []

        for room in rooms_rows:
            room_id = room[0]

            cur.execute("""
                SELECT u.id, u.name, u.is_host, u.avatar_id
                FROM users u
                JOIN room_users ru ON ru.user_id = u.id
                WHERE ru.room_id = %s
            """, (room_id,))

            users_rows = cur.fetchall()

            users = [
                {
                    "id": u[0],
                    "name": u[1],
                    "is_host": u[2],
                    "avatar_id": u[3]
                }
                for u in users_rows
            ]

            rooms.append({
                "id": room[0],
                "room_code": room[1],
                "port": room[2],
                "state": room[3],
                "id_admin": room[4],
                "game": room[5],
                "users": users
            })

        cur.close()
        conn.close()

        return rooms
    
    
    def remove_user_from_room(self, room_id, user_id):
        conn = get_connection()
        cur = conn.cursor()

        try:
            # Remove vínculo
            cur.execute("""
                DELETE FROM room_users
                WHERE room_id = %s AND user_id = %s
            """, (room_id, user_id))

            # Opcional: remover usuário da tabela users
            cur.execute("""
                DELETE FROM users
                WHERE id = %s
            """, (user_id,))

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cur.close()
            conn.close()
            
            
    def delete_room(self, room_id):
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                DELETE FROM rooms
                WHERE id = %s
            """, (room_id,))

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cur.close()
            conn.close()
            
    
    def update_room_game(self, room_id, game_id):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE rooms
                SET game_id = %s
                WHERE id = %s
            """, (game_id, room_id))

            conn.commit()

        finally:
            cursor.close()
            conn.close()
            
    
    def update_room_state(self, room_id, new_state):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE rooms
                SET state = %s
                WHERE id = %s
            """, (new_state, room_id))

            conn.commit()

        finally:
            cursor.close()
            conn.close()