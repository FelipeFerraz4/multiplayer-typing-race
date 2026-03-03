import rpyc
from rpyc.utils.classic import obtain
from rpyc.utils.server import ThreadedServer
from services.room_service import RoomService

class RPCService(rpyc.Service):

    def exposed_create_room(self, user_proxy):
        user = obtain(user_proxy)

        service = RoomService()
        return service.create_room(user)


    def exposed_join_room(self, room_code_proxy, user_proxy):
        room_code = obtain(room_code_proxy)
        user = obtain(user_proxy)

        service = RoomService()
        return service.join_room(room_code, user)


    def exposed_get_room(self, room_id_proxy):
        room_id = obtain(room_id_proxy)

        service = RoomService()
        return service.get_room(room_id)


    def exposed_leave_room(self, room_id_proxy, user_id_proxy):
        room_id = obtain(room_id_proxy)
        user_id = obtain(user_id_proxy)

        service = RoomService()
        return service.leave_room(room_id, user_id)


    def exposed_list_rooms(self):
        print("RPC: list_rooms called")
        service = RoomService()
        return service.list_rooms()


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