from flask_restx import Namespace, Resource
from models import room_model, user_model
from rpc_client import rpc_client

ns = Namespace(name='Rooms', path='/room', description='Room management endpoints for creating, joining, leaving, and controlling multiplayer typing race sessions.')

@ns.route('/')
class RoomColletion(Resource):

    @ns.marshal_list_with(room_model, mask=None)
    @ns.doc('list_rooms', description='Returns all active rooms.')
    def get(self):
        pass
    
    @ns.expect(user_model, validate=True)
    @ns.marshal_with(room_model, mask=None)
    @ns.doc('create_room', description='Create a new room.')
    def post(self):
        data = ns.payload

        user = {
            "id": data["id"],
            "name": data["name"],
            "is_host": data["is_host"],
            "avatar_id": data["avatar_id"]
        }

        room = rpc_client.call("create_room", user)

        if not room:
            ns.abort(500, "Não foi possível criar a sala no serviço RPC.")

        return room
    
@ns.route('/<string:room_id>')
class RoomById(Resource):

    @ns.marshal_with(room_model, mask=None)
    @ns.doc('get_room', description='Get room by id.')
    def get(self, room_id):
        pass

@ns.route('/<string:room_id>/start')
class RoomStart(Resource):
    
    def post(self):
        pass

@ns.route('/<string:room_id>/join')
class RoomJoin(Resource):

    @ns.expect(user_model, validate=True)
    @ns.marshal_with(room_model, mask=None)
    @ns.doc('join_room', description='Join a room.')
    def put(self, room_id):
        data = ns.payload
        
        user = {
            'id': data['id'],
            'name': data['name'],
            'is_host': data['is_host'],
            'avatar_id': data['avatar_id'],
        }
        pass
    
@ns.route('/<string:room_id>/leave')
class RoomLeave(Resource):
    
    @ns.expect(user_model, validate=True)
    @ns.marshal_with(room_model, mask=None)
    @ns.doc('leave_room', description='Leave a room.')
    def delete(self, room_id):
        pass
    
