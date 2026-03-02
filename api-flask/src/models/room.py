from flask_restx import fields
from server import server
from .states import ROOM_STATES
from .user import user_model
from .game import game_model

api = server.api

room_model = api.model(
    'Room',
    {
        'id': fields.String(
            required=True,
            description='Room identifier',
            example='4RA1'
        ),
        'port': fields.Integer(
            description='Dedicated port for game communication',
            example=6001
        ),
        'id_admin': fields.String(
            required=True,
            description='Admin (host) user id',
            example='7392'
        ),
        'state': fields.String(
            required=True,
            enum=ROOM_STATES,
            description='Room current state',
            example='WAITING'
        ),
        'users': fields.List(
            fields.Nested(user_model),
            description='Users currently inside the room'
        ),
        'game': fields.Nested(
            game_model,
            allow_null=True,
            description='Current game instance (nullable if not started)'
        )
    }
)
