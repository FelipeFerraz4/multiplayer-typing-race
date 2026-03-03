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