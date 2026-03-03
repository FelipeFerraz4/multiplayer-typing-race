from flask_restx import Namespace, Resource
from models import room_model, user_model, error_model
from client import rpc_client
from server import server
import uuid

ns = Namespace(name='Rooms', path='/room', description='Room management endpoints for creating, joining, leaving, and controlling multiplayer typing race sessions.')

@ns.route('/')
class RoomColletion(Resource):

    @ns.response(500, 'Internal server error', error_model)
    @ns.marshal_list_with(room_model, mask=None)
    @ns.doc('list_rooms', description='Returns all active rooms.')
    def get(self):
        try:
            print("API: list_rooms called")
            rooms = rpc_client.call('list_rooms')
            print(rooms)
            return rooms
        except:
            ns.abort(500, 'Internal server error')
    
    @ns.expect(user_model, validate=True)
    @ns.response(400, 'User is not host', error_model)
    @ns.response(500, 'Internal server error', error_model)
    @ns.marshal_with(room_model, mask=None)
    @ns.doc('create_room', description='Create a new room.')
    def post(self):
        data = ns.payload

        user = {
            "id": str(uuid.uuid4()).upper(),
            "name": data["name"],
            "is_host": data["is_host"],
            "avatar_id": data["avatar_id"]
        }
        
        if not user['is_host']:
            ns.abort(400, message='Only host can create a new room')

        try:
            room = rpc_client.call("create_room", user)
        except Exception:
            ns.abort(500, 'Internal server error')

        if not room:
            ns.abort(500, 'Error during room creation')

        return room
    
@ns.route('/<string:room_id>')
class RoomById(Resource):

    @ns.response(404, 'Room not found', error_model)
    @ns.response(500, 'Internal server error', error_model)
    @ns.marshal_with(room_model, mask=None)
    @ns.doc('get_room', description='Get room by id.')
    def get(self, room_id):
        try:
            room = rpc_client.call('get_room', room_id)
        except Exception:
            ns.abort(500, 'Internal server error')
        if not room:
            ns.abort(404, message='Room not found')
        return room

@ns.route('/join')
class RoomJoin(Resource):

    @ns.expect(user_model, validate=True)
    @ns.response(404, 'Room not found', error_model)
    @ns.response(400, 'Can not enter room', error_model)
    @ns.response(500, 'Internal server error', error_model)
    @ns.marshal_with(room_model, mask=None)
    @ns.doc('join_room', description='Join a room.')
    def put(self):
        """ENTRAR NA SALA"""
        data = ns.payload
        user = {
            'id': str(uuid.uuid4()).upper(),
            'name': data['name'],
            'is_host': data['is_host'],
            'avatar_id': data['avatar_id'],
        }
        room_code = data['room_code']
        
        try:    
            print(f" [RPC] Join Room: {room_code}")
            room = rpc_client.call('join_room', room_code, user)
            
            if room:
                room_id = room['id']
                print(f" [Socket] Emitindo 'room_joined' para sala: {room_id}")
                # 🚀 USANDO A INSTÂNCIA server:
                server.socketio.emit('room_joined', {'status': 'updated'}, room=room_id)
            
            return room
        except Exception as e:
            print(f" Erro Join: {e}")
            ns.abort(500, message='Internal server error')
        
@ns.route('/<string:room_id>/leave')
class RoomLeave(Resource):
    
    @ns.expect(user_model, validate=True)
    @ns.response(404, 'Room not found', error_model)
    @ns.response(500, 'Internal server error', error_model)
    @ns.marshal_with(room_model, mask=None)
    @ns.doc('leave_room', description='Leave a room.')
    def delete(self, room_id):
        try:
            room = rpc_client.call('leave_room', room_id)
        except Exception:
            ns.abort(500, message='Internal server error')
        if not room:
            ns.abort(404, message='Room not found')
        return room
    
