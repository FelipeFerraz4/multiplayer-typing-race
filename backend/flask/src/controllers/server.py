from flask_restx import Namespace, Resource

ns = Namespace(name='server', path='server')

@ns.route('/')
class Server(Resource):
    pass