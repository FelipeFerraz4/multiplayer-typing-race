from flask import Flask
from flask_restx import Api  # type: ignore
from flask_cors import CORS  # type: ignore
from flask_socketio import SocketIO, join_room, emit
import os


class Server:
    def __init__(self):
        self.__app = Flask(__name__)
        
        # No Docker, seu front responde na porta 80 (padrão http)
        # Se você acessar apenas 'localhost', a origem é 'http://localhost'
        allowed_origins = ["http://localhost", "http://127.0.0.1", "http://localhost:4200"]

        # 1. Flask CORS
        CORS(self.__app, resources={r"/*": {"origins": allowed_origins}})
        
        # 2. SocketIO CORS
        self.__socketio = SocketIO(
            self.__app, 
            cors_allowed_origins=allowed_origins,
            async_mode='eventlet'
        )

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

    @property
    def api(self) -> Api:
        return self.__api

    @api.setter
    def api(self, value) -> None:
        pass

    @property
    def app(self) -> Flask:
        return self.__app
    
    @property
    def socketio(self) -> SocketIO:
        return self.__socketio

    @app.setter
    def app(self, value) -> None:
        pass
    
    ''' @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    # Cliente entra na sala websocket
    @socketio.on('join_room')
    def handle_join(data):
        room_id = data['room_id']
        join_room(room_id)
        emit('message', {'msg': 'User joined'}, room=room_id)

    # Host inicia partida
    @socketio.on('start_game')
    def handle_start(data):
        room_id = data['room_id']
        emit('game_started', {'room_id': room_id}, room=room_id)
    
    if __name__ == '__main__':
        socketio.run(app, port=5000)    
    '''

    # def run(self) -> None:
    #     self.app.run(debug=True)

    def run(self) -> None:
        port = int(os.environ.get("PORT", 5000))
        # Isso garante que o eventlet gerencie as conexões corretamente
        print(f"Servidor subindo na porta {port}...")
        self.socketio.run(self.__app, debug=True, host="0.0.0.0", port=port, use_reloader=False)


server: Server = Server()
