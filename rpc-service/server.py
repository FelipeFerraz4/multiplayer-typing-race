import rpyc
from rpyc.utils.classic import obtain
from rpyc.utils.server import ThreadedServer
from services.room_service import RoomService
from services.game_service import GameService

class RPCService(rpyc.Service):
    
    def on_connect(self, conn):
        self.room_service = RoomService()
        self.game_service = GameService()
    
    # =========================
    # ROOM METHODS
    # =========================

    def exposed_create_room(self, user_proxy):
        user = obtain(user_proxy)

        service = self.room_service
        return service.create_room(user)


    def exposed_join_room(self, room_code_proxy, user_proxy):
        # print("RPC: join_room foi chamado")

        room_code = obtain(room_code_proxy)
        user = obtain(user_proxy)

        # print("room_code:", room_code)
        # print("user:", user)

        service = self.room_service
        result = service.join_room(room_code, user)

        # print("RPC result:", result)

        return result


    def exposed_get_room(self, room_id_proxy):
        room_id = obtain(room_id_proxy)

        service = self.room_service
        return service.get_room(room_id)


    def exposed_leave_room(self, room_id_proxy, user_id_proxy):
        room_id = obtain(room_id_proxy)
        user_id = obtain(user_id_proxy)

        service = self.room_service
        return service.leave_room(room_id, user_id)


    def exposed_list_rooms(self):
        print("RPC: list_rooms called")
        service = self.room_service
        return service.list_rooms()
    
    # =========================
    # GAME METHODS
    # =========================
    
    def exposed_start_game(self, room_id_proxy, user_id_proxy):
        room_id = obtain(room_id_proxy)
        user_id = obtain(user_id_proxy).lower()
        print("Start request")
        print("Room: " + room_id)
        print("User: " + user_id)
        service = self.game_service
        return service.start_game(room_id, user_id)


    def exposed_get_game(self, game_id_proxy):
        game_id = obtain(game_id_proxy)

        service = self.game_service
        return service.get_game(game_id)


    def exposed_update_progress(
        self,
        game_id_proxy,
        progress_update_request_proxy
    ):
        print("Init request")
        game_id = obtain(game_id_proxy)
        progress_update_request = obtain(progress_update_request_proxy)

        service = self.game_service
        return service.update_progress(
            game_id,
            progress_update_request
        )


    def exposed_get_all_progress(self, game_id_proxy):
        game_id = obtain(game_id_proxy)

        service = self.game_service
        return service.get_all_progress(game_id)


    def exposed_finish_game(self, game_id_proxy):
        game_id = obtain(game_id_proxy)

        service = self.game_service
        return service.finish_game(game_id)


    def exposed_get_result(self, game_id_proxy):
        game_id = obtain(game_id_proxy)

        service = self.game_service
        return service.get_result(game_id)


if __name__ == "__main__":
    server = ThreadedServer(
        RPCService,
        hostname="0.0.0.0",
        port=18861,
        protocol_config={
            "allow_public_attrs": True,
            "allow_pickle": True,  # ADICIONE ISSO
        }
    )

    print("RPC Service running on port 18861...")
    server.start()