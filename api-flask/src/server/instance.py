from flask import Flask, request  # <--- IMPORT CORRETO AQUI
from flask_restx import Api
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, emit
import os

class Server:
    def __init__(self):
        self.__app = Flask(__name__)
        
        allowed_origins = ["http://localhost", "http://127.0.0.1", "http://localhost:4200"]

        CORS(self.__app, resources={r"/*": {"origins": allowed_origins}})
        
        self.__socketio = SocketIO(
            self.__app, 
            cors_allowed_origins=allowed_origins,
            async_mode='eventlet'
        )
        
        # Registrar eventos
        self.register_socket_events()

        self.__api = Api(
            self.__app,
            title="Multiplayer Typing Race",
            description=(
                "Multiplayer Typing Race is a distributed application developed for the Distributed Systems course."
                "The system enables multiple players to compete in real-time typing races, "
                "synchronizing game state across clients through a RESTful API."
                "It manages player sessions, race rooms, score tracking, and ranking, "
                "ensuring consistency, scalability, and low-latency communication in a distributed environment.\n\n"
                "## WebSocket Events\n\n"
                "The system also exposes real-time communication via WebSocket.\n\n"
                "### Client → Server Events\n"
                "- `join_room`\n"
                "- `leave_room`\n"
                "- `start_game`\n"
                "- `send_progress`\n\n"
                "### Server → Client Events\n"
                "- `room_joined`\n"
                "- `game_started`\n"
                "- `progress_update`\n"
                "- `game_finished`\n"
            ),
            doc="/",
        )

    def register_socket_events(self):
        # Usamos o objeto da instância para garantir o registro
        socketio = self.__socketio

        @socketio.on('connect')
        def handle_connect():
            # request.sid identifica unicamente o navegador que conectou
            print(f"🔌 [Socket] Conectado: {request.sid}")

        @socketio.on('join_room')
        def on_join(data):
            room_id = data.get('room_id')
            if room_id:
                join_room(room_id)
                print(f"🏠 [Socket] Cliente {request.sid} entrou na sala: {room_id}")
            else:
                print("⚠️ [Socket] join_room sem ID")

        @socketio.on('start_game')
        def on_start(data):
            room_id = data.get('room_id')
            print(f"🚀 [Socket] START_GAME na sala: {room_id}")
            socketio.emit('game_started', {'room_id': room_id}, room=room_id)
            
        @socketio.on('send_progress')
        def handle_progress(data):
            room_id = data.get('room_id')
            # Repassa o progresso para todos na sala (inclusive o remetente se necessário)
            emit('progress_update', {
                'user_id': data.get('user_id'),
                'progress': data.get('progress')
            }, room=room_id, include_self=False)

    @property
    def api(self) -> Api: return self.__api

    @property
    def app(self) -> Flask: return self.__app
    
    @property
    def socketio(self) -> SocketIO: return self.__socketio

    def run(self) -> None:
        port = int(os.environ.get("PORT", 5000))
        print(f"Servidor subindo na porta {port}...")
        self.__socketio.run(self.__app, debug=True, host="0.0.0.0", port=port, use_reloader=False)

server = Server()