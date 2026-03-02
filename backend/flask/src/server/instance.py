from flask import Flask
from flask_restx import Api  # type: ignore
from flask_cors import CORS  # type: ignore
from flask_socketio import SocketIO, join_room, emit
import os


class Server:
    def __init__(self):
        self.__app = Flask(__name__)
        socketio = SocketIO(self.__app, cors_allowed_origins="*")

        CORS(self.__app)
        self.__app.config["CORS_HEADERS"] = "Content-Type"

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

    @app.setter
    def app(self, value) -> None:
        pass

    # def run(self) -> None:
    #     self.app.run(debug=True)

    def run(self) -> None:
        port = int(os.environ.get("PORT", 5000))
        self.app.run(debug=True, host="0.0.0.0", port=port)


server: Server = Server()
