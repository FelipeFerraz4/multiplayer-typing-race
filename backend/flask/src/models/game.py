from flask_restx import fields
from server import server
from .states import GAME_STATES

api = server.api

progress_model = api.model(
    'UserProgress',
    {
        'user_id': fields.String(
            required=True,
            description='User identifier'
        ),
        'progress': fields.Float(
            required=True,
            description='Typing progress percentage',
            example=42.5
        ),
        'progress_index': fields.Integer(
            required=True,
            description='Typing progress index',
            example=14
        ),
    }
)

game_model = api.model(
    'Game',
    {
        'id': fields.String(
            required=True,
            description='Game identifier',
            example='GAME123'
        ),
        'room_id': fields.String(
            required=True,
            description='Associated room identifier'
        ),
        'text': fields.String(
            required=True,
            description='Text used in typing competition'
        ),
        'text_size': fields.Integer(
            required=True,
            description='The size of text used in the typing race',
            example=14
        ),
        'state': fields.String(
            required=True,
            enum=GAME_STATES,
            description='Current game state',
            example='RUNNING'
        ),
        'users_progress': fields.List(
            fields.Nested(progress_model),
            description='Progress of each user'
        )
    }
)