from flask_restx import Namespace, Resource
from client import rpc_client
from models import game_model, progress_model, error_model, success_model, user_model, player_result_model, progress_update_model, progress_response_model

ns = Namespace('Games', path='/game', description='Game management and typing race control')

@ns.route('/<string:game_id>')
class GameById(Resource):

    @ns.response(404, 'Game not found', error_model)
    @ns.marshal_with(game_model, mask=None)
    @ns.doc('get_game', description='Retrieve a game by its identifier.')
    def get(self, game_id):
        try:
            game = rpc_client.call('get_game', game_id)
        except Exception:
            ns.abort(500, message='Internal server error')
        if not game:
            ns.abort(404, message='Game not found')
        return game
            
            
@ns.route('/<string:game_id>/progress')
class GameProgress(Resource):
    
    @ns.expect(progress_update_model, validate=True)
    @ns.response(404, 'Game not found', error_model)
    @ns.response(500, 'Internal server error', error_model)
    @ns.marshal_with(progress_response_model, mask=None)
    @ns.doc(
        'update_progress',
        description='Submit typing progress update for a specific user in the game.'
    )
    def post(self, game_id):
        data = ns.payload
        progress_update_request = {
            'user_id': data['user_id'],
            'typed_characters': data['typed_characters'],
            'errors': data['errors'],
            'elapsed_time': data['elapsed_time']
        }
        try:
            print("init endpoint")
            progress = rpc_client.call('update_progress', game_id, progress_update_request)
            print(progress)
            
        except Exception:
            ns.abort(500, message='Internal server error')
        if not progress:
            ns.abort(404, message='Game not found')
        return progress

    @ns.response(404, 'Game not found', error_model)
    @ns.response(500, 'Internal server error', error_model)
    @ns.marshal_list_with(progress_model, mask=None)
    @ns.doc(
        'get_all_progress',
        description='Retrieve the current progress of all users in the game.'
    )
    def get(self, game_id):
        try:
            users_progress = rpc_client.call('get_all_progress', game_id)
        except Exception:
            ns.abort(500, message='Internal server error')
        
        if not users_progress:
            ns.abort(404, message='Game not found')
        return users_progress

@ns.route('/<string:game_id>/finish')
class GameFinish(Resource):

    @ns.expect(user_model, validate=True)
    @ns.response(400, 'User is not the host', error_model)
    @ns.response(404, 'Game not found', error_model)
    @ns.response(500, 'Internal server error', error_model)
    @ns.marshal_with(game_model, mask=None)
    @ns.doc(
        'finish_game',
        description='Finish the typing race and compute final results.'
    )
    def post(self, game_id):
        is_host = ns.payload['is_host']
        if (not is_host):
            ns.abort(400, message='Only the host can end the game')
            
        try:
            game = rpc_client.call('finish_game', game_id)
        except Exception:
            ns.abort(500, message='Internal server error')
        
        if not game:
            ns.abort(404, message='Game not found')
        return game

@ns.route('/<string:game_id>/result')
class GameResult(Resource):

    @ns.response(404, 'Game not found', error_model)
    @ns.response(500, 'Internal server error', error_model)
    @ns.marshal_list_with(player_result_model, mask=None)
    @ns.doc(
        'get_result',
        description='Retrieve final ranking and results of the game.'
    )
    def get(self, game_id):
        try:
            game_result = rpc_client.call('get_result', game_id)
        except Exception:
            ns.abort(500, message='Internal server error')
            
        if not game_result:
            ns.abort(404, message='Game not found')
            
        return game_result.get('results', [])
        