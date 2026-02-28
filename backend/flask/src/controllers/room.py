from flask_restx import Namespace, Resource

ns = Namespace(name='Rooms', path='/room')

@ns.route('/')
class RoomsList(Resource):
    
    def get():
        pass
