import json
from database.connection import get_connection

class RoomRepository:

    def save_room(self, room):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO rooms (id, state, id_admin, data)
            VALUES (%s, %s, %s, %s)
        """, (
            room["id"],
            room["state"],
            room["id_admin"],
            json.dumps(room)
        ))

        conn.commit()
        cur.close()
        conn.close()

    def list_rooms(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT data FROM rooms")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return [row[0] for row in rows]