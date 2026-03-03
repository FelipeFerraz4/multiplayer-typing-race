from flask_restx import fields
from server import server

api = server.api

success_model = api.model(
    'Success',
    {
        'message': fields.String(
            required=True,
            description="The success message",
            example='Update done successfully'
        )
    }
)
