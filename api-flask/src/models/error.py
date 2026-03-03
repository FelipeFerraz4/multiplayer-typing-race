from flask_restx import fields
from server import server

api = server.api

error_model = api.model(
    'Error',
    {
        'message': fields.String(
            required=True,
            description="The error message",
            example='Entity not found'
        )
    }
)
