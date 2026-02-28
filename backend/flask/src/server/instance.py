from flask import Flask
from flask_restx import Api  # type: ignore
from flask_cors import CORS  # type: ignore
import os


class Server:
    def __init__(self):
        self.__app = Flask(__name__)

        CORS(self.__app)
        self.__app.config["CORS_HEADERS"] = "Content-Type"

        self.__api = Api(
            self.__app,
            title="Multiplayer Typing Race",
            description="Multiplayer Typing Race is a distributed application developed for the Distributed Systems course. "
            "The system enables multiple players to compete in real-time typing races, "
            "synchronizing game state across clients through a RESTful API. "
            "It manages player sessions, race rooms, score tracking, and ranking, "
            "ensuring consistency, scalability, and low-latency communication in a distributed environment.",
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
