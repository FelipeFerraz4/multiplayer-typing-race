from flask_restx import Namespace, Resource
from models import game_model, progress_model, user_model, player_result_model, progress_update_model

ns = Namespace('Games', path='/game', description='Game management and typing race control')

@ns.route('/<string:game_id>')
class GameById(Resource):

    @ns.marshal_with(game_model, mask=None)
    @ns.doc('get_game', description='Retrieve a game by its identifier.')
    def get(self, game_id):
        pass

@ns.route('/<string:game_id>/start')
class GameStart(Resource):

    @ns.expect(user_model, validate=True)
    @ns.marshal_with(game_model, mask=None)
    @ns.doc(
        'start_game',
        description='Start the typing race. Only the host user is allowed to perform this action.'
    )
    def post(self, game_id):
        pass

@ns.route('/<string:game_id>/progress')
class GameProgress(Resource):
    
    @ns.expect(progress_update_model, validate=True)
    @ns.doc(
        'update_progress',
        description='Submit typing progress update for a specific user in the game.'
    )
    def post(self, game_id):
        pass

    @ns.marshal_list_with(progress_model, mask=None)
    @ns.doc(
        'get_all_progress',
        description='Retrieve the current progress of all users in the game.'
    )
    def get(self, game_id):
        pass

@ns.route('/<string:game_id>/finish')
class GameFinish(Resource):

    @ns.expect(user_model, validate=True)
    @ns.marshal_with(game_model, mask=None)
    @ns.doc(
        'finish_game',
        description='Finish the typing race and compute final results.'
    )
    def post(self, game_id):
        pass

@ns.route('/<string:game_id>/result')
class GameResult(Resource):

    @ns.doc(
        'get_result',
        description='Retrieve final ranking and results of the game.'
    )
    @ns.marshal_list_with(player_result_model, mask=None)
    def get(self, game_id):
        pass