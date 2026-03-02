from flask_restx import fields
from server import server

api = server.api

player_result_model = api.model(
    'PlayerResult',
    {
        'user_id': fields.String(
            required=True,
            description='User identifier',
            example='7392'
        ),
        'name': fields.String(
            required=True,
            description='User display name',
            example='Felipe'
        ),
        'position': fields.Integer(
            required=True,
            description='Final ranking position',
            example=1
        ),
        'wpm': fields.Float(
            required=True,
            description='Words per minute achieved',
            example=78.5
        ),
        'final_time': fields.Float(
            required=True,
            description='Total time to finish in seconds',
            example=42.3
        ),
    }
)